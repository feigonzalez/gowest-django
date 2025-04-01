from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User as DjUser
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login, logout
from django.http import JsonResponse
from django.db.models import Q, Value as V
from django.db.models.functions import Concat
from .models import *
from requests import JSONDecodeError

from inspect import currentframe, getframeinfo

from datetime import date, datetime
from math import floor
import requests

#prints in console the function and source line number where the function is called
def debug(m):
    f=getframeinfo(currentframe().f_back)
    print(">["+f.function+"@"+str(f.lineno)+"] "+m)

#used to give DANGER-level messages the "alert-danger" bootstrap class
MESSAGE_DANGER=80

# Create your views here.
def index(request):
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

@login_required
def adminIndex(request):
    if not loggedIn(request,role="admin"):
        return redirect('index')
    context={"categories":Category.objects.filter(is_active=1)}
    return render(request, 'core/adminWelcome.html',context)

@login_required
def adminAccount(request):
    if not loggedIn(request,role="admin"):
       return redirect('index')
    context={"user":User.objects.get(id=request.session["uID"]),
        "secQuestions":SecQuestion.objects.all(),
        "categories":Category.objects.filter(is_active=1)}
    return render(request, 'core/adminAccount.html',context)

@login_required
def adminProducts(request):
    if not loggedIn(request,role="admin"):
       return redirect('index')
    if "adminProductsSearchQuery" in request.GET:
        products = Product.objects.filter(name__icontains=request.GET["adminProductsSearchQuery"])
    else:
        products = Product.objects.all()
    context={"products":products,
        "categories":Category.objects.filter(is_active=1),
        "adminCategories":Category.objects.all()}
    # session's "editElement" is a boolean that indicates whether the page should show
    # a specific element to be edited. the element is identified by "editTarget"
    if "editElement" in request.session and "editTarget" in request.session:
        context["editElement"]=True
        context["editTarget"]=request.session["editTarget"]
        del request.session["editElement"]
        del request.session["editTarget"]
    return render(request, 'core/adminProducts.html',context)

@login_required
def adminCategories(request):
    if not loggedIn(request,role="admin"):
       return redirect('index')
    if "adminCategoriesSearchQuery" in request.GET:
        adminCategories = Category.objects.filter(name__icontains=request.GET["adminCategoriesSearchQuery"])
    else:
        adminCategories = Category.objects.all()
    context={"categories":Category.objects.filter(is_active=1),
            "adminCategories":adminCategories}
    if "editElement" in request.session and "editTarget" in request.session:
        context["editElement"]=True
        context["editTarget"]=request.session["editTarget"]
        del request.session["editElement"]
        del request.session["editTarget"]
    return render(request, 'core/adminCategories.html',context)

@login_required
def adminClients(request):
    if not loggedIn(request,role="admin"):
       return redirect('index')
    if "adminClientsSearchQuery" in request.GET:
        q=request.GET["adminClientsSearchQuery"]
        clients = User.objects.annotate(fullname=Concat("name",V(" "),
            "surname")).filter(Q(role=1) & (Q(fullname__icontains=q) | Q(mail__icontains=q) | Q(rut__icontains=q) | Q(phone__icontains=q)))
    else:
        clients = User.objects.filter(role=1)
    """try:
        subsJson=requests.get("http://dintdt.c1.biz/aup/getAllSubs.php").json()
        subs={}
        for sub in subsJson:
            rut=subsJson[sub]["client_rut"]
            subs[rut]={"start_date":subsJson[sub]["start_date"],"end_date":subsJson[sub]["end_date"]}
        for client in clients:
            #if client exists in subs database, and their subscription is still valid
            if client.rut in subs and datetime.strptime(subs[client.rut]["end_date"],"%Y-%m-%d").date()>=date.today():
                client.subscribed=True
                client.subExpiry=subs[client.rut]["end_date"]
            else:
                client.subscribed=False
    except JSONDecodeError: #error in request
        messages.add_message(request,MESSAGE_DANGER,"Error de conexión. No se pudo obtener los datos de suscripciones.",extra_tags="board")
        for client in clients:
            client.subscribed=False"""
    context={"clients":clients,
            "categories":Category.objects.filter(is_active=1)}
    return render(request, 'core/adminclients.html',context)

