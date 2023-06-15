from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User as DjUser
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate,login, logout
from django.http import JsonResponse
from .models import *

# Create your views here.
def index(request):
    context={"categories":Category.objects.all(),
        "galleries":[]}
    for category in context["categories"]:
        context["galleries"].append({})
        context["galleries"][-1]["id"]=category.id
        context["galleries"][-1]["name"]=category.name
        context["galleries"][-1]["products"]=Product.objects.filter(category=category)
    return render(request, 'core/index.html',context)

def adminIndex(request):
    if request.session["uRole"] != 'admin':
       return redirect('index')
    return render(request, 'core/adminWelcome.html')

def adminAccount(request):
    if request.session["uRole"] != 'admin':
       return redirect('index')
    context={"user":User.objects.get(id=request.session["uID"]),
        "secQuestions":SecQuestion.objects.all()}
    return render(request, 'core/adminAccount.html',context)

def adminProducts(request):
    if request.session["uRole"] != 'admin':
       return redirect('index')
    context={"products":Product.objects.all(),
        "categories":Category.objects.all()}
    return render(request, 'core/adminProducts.html',context)

def adminCategories(request):
    if request.session["uRole"] != 'admin':
       return redirect('index')
    context={"categories":Category.objects.all()}
    return render(request, 'core/adminCategories.html',context)

def adminClients(request):
    if request.session["uRole"] != 'admin':
       return redirect('index')
    context={"clients":User.objects.filter(role=1)}
    return render(request, 'core/adminclients.html',context)

def adminSales(request):
    if request.session["uRole"] != 'admin':
       return redirect('index')
    #if request.GET["adminSalesSearchQuery"]:
    #    sales=Sale.objects.filter()
    #else:
    sales=Sale.objects.all()
    
    context={"sales":sales}
    return render(request, 'core/adminSales.html',context)

def adminAdministrators(request):
    if request.session["uRole"] != 'admin':
       return redirect('index')
    context={"admins":User.objects.filter(role=Role.objects.get(id=2))}
    return render(request, 'core/adminAdministrators.html',context)

def signup(request):
    context={"districts":District.objects.all(),
        "secQuestions":SecQuestion.objects.all()}
    return render(request, 'core/signup.html', context)

def clientAccount(request):
    print("["+str(request.session["uID"])+"]")
    if request.session["uRole"] != "client":
       return redirect('index')
    user=User.objects.get(id=request.session["uID"])
    context={"categories":Category.objects.all(),
        "secQuestions":SecQuestion.objects.all(),
        "user":user,
        "addresses":Address.objects.filter(user=user)}
    return render(request, 'core/clientAccount.html',context)

def clientSales(request):
    if request.session["uRole"] != 'client':
       return redirect('index')
    context={"categories":Category.objects.all(),
        "sales":Sale.objects.filter(user=User.objects.get(id=request.session["uID"]))}
    return render(request, 'core/clientSales.html',context)

def clientFoundation(request):
    #if user.role != client:
    #   return redirect('index')
    context={"categories":Category.objects.all()}
    #determine, with an API call, whether the client is already subscribed
    #if so, add its details to the context
    return render(request, 'core/clientFoundation.html',context)

def cart(request):
    if "uID" in request.session:
        sale = Sale.objects.get(user=User.objects.get(id=request.session["uID"]), status='Carrito')
        context={"categories":Category.objects.all(),
            "addresses":Address.objects.filter(user=User.objects.get(id=request.session["uID"])),
            "details":SaleDetail.objects.filter(sale=sale),
            "cartTotal":sale.total}
        return render(request, 'core/cart.html',context)
    else:
        return render(request, 'core/cart.html')

def category(request, id):
    thisCategory = Category.objects.get(id=id)
    context={"categories":Category.objects.all(),
        "galleries":[{"id":id, "name":thisCategory.name, "products":Product.objects.filter(category=thisCategory)}]}
    return render(request, 'core/category.html',context)

