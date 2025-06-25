from django.urls import path
from .views import (
    ProductListView, 
    CategoryListView,
    CartView,
    AddToCartView,
    CheckoutView,
    stripe_webhook,
    scrape_books_view,
    ProductReviewsView, 
    ReviewCreateView
)
urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('categories/', CategoryListView.as_view(), name='category-list'),

    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/', AddToCartView.as_view(), name='add-to-cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('stripe-webhook/', stripe_webhook, name='stripe-webhook'),
    path('scrape-books/', scrape_books_view, name='scrape-books'),
    path('products/<int:product_id>/reviews/', ProductReviewsView.as_view(), name='product-reviews'),
    path('reviews/create/', ReviewCreateView.as_view(), name='create-review'),
]