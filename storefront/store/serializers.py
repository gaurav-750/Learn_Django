from rest_framework import serializers
from .models import Product, Collection, Review, Cart, CartItem
from django.db.models import Count
from django.db import connection
from decimal import Decimal


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'slug', 'unit_price',
                  'price_with_tax', 'inventory', 'collection']

    # *Custom serializer fields:
    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')

    def calculate_tax(self, product: Product):
        return round(product.unit_price * Decimal(1.1), 2)

    # *Serializing Objects:
    # collection = serializers.PrimaryKeyRelatedField(
    #     queryset=Collection.objects.all()
    # )
    # collection = serializers.StringRelatedField()
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(),
    #     view_name='collection-detail'
    # )

    # collection = CollectionSerializer(read_only=True)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'name', 'description', 'date']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField(
        method_name='get_total_price')

    def get_total_price(self, item: CartItem):
        return item.product.unit_price * item.quantity

    class Meta:
        model = CartItem
        fields = ['id', 'quantity', 'product', 'total_price']


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    cartitems = CartItemSerializer(many=True)
    total_amount = serializers.SerializerMethodField(
        method_name='get_total_amount')

    def get_total_amount(self, cart: Cart):
        amt = 0
        for item in cart.cartitems.all():
            amt += (item.product.unit_price * item.quantity)
        return amt

    class Meta:
        model = Cart
        fields = ['id', 'cartitems', 'total_amount']
