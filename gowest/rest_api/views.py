from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from core.models import *
from .serializers import *

# Create your views here.

@csrf_exempt
@api_view(['GET', 'POST'])
def getUsers(request):
    if request.method == "GET":
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET', 'POST'])
def getSales(request):
    if request.method == "GET":
        sales = Sale.objects.all()
        serializer = SaleSerializer(sales, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        data = JSONParser().parse(request)
        serializer = SaleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET', 'POST'])
def getProducts(request):
    if request.method == "GET":
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        data = JSONParser().parse(request)
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
@csrf_exempt
@api_view(['GET'])
def getProduct(request, id):
    return Response(ProductSerializer(Product.objects.get(id=id)).data)            

@csrf_exempt
@api_view(['GET'])
def getCategory(request, id):
    return Response(CategorySerializer(Category.objects.get(id=id)).data)

@csrf_exempt
@api_view(['GET'])
def getUser(request, id):
    return Response(UserSerializer(User.objects.get(id=id)).data)

@csrf_exempt
@api_view(['GET'])
def getUserSQ(request, rut):
    if User.objects.filter(rut=rut).count()==0:
        return Response(False)
    else:
        return Response(User.objects.get(rut=rut).secQuestion.question)

@csrf_exempt
@api_view(['POST'])
def addToCart(request):
    data = JSONParser().parse(request)
    print(data)
    """user = User.objects.get(id=int(data["uID"]))
    product = Product.objects.get(id=int(data["pID"]))
    amount = int(data["amount"])
    sale = Sale.objects.filter(user=user,status="Carrito").first()
    try:
        detail = SaleDetail.objects.get(product=product)
        detail.units += amount
        detail.save()
        #return Response(200)
    except SaleDetail.DoesNotExist:
        detail = SaleDetail.objects.create(sale=sale,product=product,units=amount,subtotal=product.price*amount)
        #return Response(-1)
    """
    return Response(status=status.HTTP_201_CREATED)

@csrf_exempt
@api_view(['GET'])
def getCartItemAmount(request,uID):
    user = User.objects.get(id=uID)
    return Response(SaleDetail.objects.filter(sale=Sale.objects.filter(user=user,status="Carrito").first()).count())