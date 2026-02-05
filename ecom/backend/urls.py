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
    

    
]