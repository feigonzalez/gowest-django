from django.shortcuts import render, redirect
from .models import *

# Create your views here.
def index(request):
    context={"categories":Category.objects.all(),
        "galleries":[]}
    for category in context["categories"]:
        context["galleries"].append(Product.objects.filter(category=category))
    return render(request, 'core/index.html',context)

def adminIndex(request):
    #if user.role != admin:
    #   return redirect('index')
    return render(request, 'core/adminWelcome.html')

def adminAccount(request):
    #if user.role != admin:
    #   return redirect('index')
    return render(request, 'core/adminAccount.html')

def adminProducts(request):
    #if user.role != admin:
    #   return redirect('index')
    context={"products":Product.objects.all(),
        "categories":Category.objects.all()}
    return render(request, 'core/adminProducts.html',context)

def adminCategories(request):
    #if user.role != admin:
    #   return redirect('index')
    context={"categories":Category.objects.all()}
    return render(request, 'core/adminCategories.html',context)

def adminClients(request):
    #if user.role != admin:
    #   return redirect('index')
    context={"clients":User.objects.filter(role=1)}
    return render(request, 'core/adminclients.html',context)

def adminSales(request):
    #if user.role != admin:
    #   return redirect('index')
    #if request.GET["adminSalesSearchQuery"]:
    #    sales=Sale.objects.filter()
    #else:
    sales=Sale.objects.all()
    
    context={"sales":sales}
    return render(request, 'core/adminSales.html',context)

def adminAdministrators(request):
    #if user.role != admin:
    #   return redirect('index')
    return render(request, 'core/adminAdministrators.html')

def signup(request):
    context={"districts":,Districts.objects.all(),
        "secQuestions":SecQuestions.objects.all()}
    return render(request, 'core/signup.html', context)

def clientAccount(request):
    #if user.role != client:
    #   return redirect('index')
    context={"categories":Category.objects.all()}
    return render(request, 'core/clientAccount.html',context)

def clientSales(request):
    #if user.role != client:
    #   return redirect('index')
    context={"categories":Category.objects.all()
#        "sales":Sales.objects.filter(user=SESSION["user"])}
        }
    return render(request, 'core/clientSales.html',context)

def clientFoundation(request):
    #if user.role != client:
    #   return redirect('index')
    context={"categories":Category.objects.all()}
    #determine, with an API call, whether the client is already subscribed
    #if so, add its details to the context
    return render(request, 'core/clientFoundation.html',context)

def cart(request):
    context={"categories":Category.objects.all()
        #"addresses":Address.objects.filter(user=SESSION["user"])},
        #"details":SaleDetail.objects.filter(user=SESSION["user"])
        }
    return render(request, 'core/cart.html',context)

def category(request, id):
    context={"categories":Category.objects.all(),
        "galleries":[Product.objects.filter(category=Category.objects.get(id=id))]}
    return render(request, 'core/category.html',context)

def product(request, id):
    context={"categories":Category.objects.all(),
        "product":Product.objects.get(id=id)}
    return render(request, 'core/product.html',context)

def recoverPass(request):
    return render(request, 'core/recoverPass.html')

#Input and user actions processing

def processLogin(request):
    #get data from user, depending on provided mail
    #compare provided pass with retrieved password
    #if passes match
    #   set SESSION["user"] to corresponding user
    #else
    return redirect('index')

def processSignup(request):
    name = request.POST["clientName"]
    surname = request.POST["clientSurname"]
    rut = request.POST["clientRut"]
    mail = request.POST["clientMail"]
    phone = request.POST["clientPhone"]
    password = request.POST["clientPassword"]
    question = SecQuestion.objects.get(id=request.POST["clientSecQuestion"])
    answer = request.POST["clientSecAnswer"]
    street = request.POST["clientAddressStreet"]
    number = request.POST["clientAddressNumber"]
    postalCode = request.POST["clientAddressPostalCode"]
    district = Districts.objects.get(id = request.POST["clientAddressDistrict"])
    #insert new client-type user into db
    user = User.objects.create(rut=rut,name=name,surname=surname,mail=mail,phone=phone,
        password=password,role=Role.objects.get(role=1),secQuestion=secQuestion,
        secAnswer=secAnswer)
    #insert client's new address into db
    Address.objects.create(street=street, number=number, postalCode=postalCode,
        user=user, district=district)
    return redirect('index')

def validatePassRecovery(request):
    rut = request.POST["recoverRut"]
    secAnswer = request.POST["recoverSecAnswer"]
    if User.objects.get(rut = rut).secAnswer = secAnswer:
        #user is valid. log in and redirect to index
        return redirect('index')
    else
        #wrong secanswer. stay in recoverPass and give feedback
        context={"wrongAnswer":True}
        return render(request,'core/recoverPass.html',context)

def processClientUpdateChanges(request, type):
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

def confirmSaleAction(request):
    action=request.POST["action"]
    target=request.POST["target"]
    #if SESSION["user"].role == 2: #if admin
    #   return redirect('adminSales')
    #else:
    return redirect('clientSales')

def confirmDeletion(request):
    target=request.POST["target"]
    origin=request.POST["origin"]
    return redirect(origin)

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
    Category.objects.create(name=name)
    return redirect('adminCategories')