@login_required
def adminSales(request):
    if not loggedIn(request,role="admin"):
       return redirect('index')
    if "adminSalesSearchQuery" in request.GET:
        q=request.GET["adminSalesSearchQuery"]
        users=User.objects.annotate(fullname=Concat("name",V(" "),"surname")).filter(Q(role=1) & Q(fullname__icontains=q))
        sales=Sale.objects.none()
        for user in users:
            sales|=Sale.objects.filter(Q(user=user))
        sales|=Sale.objects.filter(Q(status__icontains=q))
    else:
        sales=Sale.objects.all()
    context={"sales":sales,
            "categories":Category.objects.filter(is_active=1)}
    return render(request, 'core/adminSales.html',context)

@login_required
def adminAdministrators(request):
    if not loggedIn(request,role="admin"):
       return redirect('index')
    if "adminAdministratorsSearchQuery" in request.GET:
        q=request.GET["adminAdministratorsSearchQuery"]
        admins = User.objects.annotate(fullname=Concat("name",V(" "),
            "surname")).filter(Q(role=2) & (Q(fullname__icontains=q) | Q(mail__icontains=q) | Q(rut__icontains=q) | Q(phone__icontains=q)))
    else:
        admins = User.objects.filter(role=2)
    context={"admins":admins,
            "categories":Category.objects.filter(is_active=1)}
    return render(request, 'core/adminAdministrators.html',context)

def signup(request):
    context={"districts":District.objects.all(),
        "secQuestions":SecQuestion.objects.all(),
        "categories":Category.objects.filter(is_active=1)}
    return render(request, 'core/signup.html', context)

@login_required
def clientAccount(request):
    if not loggedIn(request,role="client"):
       return redirect('index')
    user=User.objects.get(id=request.session["uID"])
    context={"districts":District.objects.all(),
        "secQuestions":SecQuestion.objects.all(),
        "user":user,
        "addresses":Address.objects.filter(user=user,is_active=1),
        "categories":Category.objects.filter(is_active=1)}
    return render(request, 'core/clientAccount.html',context)

@login_required
def clientSales(request):
    if not loggedIn(request,role="client"):
       return redirect('index')
    context={"categories":Category.objects.filter(is_active=1),
        "sales":Sale.objects.filter(user=User.objects.get(id=request.session["uID"]))}
    return render(request, 'core/clientSales.html',context)

@login_required
def clientFoundation(request):
    if not loggedIn(request,role="client"):
       return redirect('index')
    context={"categories":Category.objects.filter(is_active=1)}
    #determine, with an API call, whether the client is already subscribed
    #if so, add its details to the context
    """sub=getSubscription(request)
    if sub is None:
        messages.add_message(request,MESSAGE_DANGER,"Error de conexión. No se pudo obtener datos de suscripción.",extra_tags="board")
    elif sub["subscribed"]:
        context["subEndDate"]=sub["end_date"]"""
    return render(request, 'core/clientFoundation.html',context)

def cart(request):
    if loggedIn(request,role="admin"):
       return redirect('index')
    elif loggedIn(request,role="client"):
        user=User.objects.get(id=request.session["uID"])
        sale = Sale.objects.get(user=user, status='Carrito')
        context={"categories":Category.objects.filter(is_active=1),
            "addresses":Address.objects.filter(user=user,is_active=1),
            "details":SaleDetail.objects.filter(sale=sale),
            "cartTotal":sale.total}
        """if getSubscription(request)["subscribed"]:
            context["discount"]=-floor(context["cartTotal"]*0.1)
            context["cartTotal"]+=context["discount"]"""
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
    context={"categories":Category.objects.filter(is_active=1)}
    return render(request, 'core/recoverPass.html',context)

