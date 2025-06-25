from rest_framework import serializers
from .models import Category, Product, Cart, CartItem, Order, Review

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'description')

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Product
        fields = (
            'id', 'name', 'slug', 'category',
            'description', 'price', 'stock',
            'available', 'created_at'
        )


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ('id', 'product', 'quantity', 'created_at')

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ('id', 'user', 'items', 'total_price', 'created_at')

    def get_total_price(self, obj):
        return sum(
            item.product.price * item.quantity
            for item in obj.items.all()
        )

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'user', 'amount', 'currency', 'status', 'created_at')


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    
    class Meta:
        model = Review
        fields = ('id', 'user', 'product', 'rating', 'comment', 'created_at')
        read_only_fields = ('user', 'created_at')