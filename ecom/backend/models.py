from django.db import models
import datetime

from django.contrib.auth.models import User

import datetime
from django.utils import timezone

# Create your models here.

#For permission 

# Create your models here.
class MenuList(models.Model):
    module_name        = models.CharField(max_length=100, db_index=True)
    menu_name          = models.CharField(max_length=100, unique=True, db_index=True)
    menu_url           = models.CharField(max_length=250, unique=True)
    menu_icon          = models.CharField(max_length=250, blank=True, null=True)
    parent_id          = models.IntegerField()
    is_main_menu       = models.BooleanField(default=False)
    is_sub_menu        = models.BooleanField(default=False)
    is_sub_child_menu  = models.BooleanField(default=False)
    created_at         = models.DateTimeField(auto_now_add=True)
    updated_at         = models.DateTimeField(blank=True, null=True)
    deleted_at         = models.DateTimeField(blank=True, null=True)
    created_by         = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active          = models.BooleanField(default=True)
    deleted            = models.BooleanField(default=False)

    class Meta:
        db_table = "menu_list"

    def __str__(self) -> str:
        return self.menu_name

class UserPermission(models.Model):
    user          = models.ForeignKey(User, on_delete=models.CASCADE, related_name="employee_user_for_permission") 
    menu          = models.ForeignKey(MenuList, on_delete=models.CASCADE, related_name="menu_for_permission") 
    can_view      = models.BooleanField(default=False)
    can_add       = models.BooleanField(default=False)
    can_update    = models.BooleanField(default=False)
    can_delete    = models.BooleanField(default=False)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    created_by    = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_by_user") 
    updated_by    = models.ForeignKey(User, on_delete=models.CASCADE, related_name="updated_by_user", blank=True, null=True) 
    deleted_by    = models.ForeignKey(User, on_delete=models.CASCADE, related_name="deleted_by_user", blank=True, null=True)
    is_active     = models.BooleanField(default=True)
    deleted       = models.BooleanField(default=False)

    class Meta:
        db_table = "user_permission"

    def __str__(self):
        return str(self.menu)
#permission ends here
class Brand (models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "brand"


class Category (models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "category"

class Product (models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    dimensions = models.CharField(max_length=100, blank=True, null=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    rating = models.FloatField(default=0)
    delivery_day_min = models.IntegerField(default=0)
    delivery_day_max = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_reviews = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    avl_quantity = models.IntegerField(default=0)
    image=models.ImageField(upload_to='product_images/', blank=True, null=True)

    def __str__(self):
        return self.name
    class Meta:
        db_table = "products"

class ProductImage (models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image_url = models.ImageField(upload_to='product_images/')
    position = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Image for {self.product.name}"
    class Meta:
        db_table = "product_images"
        ordering = ['position']

class ProductCategory (models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} in {self.category.name}"
    
    class Meta:
        db_table = "product_category"
        

class Attribute (models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "attribute"
class AttributeValue (models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"
    
    class Meta:
        db_table = "attribute_value"
class ProductAttributeValue (models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute_value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} - {self.attribute_value}"
    
    class Meta:
        db_table = "product_attribute_value"

class Membership (models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "membership"


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
    class Meta:
        db_table = "customer"
class Review (models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review for {self.product.name} by {self.customer.user.username}"
    
    class Meta:
        db_table = "review"
class Cart (models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.customer.user.username}"
    
    class Meta:
        db_table = "cart"



class discountCoupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code

    class Meta:
        db_table = "discount_coupons"

class OrderCart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,related_name='order_cart')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    is_order= models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_amount(self):
        return_value=float(self.quantity) * float(self.product.price)
        return return_value
    
    class Meta:
        db_table = 'order_cart'

    def __str__(self):
        return f"{self.customer} - {self.product.product_name} ({self.quantity})"
    
class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )

    order_number = models.CharField(max_length=100, blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    billing_address = models.CharField(max_length=255, blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    order_amount = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    shipping_charge = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    discount = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    coupon_discount = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    vat_amount = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    tax_amount = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    paid_amount = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    due_amount = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    grand_total = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.order_number)+" ("+str(self.customer)+" - "+str(self.created_at)+")"

    class Meta:
        db_table = 'orders'

    def save(self, *args, **kwargs):
        if not self.order_number:
            current_year = datetime.date.today().year
            current_month = datetime.date.today().month
            current_day = datetime.date.today().day
            current_customer_id = self.customer.id

            last_order = Order.objects.filter(order_number__startswith=f"{current_year}{current_month:02d}")

            increase_number = 1
            new_order_number = f"{current_year}{current_month:02d}{last_order.count() + increase_number:04d}{current_day:02d}{current_customer_id}"

            while Order.objects.filter(order_number=new_order_number).exists():
                increase_number += 1
                new_order_number = f"{current_year}{current_month:02d}{last_order.count() + increase_number:04d}{current_day:02d}{current_customer_id}"

            self.order_number = new_order_number

        super().save(*args, **kwargs)

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, related_name='order_details', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    unit_price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    is_discount = models.BooleanField(default=False)
    discount_price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.order.order_number)+" ("+str(self.product)+" - "+str(self.quantity)+")"

    class Meta:
        db_table = 'order_details'

class OnlinePaymentRequest(models.Model):
    order = models.ForeignKey(Order, related_name='order_payment_requests', on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    payment_status_list = [('Pending', 'Pending'), ('Paid', 'Paid'), ('Cancelled', 'Cancelled'), ('Failed', 'Failed')]
    payment_status = models.CharField(max_length=15, choices=payment_status_list, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_request_created_by')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "online_payment_request"

class OrderPayment(models.Model):
    order = models.ForeignKey(Order, related_name='order_payments', on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    transaction_id = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.order.order_number)+" ("+str(self.payment_method)+" - "+str(self.amount)+")"

    class Meta:
        db_table = 'order_payments'

#Email OTP Verification

class EmailOTP(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=60)

    def __str__(self):
        return f"{self.email} - {self.code}"
 