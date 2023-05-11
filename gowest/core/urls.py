from django.contrib import admin
from django.urls import path, include
from .views import index, adminIndex, signup

urlpatterns = [
    path('', index, name='index'),
    path('admin/', adminIndex, name='adminIndex'),
    path('signup/', signup, name='signup'),
]