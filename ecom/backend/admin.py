from django.contrib import admin

# Register your models here.
from .models import Brand, Product, UserPermission, MenuList,Category,Product

admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(UserPermission)
admin.site.register(MenuList)
admin.site.register(Category)

