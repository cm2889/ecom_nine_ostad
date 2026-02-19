from django.contrib import admin
from django.urls import path
from. import views


urlpatterns = [

    path('dashboard/', views.ecom_dashboard, name='dashboard'),
    path('brand-list/', views.brand, name='brand'),
    path('add-brand/', views.add_brand, name='add_new_brand'),

    path('category-list/', views.category_list, name='category'),
    path('product-list/', views.products_list, name='products'),
    path('add-product/', views.add_product, name='add_product'),
    path('', views.home, name='home'),

    #Porducts information
    path('products/', views.product_web_list, name='product_web_list'),
    path('products/<slug:product_slug>/', views.products_details, name='products_details'),

    
     # Authentication
    path('login/', views.login_view, name='user_login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='user_logout'),
    path('request-otp/', views.request_otp_view, name='request_otp'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),

    
    #ajax

    path('add-or-update-cart/', views.add_or_update_cart, name='add_or_update_cart'),

]