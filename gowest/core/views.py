from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User as DjUser
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate,login, logout
from django.http import JsonResponse
from datetime import date
from .models import *

#used to give DANGER-level messages the "alert-danger" bootstrap class
MESSAGE_DANGER=80

# Create your views here.
def index(request):
    if 'uRole' in request.session and request.session["uRole"] == 'admin':
        return redirect('adminIndex')
    context={"categories":Category.objects.filter(is_active=1),
        "galleries":[]}
    if "loginStatus" in request.session:
        context["loginStatus"]="FAIL"
        context["loginUser"]=request.session["loginUser"]
        del request.session["loginStatus"]
        del request.session["loginUser"]
    for category in context["categories"]:
        context["galleries"].append({})
        context["galleries"][-1]["id"]=category.id
        context["galleries"][-1]["name"]=category.name
        context["galleries"][-1]["products"]=Product.objects.filter(category=category,is_active=1)
    return render(request, 'core/index.html',context)

def adminIndex(request):
    if 'uRole' not in request.session or request.session["uRole"] != 'admin':
       return redirect('index')
    return render(request, 'core/adminWelcome.html')

def adminAccount(request):
    if 'uRole' not in request.session or request.session["uRole"] != 'admin':
       return redirect('index')
    context={"user":User.objects.get(id=request.session["uID"]),
        "secQuestions":SecQuestion.objects.all()}
    return render(request, 'core/adminAccount.html',context)

def adminProducts(request):
    if 'uRole' not in request.session or request.session["uRole"] != 'admin':
       return redirect('index')
    if "adminProductsSearchQuery" in request.GET:
        products = Product.objects.filter(name__icontains=request.GET["adminProductsSearchQuery"])
    else:
        products = Product.objects.all()
    context={"products":products,
        "categories":Category.objects.all()}
    return render(request, 'core/adminProducts.html',context)

def adminCategories(request):
    if 'uRole' not in request.session or request.session["uRole"] != 'admin':
       return redirect('index')
    if "adminCategoriesSearchQuery" in request.GET:
        categories = Category.objects.filter(name__icontains=request.GET["adminCategoriesSearchQuery"])
    else:
        categories = Category.objects.all()
    context={"categories":categories}
    return render(request, 'core/adminCategories.html',context)

def adminClients(request):
    if 'uRole' not in request.session or request.session["uRole"] != 'admin':
       return redirect('index')
    context={"clients":User.objects.filter(role=1)}
    return render(request, 'core/adminclients.html',context)

def adminSales(request):
    if 'uRole' not in request.session or request.session["uRole"] != 'admin':
       return redirect('index')
    #TODO: filter sales if search query given
    sales=Sale.objects.all()
    context={"sales":sales}
    return render(request, 'core/adminSales.html',context)

def adminAdministrators(request):
    if 'uRole' not in request.session or request.session["uRole"] != 'admin':
       return redirect('index')
    context={"admins":User.objects.filter(role=Role.objects.get(id=2))}
    return render(request, 'core/adminAdministrators.html',context)

def signup(request):
    context={"districts":District.objects.all(),
        "secQuestions":SecQuestion.objects.all()}
    return render(request, 'core/signup.html', context)

def clientAccount(request):
    if 'uRole' not in request.session or request.session["uRole"] != "client":
       return redirect('index')
    user=User.objects.get(id=request.session["uID"])
    context={"districts":District.objects.all(),
        "secQuestions":SecQuestion.objects.all(),
        "user":user,
        "addresses":Address.objects.filter(user=user,is_active=1)}
    return render(request, 'core/clientAccount.html',context)

def clientSales(request):
    if 'uRole' not in request.session or request.session["uRole"] != "client":
       return redirect('index')
    context={"categories":Category.objects.filter(is_active=1),
        "sales":Sale.objects.filter(user=User.objects.get(id=request.session["uID"]))}
    return render(request, 'core/clientSales.html',context)

def clientFoundation(request):
    if 'uRole' not in request.session or request.session["uRole"] != "client":
       return redirect('index')
    context={"categories":Category.objects.filter(is_active=1)}
    #determine, with an API call, whether the client is already subscribed
    #if so, add its details to the context
    return render(request, 'core/clientFoundation.html',context)