#Input and user actions processing

def processLogin(request):
    debug("Logging in...")
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
        debug("Django user does not exist")
        return redirect('index')
    valid = check_password(rawPass, djUser.password)
    if not valid:
        #TODO alert, password is wrong
        debug("Wrong login password")
        request.session["loginStatus"]="FAIL"
        request.session["loginUser"]=mail
        return redirect('index')
    try:
        user = User.objects.get(mail=mail)
    #except UserDoesNotExist: alert, redirect
    except User.DoesNotExist:
        #TODO alert
        debug("Database user does not exist")
        request.session["loginStatus"]="FAIL"
        request.session["loginUser"]=mail
        return redirect('index')
    authUser = authenticate(username=mail,password=rawPass)
    if authUser is not None and user is not None:
        login(request, authUser)
        debug("User ["+mail+"] logged in")
        request.session["uID"]=user.id
        request.session["uName"]=user.name
        request.session["uSurname"]=user.surname
        if user.role.name == "administrator":
            request.session["uRole"]="admin"
        else:
            request.session["uRole"]="client"
            #get the number of items on the user's cart
            totalItems=0
            for saleDetail in SaleDetail.objects.filter(sale=Sale.objects.filter(user=user,status="Carrito").first()):
                totalItems += saleDetail.units
            request.session["cartItems"] = totalItems
    return redirect('index')

def logOff(request):
    debug("Logging off...")
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
        context["RUT"]=True
        valid = False
    if User.objects.filter(mail=mail).count()>0:
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

@login_required
def processAdminAccountChanges(request, type):
    if not loggedIn(request,role="admin"):
        messages.add_message(request,MESSAGE_DANGER,"Debe ingresar como administrador para cambiar sus datos.", extra_tags="board")
        return redirect('index')
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

@login_required
def processClientAccountChanges(request, type):
    if not loggedIn(request,role="client"):
        messages.add_message(request,MESSAGE_DANGER,"Debe ingresar como cliente para cambiar sus datos.", extra_tags="board")
        return redirect('index')
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

@login_required
def checkout(request):
    if not loggedIn(request,role="client"):
        messages.add_message(request,MESSAGE_DANGER,"Debe ingresar como cliente para pagar una compra.", extra_tags="board")
        return redirect('index')
    doneSale = Sale.objects.filter(user=User.objects.get(id=request.session["uID"]),status="Carrito").first()
    doneSale.status="Pagada"
    doneSale.saleDate=date.today()
    doneSale.address=Address.objects.get(id=int(request.POST["cartAddress"]))
    doneSale.save()
    """if getSubscription(request)["subscribed"]:
        subscribed=1
    else:
        subscribed=0"""
    subscribed=0
    Sale.objects.create(user=User.objects.get(id=request.session["uID"]),
        address=Address.objects.filter(user=User.objects.get(id=request.session["uID"])).first(),
        status="Carrito",total=0,saleDate=date.today(),subscribed=subscribed)
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

@login_required
def confirmSaleAction(request):
    #TODO
    action=request.POST["action"]
    target=request.POST["target"]
    sale=Sale.objects.get(id=int(target))
    if action=="shipment":
        if not loggedIn(request,role="admin"):
            messages.add_message(request,MESSAGE_DANGER,"No tiene permisos para marcar esta venta como Despachada.", extra_tags="board")
            return redirect('index')
        sale.status="Despachada"
        sale.save()
    elif action=="reception":
        if not loggedIn(request,role="client"):
            messages.add_message(request,MESSAGE_DANGER,"No tiene permisos para marcar esta compra como Completada.", extra_tags="board")
            return redirect('index')
        sale.status="Completada"
        sale.deliveryDate=date.today()
        sale.save()
    if request.session["uRole"] == "admin": #if admin
       return redirect('adminSales')
    else:
        return redirect('clientSales')

