
from .models import ProductModel, OrderModel
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderModel
        fields = "__all__"