def product(request, id):
    context={"categories":Category.objects.all(),
        "product":Product.objects.get(id=id)}
    return render(request, 'core/product.html',context)

def recoverPass(request):
    return render(request, 'core/recoverPass.html')

#Input and user actions processing

def processLogin(request):
    #TODO
    #get data from user, depending on provided mail
    mail=request.POST["mail"]
    rawPass=request.POST["password"]
    #try: get user from djUser table
    try:
        djUser=DjUser.objects.get(username=mail)
    #except UserDoesNotExist: alert, redirect
    except DjUser.DoesNotExist:
        #TODO alert
        return redirect('index')
    valid = check_password(rawPass, djUser.password)
    if not valid:
        #TODO alert
        return redirect('index')
    try:
        user = User.objects.get(mail=mail)
    #except UserDoesNotExist: alert, redirect
    except User.DoesNotExist:
        #TODO alert
        #message user doesnt exist: show login modal with "invalid" text
        return redirect('index')
    authUser = authenticate(username=mail,password=rawPass)
    if authUser is not None and user is not None:
        print("logged as "+user.name)
        print("with role "+str(user.role.name))
        login(request, authUser)
        request.session["uID"]=user.id
        request.session["uName"]=user.name
        request.session["uSurname"]=user.surname
        if user.role.name == "administrator":
            request.session["uRole"]="admin"
            return redirect('adminIndex')
        else:
            request.session["uRole"]="client"
            return redirect('index')
    #return redirect('index')

def logOff(request):
    logout(request)
    return redirect('index')

def processSignup(request):
    name = request.POST["clientName"]
    surname = request.POST["clientSurname"]
    rut = request.POST["clientRut"]
    mail = request.POST["clientMail"]
    phone = request.POST["clientPhone"]
    rawPass = request.POST["clientPassword"]
    password=make_password(rawPass)
    secQuestion = SecQuestion.objects.get(id=request.POST["clientSecQuestion"])
    secAnswer = request.POST["clientSecAnswer"]
    streetName = request.POST["clientAddressStreet"]
    streetNumber = request.POST["clientAddressNumber"]
    postalCode = request.POST["clientAddressPostalCode"]
    district = District.objects.get(id = request.POST["clientAddressDistrict"])
    #insert new client-type user into db
    user = User.objects.create(rut=rut,name=name,surname=surname,mail=mail,phone=phone,
        password=password,role=Role.objects.get(id=1),secQuestion=secQuestion,
        secAnswer=secAnswer)
    #insert client's new address into db
    Address.objects.create(streetName=streetName, streetNumber=streetNumber, postalCode=postalCode,
        user=user, district=district)
    
    djUser = DjUser.objects.create_user(username=mail, email=mail, password=rawPass)
    djUser.is_staff=False
    djUser.save()

    return redirect('index')

def processAdminAccountChanges(request, type):
    #TODO
    if type == "data":
        #update the user's name, surname, phone, and mail
        pass
    if type == "password":
        #update the user's password
        pass
    if type == "secQuestion":
        #update the user's security question and answer
        pass
    return redirect('adminAccount')

def processClientAccountChanges(request, type):
    #TODO
    if type == "data":
        #update the user's name, surname, phone, and mail
        pass
    if type == "password":
        #update the user's password
        pass
    if type == "secQuestion":
        #update the user's security question and answer
        pass
    return redirect('clientAccount')

def checkout(request):
    #TODO
    return redirect('index')

def validatePassRecovery(request):
    #TODO
    rut = request.POST["recoverRut"]
    secAnswer = request.POST["recoverSecAnswer"]
    if User.objects.get(rut = rut).secAnswer == secAnswer:
        #user is valid. log in and redirect to index
        return redirect('index')
    else:
        #wrong secanswer. stay in recoverPass and give feedback
        context={"wrongAnswer":True}
        return render(request,'core/recoverPass.html',context)