@login_required
def confirmDeletion(request):
    #TODO
    target=request.POST["target"]
    origin=request.POST["origin"]
    if origin == "adminCategories":
        if not loggedIn(request,role="admin"):
            messages.add_message(request,MESSAGE_DANGER,"No tiene permisos para desactivar una categoría.", extra_tags="board")
            return redirect('index')
        try:
            item = Category.objects.get(id=int(target))
            item.is_active=0
            item.save()
            messages.success(request,"Categoría desactivada", extra_tags="board")
        except Category.DoesNotExist:
            messages.add_message(request,MESSAGE_DANGER,"ERROR: Categoría indicada no existe", extra_tags="board")
    elif origin == "clientAccount":
        if not loggedIn(request,role="client"):
            messages.add_message(request,MESSAGE_DANGER,"No tiene permisos para eliminar la dirección de un cliente.", extra_tags="board")
            return redirect('index')
        try:
            if Address.objects.filter(user=User.objects.get(id=int(request.session["uID"]))).count()==1:
                messages.add_message(request,MESSAGE_DANGER,"No puede eliminar su única dirección.", extra_tags="board")
            else:
                item = Address.objects.get(id=int(target))
                item.is_active=0
                item.save()
                messages.success(request,"Dirección eliminada", extra_tags="board")
        except Address.DoesNotExist:
            messages.add_message(request,MESSAGE_DANGER,"ERROR: Dirección indicada no existe", extra_tags="board")
    elif origin == "adminProducts":
        if not loggedIn(request,role="admin"):
            messages.add_message(request,MESSAGE_DANGER,"No tiene permisos para desactivar un producto.", extra_tags="board")
            return redirect('index')
        try:
            item = Product.objects.get(id=int(target))
            item.is_active=0
            item.save()
            messages.success(request,"Producto desactivado", extra_tags="board")
        except Product.DoesNotExist:
            messages.add_message(request,MESSAGE_DANGER,"ERROR: Producto indicado no existe", extra_tags="board")
    elif origin == "adminAdministrators":
        if not loggedIn(request,role="admin"):
            messages.add_message(request,MESSAGE_DANGER,"No tiene permisos para eliminar un administrador.", extra_tags="board")
            return redirect('index')
        valid=True
        try:
            item = User.objects.get(id=int(target))
            if item.role.id != 2:
                messages.add_message(request,MESSAGE_DANGER,"Usuario indicado no es administrador", extra_tags="board")
                valid = False
            if item.id == int(request.session["uID"]):
                messages.add_message(request,MESSAGE_DANGER,"No puede eliminarse a sí mismo/a", extra_tags="board")
                valid = False
            if valid:
                item.delete()
                djUser=DjUser.objects.get(email=item.mail)
                djUser.delete()
                messages.success(request,"Administrador eliminado", extra_tags="board")
        except Category.DoesNotExist:
            messages.add_message(request,MESSAGE_DANGER,"ERROR: Administrador indicado no existe", extra_tags="board")
    return redirect(origin)

@login_required
def confirmActivation(request):
    if not loggedIn(request,role="admin"):
        messages.add_message(request,MESSAGE_DANGER,"No tiene permisos para activar elementos.", extra_tags="board")
        return redirect('index')
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
    return redirect(origin)

@login_required
def subscribeToFoundation(request):
    if not loggedIn(request,role="client"):
        messages.add_message(request,MESSAGE_DANGER,"Debe ingresar como cliente para suscribirse.", extra_tags="board")
        return redirect('index')
    try:
        post=requests.post("http://dintdt.c1.biz/aup/postSub.php",{"rut":User.objects.get(id=int(request.session["uID"])).rut}).json()
        if post["status"]=="GOOD":
            request.session["subscribed"]=True
        else:
            messages.add_message(request,MESSAGE_DANGER,"No se pudo realizar la suscripción.",extra_tags="board")
    except JSONDecodeError:
        messages.add_message(request,MESSAGE_DANGER,"Error de conexión. No se pudo realizar la suscripción.",extra_tags="board")
    return redirect('clientFoundation')

