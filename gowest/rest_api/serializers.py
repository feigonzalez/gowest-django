from rest_framework import serializers
from core.models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name']

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id','name']

class SecQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecQuestion
        fields = ['id','question']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['rut', 'name', 'surname', 'mail', 'phone', 'password', 'role', 'secQuestion', 'secAnswer']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id','streetName','streetNumber','postalCode','user','district']

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ['saleDate', 'deliveryDate', 'status', 'total', 'user', 'address', 'subscribed']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'image', 'price', 'stock', 'category']

class SaleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleDetail
        fields = ['id','sale','product','units','subtotal']