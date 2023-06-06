from rest_framework import serializers
from core.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['rut', 'name', 'surname', 'mail', 'phone', 'password', 'role', 'secQuestion', 'secAnswer']

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ['saleDate', 'deliveryDate', 'status', 'total', 'user', 'address', 'subscribed']