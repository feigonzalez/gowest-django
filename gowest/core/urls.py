from django.contrib import admin
from django.urls import path, include
from .views import *
#from .views import index, adminIndex, signup, account, cart, category, product, recoverPass, adminAccount

urlpatterns = [
    path('', index, name='index'),
    path('admin/', adminIndex, name='adminIndex'),
    path('admin/account', adminAccount, name='adminAccount'),
    path('admin/products', adminProducts, name='adminProducts'),
    path('admin/categories', adminCategories, name='adminCategories'),
    path('admin/clients', adminClients, name='adminClients'),
    path('admin/sales', adminSales, name='adminSales'),
    path('admin/administrators', adminAdministrators, name='adminAdministrators'),
    path('signup/', signup, name='signup'),
    path('account/', clientAccount, name='clientAccount'),
    path('account/sales', clientSales, name='clientSales'),
    path('account/foundation', clientFoundation, name='clientFoundation'),
    path('cart/', cart, name='cart'),
    path('category/<int:id>', category, name='category'),
    path('product/<int:id>', product, name='product'),
    path('recoverPass/', recoverPass, name='recoverPass'),
    path('createCategory/', createCategory, name = 'createCategory'),
    path('createProduct/', createProduct, name = 'createProduct'),
    path('createAdministrator/', createAdministrator, name = 'createAdministrator'),
    path('createAddress/', createAddress, name = 'createAddress'),
    path('processSignup/', processSignup, name='processSignup'),
    path('processLogin/', processLogin, name='processLogin'),
    path('processClientAccountChanges/<str:type>', processClientAccountChanges, name='processClientAccountChanges'),
    path('processAdminAccountChanges/<str:type>', processAdminAccountChanges, name='processAdminAccountChanges'),
    path('validatePassRecovery/', validatePassRecovery, name='validatePassRecovery'),
    path('logOff/', logOff, name='logOff'),
    path('checkout/', checkout, name='checkout'),
    path('confirmSaleAction/', confirmSaleAction, name='confirmsSaleAction'),
    path('confirmDeletion/', confirmDeletion, name='confirmDeletion'),
    path('confirmSaleAction/', confirmSaleAction, name='confirmSaleAction'),
    path('searchClientSales/', searchClientSales, name='searchClientSales'),
    path('subscribeToFoundation/', subscribeToFoundation, name='subscribeToFoundation'),
]