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
@api_view(['GET'])
def addToCart(request):
    #data = JSONParser.parse(request)
    user = User.objects.get(id=request.session["uID"])
    product = Product.objects.get(id=int(request.GET["pID"]))
    amount = int(request.GET["amount"])
    sale = Sale.objects.filter(user=user,status="Carrito").first()
    try:
        detail = SaleDetail.objects.get(product=product)
        detail.units += amount
        detail.subtotal += amount*product.price
        detail.save()
        recalculateCartTotalInternal(request.session["uID"])
        #return Response(200)
    except SaleDetail.DoesNotExist:
        detail = SaleDetail.objects.create(sale=sale,product=product,units=amount,subtotal=product.price*amount)
        recalculateCartTotalInternal(request.session["uID"])
        #return Response(-1)
    return Response(status=status.HTTP_201_CREATED)

@csrf_exempt
@api_view(['GET'])
def setToCart(request):
    #data = JSONParser.parse(request)
    user = User.objects.get(id=request.session["uID"])
    product = Product.objects.get(id=int(request.GET["pID"]))
    amount = int(request.GET["amount"])
    sale = Sale.objects.filter(user=user,status="Carrito").first()
    try:
        detail = SaleDetail.objects.get(product=product)
        detail.units = amount
        detail.subtotal = amount*product.price
        detail.save()
        recalculateCartTotalInternal(request.session["uID"])
        #return Response(200)
    except SaleDetail.DoesNotExist:
        detail = SaleDetail.objects.create(sale=sale,product=product,units=amount,subtotal=product.price*amount)
        recalculateCartTotalInternal(request.session["uID"])
        #return Response(-1)
    return Response(status=status.HTTP_201_CREATED)

@csrf_exempt
@api_view(['GET'])
def removeFromCart(request,dID):
    saleDetail=SaleDetail.objects.get(id=int(dID))
    saleDetail.delete()
    recalculateCartTotalInternal(request.session["uID"])
    return Response(status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['GET'])
def getCartItemAmount(request):
    user = User.objects.get(id=request.session["uID"])
    totalItems=0
    for saleDetail in SaleDetail.objects.filter(sale=Sale.objects.filter(user=user,status="Carrito").first()):
        totalItems += saleDetail.units
    request.session["cartItems"] = totalItems
    return Response(totalItems)

@csrf_exempt
@api_view(['GET'])
def recalculateCartTotal(request):
    recalculateCartTotalInternal(request.session["uID"])

def recalculateCartTotalInternal(uID):
    sale=Sale.objects.get(user=User.objects.get(id=uID),status="Carrito")
    total = 0
    for saleDetail in SaleDetail.objects.filter(sale=sale):
        total += saleDetail.subtotal
    sale.total=total
    sale.save()