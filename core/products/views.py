from rest_framework import generics, filters, status, permissions
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Category, Cart, CartItem, Order, Review
from .serializers import ProductSerializer, CategorySerializer, CartSerializer, CartItemSerializer, OrderSerializer, ReviewSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework.decorators import api_view

import stripe
import json

stripe.api_key = settings.STRIPE_SECRET_KEY

from .utils import scrape_books

class StandardResultsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(available=True)
    serializer_class = ProductSerializer
    pagination_class = StandardResultsPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category']
    search_fields = ['name', 'description']

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer



class CartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart

class AddToCartView(generics.CreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)

class CheckoutView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        cart = Cart.objects.get(user=request.user)
        total_price = sum(
            item.product.price * item.quantity
            for item in cart.items.all()
        )

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': settings.STRIPE_CURRENCY,
                        'product_data': {
                            'name': 'Your Order',
                        },
                        'unit_amount': int(total_price * 100),  
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=settings.FRONTEND_SUCCESS_URL + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=settings.FRONTEND_CANCEL_URL,
                metadata={
                    'user_id': request.user.id,
                    'cart_id': cart.id,
                }
            )
            return Response({'session_url': checkout_session.url})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        user_id = session['metadata']['user_id']
        cart_id = session['metadata']['cart_id']

        Order.objects.create(
            user_id=user_id,
            stripe_payment_intent_id=session['payment_intent'],
            amount=session['amount_total'] / 100,
            currency=session['currency'],
            status='paid'
        )

        # Clear the cart after successful payment
        CartItem.objects.filter(cart_id=cart_id).delete()

    return HttpResponse(status=200)



class ReviewCreateView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ProductReviewsView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return Review.objects.filter(product_id=product_id)

@api_view(['GET'])
def scrape_books_view(request):
    try:
        books = scrape_books()
        return Response(books)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    