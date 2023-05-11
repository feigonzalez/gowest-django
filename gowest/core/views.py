from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'core/index.html')

def adminIndex(request):
    return render(request, 'core/adminIndex.html')

def signup(request):
    return render(request, 'core/signup.html')