def confirmSaleAction(request):
    #TODO
    action=request.POST["action"]
    target=request.POST["target"]
    #if SESSION["user"].role == 2: #if admin
    #   return redirect('adminSales')
    #else:
    return redirect('clientSales')

def confirmDeletion(request):
    #TODO
    target=request.POST["target"]
    origin=request.POST["origin"]
    if origin == "adminCategories":
        item = Category.objects.get(id=int(target))
        item.delete()
    return redirect(origin)

def subscribeToFoundation(request):
    #TODO
    return redirect('clientFoundation')

#User-side searches

def searchClientSales(request):
    return render('clientSales')

#database manipulation

def getProductData(request, id):
    p = Product.objects.get(id=id)
    return JsonResponse({"id":p.id,"name":p.name,"image":p.image.url,"description":p.description,
        "stock":p.stock,"price":p.price,"category":p.category.id})

def createProduct(request):
    name = request.POST["productName"]
    description = request.POST["productDescription"]
    price = request.POST["productPrice"]
    stock = request.POST["productStock"]
    image = request.FILES["productImage"]
    category = Category.objects.get(id = request.POST["productCategory"])
    Product.objects.create(name=name, description=description, price=price, stock=stock, image=image, category=category)
    return redirect('adminProducts')

def createCategory(request):
    name = request.POST['categoryName']
    if request.POST['update']=="true":
        category=Category.objects.get(id)
    Category.objects.create(name=name)
    return redirect('adminCategories')

def createAddress(request):
    return redirect('clientAccount')

def createAdministrator(request):
    return redirect('adminAdministrators')

#DB data preparation

def prepareUsers(request):
    User.objects.create(rut='10.000.000-0',name='William',surname='Hartnell',mail='whart@mail.com',phone='+123456789',
        password=make_password('pass'),role=Role.objects.get(id=1),secQuestion=SecQuestion.objects.get(id=4),
        secAnswer='13')
    djUser = DjUser.objects.create_user(username='whart@mail.com', email='whart@mail.com', password='pass')
    djUser.is_staff=False
    djUser.save()
    User.objects.create(rut='11.000.000-0',name='Patrick',surname='Troughton',mail='ptrou@mail.com',phone='+234567891',
        password=make_password('pass'),role=Role.objects.get(id=1),secQuestion=SecQuestion.objects.get(id=4),
        secAnswer='12')
    djUser = DjUser.objects.create_user(username='ptrou@mail.com', email='ptrou@mail.com', password='pass')
    djUser.is_staff=False
    djUser.save()
    User.objects.create(rut='12.000.000-0',name='Jon',surname='Pertwee',mail='jpert@mail.com',phone='+345678912',
        password=make_password('pass'),role=Role.objects.get(id=1),secQuestion=SecQuestion.objects.get(id=4),
        secAnswer='11')
    djUser = DjUser.objects.create_user(username='jpert@mail.com', email='jpert@mail.com', password='pass')
    djUser.is_staff=False
    djUser.save()
    User.objects.create(rut='13.000.000-0',name='Tom',surname='Baker',mail='tbake@mail.com',phone='+456789123',
        password=make_password('pass'),role=Role.objects.get(id=1),secQuestion=SecQuestion.objects.get(id=4),
        secAnswer='10')
    djUser = DjUser.objects.create_user(username='tbake@mail.com', email='tbake@mail.com', password='pass')
    djUser.is_staff=False
    djUser.save()

    User.objects.create(rut='20.000.000-0',name='Alvis',surname='Claus',mail='aclau@mail.com',phone='+987654321',
        password=make_password('pass'),role=Role.objects.get(id=2),secQuestion=SecQuestion.objects.get(id=2),
        secAnswer='Kermit')
    djUser = DjUser.objects.create_user(username='aclau@mail.com', email='aclau@mail.com', password='pass')
    djUser.is_staff=True
    djUser.save()

    return redirect('index')