def cart(request):
    if 'uRole' in request.session and request.session["uRole"] == 'client':
        sale = Sale.objects.get(user=User.objects.get(id=request.session["uID"]), status='Carrito')
        context={"categories":Category.objects.all(),
            "addresses":Address.objects.filter(user=User.objects.get(id=request.session["uID"]),is_active=1),
            "details":SaleDetail.objects.filter(sale=sale),
            "cartTotal":sale.total}
        return render(request, 'core/cart.html',context)
    else:
        return render(request, 'core/cart.html')

def category(request, id):
    thisCategory = Category.objects.get(id=id)
    context={"categories":Category.objects.filter(is_active=1),
        "galleries":[{"id":id, "name":thisCategory.name, "products":Product.objects.filter(category=thisCategory,is_active=1)}]}
    return render(request, 'core/category.html',context)

def product(request, id):
    context={"categories":Category.objects.filter(is_active=1),
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
        #TODO alert, password is wrong
        request.session["loginStatus"]="FAIL"
        request.session["loginUser"]=mail
        return redirect('index')
    try:
        user = User.objects.get(mail=mail)
    #except UserDoesNotExist: alert, redirect
    except User.DoesNotExist:
        #TODO alert
        #message user doesnt exist: show login modal with "invalid" text
        request.session["loginStatus"]="FAIL"
        request.session["loginUser"]=mail
        return redirect('index')
    authUser = authenticate(username=mail,password=rawPass)
    if authUser is not None and user is not None:
        login(request, authUser)
        request.session["uID"]=user.id
        request.session["uName"]=user.name
        request.session["uSurname"]=user.surname
        if user.role.name == "administrator":
            request.session["uRole"]="admin"
            return redirect('adminIndex')
        else:
            request.session["uRole"]="client"
            #get the number of items on the user's cart
            totalItems=0
            for saleDetail in SaleDetail.objects.filter(sale=Sale.objects.filter(user=user,status="Carrito").first()):
                totalItems += saleDetail.units
            request.session["cartItems"] = totalItems
            return redirect('index')
    #this return should never be reached
    return redirect('index')

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
    valid = True
    context={"districts":District.objects.all()}
    if User.objects.filter(rut=rut).count()>0:
        #context["message"]="user with rut exists"
        #TODO: change to use messages instead
        context["RUT"]=True
        valid = False
    if User.objects.filter(mail=mail).count()>0:
        #context["message"]="user with email exists"
        #TODO: change to use messages instead
        context["MAIL"]=True
        valid = False
    if not valid:
        return render(request, 'core/signup.html', context)
    #insert new client-type user into db
    user = User.objects.create(rut=rut,name=name,surname=surname,mail=mail,phone=phone,
        password=password,role=Role.objects.get(id=1),secQuestion=secQuestion,
        secAnswer=secAnswer)
    #insert client's new address into db
    address = Address.objects.create(streetName=streetName, streetNumber=streetNumber, postalCode=postalCode,
        user=user, district=district)
    #create an empty "cart" sale for the client
    Sale.objects.create(user=user,address=address,status="Carrito",total=0,saleDate=date.today(),subscribed=0)
    
    djUser = DjUser.objects.create_user(username=mail, email=mail, password=rawPass)
    djUser.is_staff=False
    djUser.save()
    
    login(request, djUser)
    request.session["uID"]=user.id
    request.session["uName"]=user.name
    request.session["uSurname"]=user.surname
    request.session["uRole"]="client"
    request.session["cartItems"] = 0

    return redirect('index')

def processAdminAccountChanges(request, type):
    #TODO
    user = User.objects.get(id=request.session["uID"])
    djuser = DjUser.objects.get(email=user.mail)
    if type == "data":
        #update the user's name, surname, phone, and mail
        name=request.POST["adminName"]
        surname=request.POST["adminSurname"]
        phone=request.POST["adminPhone"]
        user.name=name
        user.surname=surname
        user.phone=phone
        user.save()
        request.session["uName"]=name
        request.session["uSurname"]=surname
        messages.success(request, "Datos actualizados", extra_tags="board")
    if type == "password":
        valid = False
        password = request.POST["adminPassword"]
        passwordConfirm = request.POST["adminPasswordConfirm"]
        if request.session["recoverPass"]:
            valid = True
            del request.session["recoverPass"]
        else:
            oldPass = request.POST["adminOldPassword"]
            valid = check_password(oldPass, djuser.password)
        if valid:
            user.password=make_password(password)
            user.save()
            djuser.set_password(password)
            djuser.save()
            messages.success(request, "Contraseña actualizada", extra_tags="board")
        else:
            messages.error(request, "Su contraseña actual no es correcta", extra_tags="board")
        pass
    if type == "secQuestion":
        if user.secAnswer != request.POST["adminOldSecAnswer"]:
            messages.add_message(request, MESSAGE_DANGER, "Respuesta de seguridad incorrecta", extra_tags="board")
            return redirect('adminAccount')
        user.secQuestion = SecQuestion.objects.get(id=request.POST["adminSecQuestion"])
        user.secAnswer = request.POST["adminSecAnswer"]
        user.save()
        messages.success(request, "Datos de recuperación actualizados", extra_tags="board")
        pass
    return redirect('adminAccount')

def processClientAccountChanges(request, type):
    user = User.objects.get(id=request.session["uID"])
    djuser = DjUser.objects.get(email=user.mail)
    if type == "data":
        name=request.POST["updateClientName"]
        surname=request.POST["updateClientSurname"]
        phone=request.POST["updateClientPhone"]
        user.name=name
        user.surname=surname
        user.phone=phone
        user.save()
        request.session["uName"]=name
        request.session["uSurname"]=surname
        messages.success(request, "Datos actualizados", extra_tags="board")
    if type == "password":
        valid = False
        password = request.POST["updateClientPassword"]
        passwordConfirm = request.POST["updateClientPasswordConfirm"]
        if request.session["recoverPass"]:
            valid = True
            del request.session["recoverPass"]
        else:
            oldPass = request.POST["updateClientOldPassword"]
            valid = check_password(oldPass, djuser.password)
        if valid:
            user.password=make_password(password)
            user.save()
            djuser.set_password(password)
            djuser.save()
            messages.success(request, "Contraseña actualizada", extra_tags="board")
        else:
            messages.error(request, "Su contraseña actual no es correcta", extra_tags="board")
    if type == "secQuestion":
        #update the user's security question and answer
        if user.secAnswer != request.POST["updateClientOldSecAnswer"]:
            messages.add_message(request, MESSAGE_DANGER, "Respuesta de seguridad incorrecta", extra_tags="board")
            return redirect('clientAccount')
        user.secQuestion = SecQuestion.objects.get(id=request.POST["updateClientSecQuestion"])
        user.secAnswer = request.POST["updateClientSecAnswer"]
        user.save()
        messages.success(request, "Datos de recuperación actualizados", extra_tags="board")
    return redirect('clientAccount')

def checkout(request):
    doneSale = Sale.objects.filter(user=User.objects.get(id=request.session["uID"]),status="Carrito").first()
    doneSale.status="Pagada"
    doneSale.saleDate=date.today()
    doneSale.address=Address.objects.get(id=int(request.POST["cartAddress"]))
    doneSale.save()
    Sale.objects.create(user=User.objects.get(id=request.session["uID"]),
        address=Address.objects.filter(user=User.objects.get(id=request.session["uID"])).first(),
        status="Carrito",total=0,saleDate=date.today(),subscribed=0)
    request.session["cartItems"]=0
    return redirect('index')

def validatePassRecovery(request):
    #TODO
    mail = request.POST["recoverMail"]
    secAnswer = request.POST["recoverSecAnswer"]
    try:
        user = User.objects.get(mail = mail)
    except User.DoesNotExist:
        #message user doesnt exist: show login modal with "invalid" text
        return redirect('index')
        pass
    if user.secAnswer == secAnswer:
        #TODO
        #try: get user from djUser table
        try:
            djUser=DjUser.objects.get(username=user.mail)
        #except UserDoesNotExist: alert, redirect
        except DjUser.DoesNotExist:
            #TODO alert
            return redirect('index')
        if djUser is not None and user is not None:
            login(request, djUser)
            request.session["uID"]=user.id
            request.session["uName"]=user.name
            request.session["uSurname"]=user.surname
            request.session["recoverPass"]=True
            if user.role.id == 2:
                request.session["uRole"]="admin"
                return redirect('adminAccount')
            else:
                request.session["uRole"]="client"
                return redirect('clientAccount')
    else:
        #wrong secanswer. stay in recoverPass and give feedback
        context={"wrongAnswer":True,"mail":mail}
        return render(request,'core/recoverPass.html',context)

def confirmSaleAction(request):
    #TODO
    action=request.POST["action"]
    target=request.POST["target"]
    if request.session["uRole"] == 2: #if admin
       return redirect('adminSales')
    else:
        return redirect('clientSales')

def confirmActivation(request):
    target=request.POST["target"]
    origin=request.POST["origin"]
    pass

def confirmDeletion(request):
    #TODO
    target=request.POST["target"]
    origin=request.POST["origin"]
    if origin == "adminCategories":
        item = Category.objects.get(id=int(target))
        item.is_active=0
        item.save()
        messages.success(request,"Categoría desactivada", extra_tags="board")
    elif origin == "clientAccount":
        item = Address.objects.get(id=int(target))
        item.is_active=0
        item.save()
        messages.success(request,"Dirección eliminada", extra_tags="board")
    elif origin == "adminProducts":
        item = Product.objects.get(id=int(target))
        item.is_active=0
        item.save()
        messages.success(request,"Producto desactivado", extra_tags="board")
    elif origin == "adminCategories":
        item = Category.objects.get(id=int(target))
        item.is_active=0
        item.save()
        messages.success(request,"Categoría desactivada", extra_tags="board")
    return redirect(origin)

def confirmActivation(request):
    #TODO
    target=request.POST["target"]
    origin=request.POST["origin"]
    if origin == "adminCategories":
        item = Category.objects.get(id=int(target))
        item.is_active=1
        item.save()
        messages.success(request,"Categoría activada", extra_tags="board")
    elif origin == "adminProducts":
        item = Product.objects.get(id=int(target))
        item.is_active=1
        item.save()
        messages.success(request,"Producto activado", extra_tags="board")
    elif origin == "adminCategories":
        item = Category.objects.get(id=int(target))
        item.is_active=1
        item.save()
        messages.success(request,"Categoría activada", extra_tags="board")
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

def postProduct(request):
    name = request.POST["productName"]
    description = request.POST["productDescription"]
    price = request.POST["productPrice"]
    stock = request.POST["productStock"]
    category = Category.objects.get(id = int(request.POST["productCategory"]))
    #The form validation checks for the existence of an image preview in the form.
    #It can be empty and pass validation if the product already has an image assigned,
    #but it was not updated.
    image=None
    if "productImage" in request.FILES:
        image = request.FILES["productImage"]
    update=request.POST["update"]
    if update=="true":
        product = Product.objects.get(id=int(request.POST["pID"]))
        product.name=name
        product.description=description
        product.price=price
        product.stock=stock
        product.category=category
        if image is not None:
            product.image=image
        product.save()
        messages.success(request,"Producto actualizado", extra_tags="board")
    else:
        Product.objects.create(name=name, description=description, price=price, stock=stock, image=image, category=category)
    return redirect('adminProducts')

def createCategory(request):
    name = request.POST['categoryName']
    id = request.POST['categoryId']
    if request.POST['update']=="true":
        category=Category.objects.get(id=id)
        category.name=name;
        category.save()
    else:
        Category.objects.create(name=name)
    return redirect('adminCategories')

def postAddress(request):
    streetName=request.POST["addressFormStreet"]
    streetNumber=request.POST["addressFormNumber"]
    postalCode=request.POST["addressFormPostalCode"]
    district=District.objects.get(id=int(request.POST["addressFormDistrict"]))
    update=request.POST["addressFormUpdate"]
    if update=="true":  #update an existing address
        address=Address.objects.get(id=int(request.POST["addressFormId"]))
        address.streetName=streetName
        address.streetNumber=streetNumber
        address.postalCode=postalCode
        address.district=district
        address.save()
        messages.success(request,"Dirección actualizada", extra_tags="board")
    else:
        Address.objects.create(user=User.objects.get(id=request.session["uID"]),streetName=streetName, streetNumber=streetNumber, postalCode=postalCode,
            district=district)
        messages.success(request,"Dirección añadida", extra_tags="board")
    return redirect('clientAccount')

def createAdministrator(request):
    return redirect('adminAdministrators')