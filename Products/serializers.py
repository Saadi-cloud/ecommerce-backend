from rest_framework import serializers
from Products.models import Product, Cart, Checkout, CheckoutProduct

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checkout
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckoutProduct
        fields = '__all__'