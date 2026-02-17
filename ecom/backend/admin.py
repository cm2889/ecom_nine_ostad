from django.contrib import admin

# Register your models here.
from .models import Brand, MenuList, Product, ProductCategory, UserPermission, MenuList,Category,Product,ProductImage

admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(UserPermission)
admin.site.register(MenuList)
admin.site.register(Category)
admin.site.register(ProductCategory)
admin.site.register(ProductImage)

