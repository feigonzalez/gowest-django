from django.db import models

# Create your models here.
class District(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    
    def __str__(self) -> str:
        return self.name

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)

    def __str__(self) -> str:
        return self.name

class Role(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)

    def __str__(self) -> str:
        return self.name

class SecQuestion(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=128)

    def __str__(self) -> str:
        return self.question

class User(models.Model):
    id = models.AutoField(primary_key=True)
    rut = models.CharField(max_length=16)
    name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    mail = models.CharField(max_length=128)
    phone = models.CharField(max_length=16,blank=True,null=True)
    password = models.CharField(max_length=128) #stores the hashed pass? length of hashed pass?
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    secQuestion = models.ForeignKey(SecQuestion, on_delete=models.CASCADE)
    secAnswer = models.CharField(max_length=64)

    def __str__(self) -> str:
        return self.name+" "+self.surname

class Address(models.Model):
    id = models.AutoField(primary_key=True)
    streetName = models.CharField(max_length=64)
    streetNumber = models.CharField(max_length=16)
    postalCode = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    district = models.ForeignKey(District,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.streetName+" "+self.streetNumber

class Sale(models.Model):
    id = models.AutoField(primary_key=True)
    saleDate = models.DateField()
    deliveryDate = models.DateField(blank=True,null=True)
    status = models.CharField(max_length=16)
    total = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    subscribed = models.IntegerField()

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    description = models.TextField()
    image = models.ImageField(upload_to="products")
    price = models.IntegerField()
    stock = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

class SaleDetail(models.Model):
    id = models.AutoField(primary_key=True)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    units = models.IntegerField()
    subtotal = models.IntegerField()
