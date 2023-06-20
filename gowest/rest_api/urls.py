from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('getUsers', getUsers, name='getUsers'),
    path('getSales', getSales, name='getSales'),
    path('getProducts', getProducts, name='getProducts'),
    path('getProduct/<int:id>', getProduct, name='getProduct'),
    path('getCategory/<int:id>', getCategory, name='getCategory'),
    ]