from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('getUsers', getUsers, name='getUsers'),
    path('getSales', getSales, name='getSales'),
    ]