#database manipulation

def getProductData(request, id):
    p = Product.objects.get(id=id)
    return JsonResponse({"id":p.id,"name":p.name,"image":p.image.url,"description":p.description,
        "stock":p.stock,"price":p.price,"category":p.category.id})

@login_required
def postProduct(request):
    if not loggedIn(request,role="admin"):
        messages.add_message(request,MESSAGE_DANGER,"No tiene permisos para crear un producto.", extra_tags="board")
        return redirect('index')
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

@login_required
def createCategory(request):
    if not loggedIn(request,role="admin"):
        messages.add_message(request,MESSAGE_DANGER,"No tiene permisos para crear una categoría.", extra_tags="board")
        return redirect('index')
    name = request.POST['categoryName']
    id = request.POST['categoryId']
    if request.POST['update']=="true":
        category=Category.objects.get(id=id)
        category.name=name;
        category.save()
    else:
        Category.objects.create(name=name)
    return redirect('adminCategories')

@login_required
def postAddress(request):
    if not loggedIn(request,role="client"):
        messages.add_message(request,MESSAGE_DANGER,"Debe ingresar como cliente para registrar una dirección.", extra_tags="board")
        return redirect('index')
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

@login_required
def createAdministrator(request):
    if not loggedIn(request,role="admin"):
        messages.add_message(request,MESSAGE_DANGER,"No tiene permisos para crear un administrador.", extra_tags="board")
        return redirect('index')
    mail=request.POST["adminFormNewMail"]
    rut=request.POST["adminFormNewRUT"]
    valid=True
    if User.objects.filter(rut=rut).count()>0:
        messages.add_message(request,MESSAGE_DANGER,"Administrador no creado: Usuario con RUT ingresado ya existe.",extra_tags="board")
        valid=False
    if User.objects.filter(mail=mail).count()>0:
        messages.add_message(request,MESSAGE_DANGER,"Administrador no creado: Usuario con correo ingresado ya existe.",extra_tags="board")
        valid=False
    if not valid:
        return redirect('adminAdministrators')
    name=request.POST["adminFormNewName"]
    surname=request.POST["adminFormNewSurname"]
    phone=request.POST["adminFormNewPhone"]
    
    rawPass = name+surname+"!"+rut
    password=make_password(rawPass)
    
    secQuestion = SecQuestion.objects.get(id=1)
    secAnswer = "0"
    
    #insert new admin-type user into db
    user = User.objects.create(rut=rut,name=name,surname=surname,mail=mail,phone=phone,
        password=password,role=Role.objects.get(id=2),secQuestion=secQuestion,
        secAnswer=secAnswer)
    
    djUser = DjUser.objects.create_user(username=mail, email=mail, password=rawPass)
    djUser.is_staff=True
    djUser.save()
    
    messages.success(request,"Administrador creado (contraseña: \""+rawPass+"\")",extra_tags="board")
    return redirect('adminAdministrators')

@login_required
def editProduct(request,id):
    if not loggedIn(request,role="admin"):
        return redirect('index')
    request.session["editElement"]=True
    request.session["editTarget"]=id
    return redirect('adminProducts')

@login_required
def editCategory(request,id):
    if not loggedIn(request,role="admin"):
        return redirect('index')
    request.session["editElement"]=True
    request.session["editTarget"]=id
    return redirect('adminCategories')

def getSubscription(request):
    try:
        result = requests.get("http://dintdt.c1.biz/aup/getSub.php",{"rut":User.objects.get(id=int(request.session["uID"])).rut}).json()
        return result
    except JSONDecodeError:
        return None

#def closeSession(request):
#    logout(request)
#    return redirect('index')

def loggedIn(request,id=None,role=None):
    if "uID" not in request.session:
        return False
    if id is not None and int(request.session["uID"])!=int(id):
        return False
    if role is not None and ("uRole" not in request.session or request.session["uRole"]!=role):
        return False
    return True