from rest_framework import serializers
from .models import Store, Product

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'store_name']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'product_name', 'is_available', 'store']

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_name', 'is_available', 'store']
