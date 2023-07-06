from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from core.models import *
from .serializers import *

#get-all-from-table methods

@csrf_exempt
@api_view(['GET'])
def getUsers(request):
    if "uRole" not in request.session or request.session["uRole"] != "admin":
        return Response(status=status.HTTP_403_FORBIDDEN)
    return Response(UserSerializer(User.objects.all(), many=True).data)

@csrf_exempt
@api_view(['GET'])
def getSales(request):
    if "uRole" not in request.session or request.session["uRole"] != "admin":
        return Response(status=status.HTTP_403_FORBIDDEN)
    return Response(SaleSerializer(Sale.objects.all(), many=True).data)

@csrf_exempt
@api_view(['GET'])
def getProducts(request):
    if "uRole" not in request.session or request.session["uRole"] != "admin":
        return Response(status=status.HTTP_403_FORBIDDEN)
    return Response(ProductSerializer(Product.objects.all(), many=True).data)

#get-by-id methods that require data from multiple tables

@csrf_exempt
@api_view(['GET'])
def getSaleDetails(request, id):
    if "uID" not in request.session or "uRole" not in request.session or request.session["uRole"]!="admin":
        return Response(status=status.HTTP_403_FORBIDDEN)
    sale = Sale.objects.get(id=id)
    saleJson = SaleSerializer(sale).data
    if request.session["uID"]==sale.user.id:
        del saleJson["user"]
    details = SaleDetail.objects.filter(sale=sale)
    detailsJson = []
    for d in details:
        p=Product.objects.get(id=d.product.id)
        newD={}
        newD["productName"]=p.name
        newD["productPrice"]=p.price
        newD["units"]=d.units
        newD["subtotal"]=d.subtotal
        detailsJson.append(newD)
    response={
        "sale":saleJson,
        "address":sale.address.streetName+" "+sale.address.streetNumber+", "+sale.address.district.name,
        "details":detailsJson
    }
    return Response(response)

@csrf_exempt
@api_view(['GET'])
def getAddress(request, id):
    if "uID" not in request.session or "uRole" not in request.session or request.session["uRole"]!="admin":
        return Response(status=status.HTTP_403_FORBIDDEN)
    address = Address.objects.get(id=id)
    addressJson = AddressSerializer(address).data
    addressJson["districtName"]=address.district.name
    if request.session["uID"]!=address.user.id and request.session["uRole"]!="admin":
        return Response(status=status.HTTP_403_FORBIDDEN)
    return Response(addressJson)

#get-by-id-from-table methods
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

#client-related methods
@csrf_exempt
@api_view(['GET'])
def getUserSQ(request, mail):
    if User.objects.filter(mail=mail).count()==0:
        return Response(False)
    else:
        return Response(User.objects.get(mail=mail).secQuestion.question)

@csrf_exempt
@api_view(['GET'])
def addToCart(request):
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
    if "uID" not in request.session:
        return Response(status=status.HTTP_403_FORBIDDEN)
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
    if "uID" not in request.session:
        return Response(status=status.HTTP_403_FORBIDDEN)
    return Response(UserSerializer(User.objects.all(), many=True).data)
    saleDetail=SaleDetail.objects.get(id=int(dID))
    saleDetail.delete()
    recalculateCartTotalInternal(request.session["uID"])
    return Response(status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['GET'])
def getCartItemAmount(request):
    if "uID" not in request.session:
        return Response(status=status.HTTP_403_FORBIDDEN)
    user = User.objects.get(id=request.session["uID"])
    totalItems=0
    for saleDetail in SaleDetail.objects.filter(sale=Sale.objects.filter(user=user,status="Carrito").first()):
        totalItems += saleDetail.units
    request.session["cartItems"] = totalItems
    return Response(totalItems)

@csrf_exempt
@api_view(['GET'])
def recalculateCartTotal(request):
    if "uID" not in request.session:
        return Response(status=status.HTTP_403_FORBIDDEN)
    recalculateCartTotalInternal(request.session["uID"])

def recalculateCartTotalInternal(uID):
    sale=Sale.objects.get(user=User.objects.get(id=uID),status="Carrito")
    total = 0
    for saleDetail in SaleDetail.objects.filter(sale=sale):
        total += saleDetail.subtotal
    sale.total=total
    sale.save()

#login-related methods
@csrf_exempt
@api_view(['GET'])
def isRutAvailable(request, rut):
    return Response(User.objects.filter(rut=rut).count() == 0)

@csrf_exempt
@api_view(['GET'])
def isMailAvailable(request, mail):
    return Response(User.objects.filter(mail=mail).count() == 0)

