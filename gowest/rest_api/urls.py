from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('getUsers', getUsers, name='getUsers'),
    path('getSales', getSales, name='getSales'),
    path('getProducts', getProducts, name='getProducts'),
    path('getUser/<int:id>', getUser, name='getUser'),
    path('getUserSQ/<str:mail>', getUserSQ, name='getUserSQ'),
    path('getProduct/<int:id>', getProduct, name='getProduct'),
    path('getCategory/<int:id>', getCategory, name='getCategory'),
    path('getAddress/<int:id>', getAddress, name='getAddress'),
    path('getAddressesByUser/<int:id>', getAddressesByUser, name='getAddressesByUser'),
    path('getSaleDetails/<int:id>', getSaleDetails, name='getSaleDetails'),
    path('addToCart',addToCart,name='addToCart'),
    path('setToCart',setToCart,name='setToCart'),
    path('getCartItemAmount',getCartItemAmount,name='getCartItemAmount'),
    path('removeFromCart/<int:dID>',removeFromCart,name='removeFromCart'),
    path('isRutAvailable/<str:rut>',isRutAvailable,name='isRutAvailable'),
    path('isMailAvailable/<str:mail>',isMailAvailable,name='isMailAvailable')
    ]