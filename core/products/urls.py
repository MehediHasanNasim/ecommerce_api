from django.urls import path
from .views import (
    ProductListView, 
    CategoryListView,
    CartView,
    AddToCartView,
    CheckoutView,
    stripe_webhook  
)
urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('categories/', CategoryListView.as_view(), name='category-list'),

    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/', AddToCartView.as_view(), name='add-to-cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('stripe-webhook/', stripe_webhook, name='stripe-webhook'),
]