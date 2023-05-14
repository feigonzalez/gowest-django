from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'core/index.html')

def adminIndex(request):
    return render(request, 'core/adminIndex.html')

def signup(request):
    return render(request, 'core/signup.html')

"""
    path('account/', signup, name='account'),
    path('cart/', signup, name='cart'),
    path('category/', signup, name='category'),
    path('product/', signup, name='product'),
    path('recoverPass/', signup, name='recoverPass'),
"""

def account(request):
    return render(request, 'core/account.html')

def cart(request):
    return render(request, 'core/cart.html')

def category(request):
    return render(request, 'core/category.html')

def product(request):
    return render(request, 'core/product.html')

def recoverPass(request):
    return render(request, 'core/recoverPass.html')