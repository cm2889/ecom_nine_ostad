from multiprocessing import context
from pyexpat.errors import messages
from urllib import request
from django.shortcuts import redirect, render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import authenticate, login, logout

from backend.models import Brand, Category, Customer, Product,ProductCategory,EmailOTP,OrderCart
from backend.common_func import checkUserPermission

from django.contrib.auth.models import User

from backend.utls import generate_otp

from django.http import JsonResponse
from django.contrib import messages
# Create your views here.


#For Pagination data


def paginate_data(request, page_num, data_list):
    items_per_page, max_pages = 10, 10
    paginator = Paginator(data_list, items_per_page)
    last_page_number = paginator.num_pages

    try:
        data_list = paginator.page(page_num)
    except PageNotAnInteger:
        data_list = paginator.page(1)
    except EmptyPage:
        data_list = paginator.page(paginator.num_pages)

    current_page = data_list.number
    start_page = max(current_page - int(max_pages / 2), 1)
    end_page = start_page + max_pages

    if end_page > last_page_number:
        end_page = last_page_number + 1
        start_page = max(end_page - max_pages, 1)

    paginator_list = range(start_page, end_page)

    return data_list, paginator_list, last_page_number

def ecom_dashboard(request):
      return render(request, 'home/home.html')


def brand(request):
            
            if not checkUserPermission(request, "can_view", "/backend/brand-list/"):
                return render(request,"403.html")
            
            brands = Brand.objects.filter(is_active=True).order_by('-id')
            page_number = request.GET.get('page', 1)
            brands, paginator_list, last_page_number = paginate_data(request, page_number, brands)

            context = {
                'paginator_list': paginator_list,
                'last_page_number': last_page_number,
                'brands': brands,
            }
            return render(request, 'brand/brand.html', context)
def add_brand(request):
    if not checkUserPermission(request, "can_add", "/backend/brand-list/"):
        return render(request,"403.html")
    
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Brand.objects.create(name=name)
            return redirect('brand')
        else:
            return render(request, 'brand/add_brand.html', {'error': 'Brand name cannot be empty.'})
    return render(request, 'brand/add_brand.html')


def category_list(request):
            
            if not checkUserPermission(request, "can_view", "/backend/category-list/"):
                return render(request,"403.html")
            
            categories = Category.objects.filter(is_active=True).order_by('-id')
            page_number = request.GET.get('page', 1)
            categories, paginator_list, last_page_number = paginate_data(request, page_number, categories)

            context = {
                'paginator_list': paginator_list,
                'last_page_number': last_page_number,
                'categories': categories,
            }
            return render(request, 'category/category.html', context)


def products_list(request):
     
    if not checkUserPermission(request, "can_view", "/backend/product-list/"):
            return render(request,"403.html")
     
    products = Product.objects.filter(is_active=True).order_by('-id')
    page_number = request.GET.get('page', 1)
    products, paginator_list, last_page_number = paginate_data(request, page_number, products)

    context = {
                'paginator_list': paginator_list,
                'last_page_number': last_page_number,
                'products': products,
            }
    return render(request, 'product/product.html', context)

def add_product(request):
    if not checkUserPermission(request, "can_add", "/backend/product-list/"):
        return render(request,"403.html")
    
    brands = Brand.objects.filter(is_active=True)
    categories = Category.objects.filter(is_active=True)

    if request.method == 'POST':
        name = request.POST.get('name')
        brand_id = request.POST.get('brand')
        category_ids = request.POST.getlist('categories')
        price = request.POST.get('price')

        # Debug: Log all POST data
        print("POST data:", request.POST)
        print("name:", name)
        print("brand_id:", brand_id)
        print("category_ids:", category_ids)
        print("price:", price)

        if name and price and category_ids:
            try:
                price = float(price)
                product = Product.objects.create(name=name, price=price,brand_id=brand_id if brand_id else None)
                
                for category_id in category_ids:
                    try:
                         if not ProductCategory.objects.filter(product=product, category_id=category_id).exists():
                            ProductCategory.objects.create(product=product, category_id=category_id)
                         
                    except ValueError:
                        print(f"Invalid category ID: {category_id}")
                        continue

                return redirect('products')
            except (ValueError, TypeError):
                return render(request, 'product/add_product.html', {'error': 'Invalid price format.', 'brands': brands, 'categories': categories})
        else:
            return render(request, 'product/add_product.html', {'error': 'All fields are required.', 'brands': brands, 'categories': categories})
    
    return render(request, 'product/add_product.html', {'brands': brands, 'categories': categories})


def home(request):
     
    categories = Category.objects.filter(is_active=True).order_by('-id')[:5]
    featured_products = Product.objects.filter(is_active=True, is_featured=True).order_by('-id')[:10]

    context = {
         'categories': categories,
         'featured_products': featured_products,}
    return render(request, 'website/home.html', context)

def product_web_list(request):
    products = Product.objects.filter(is_active=True).order_by('-id')
    context = {
        'products': products,
    }
    return render(request, 'website/product/list.html', context)

def products_details(request, product_slug):
    product = Product.objects.filter(slug=product_slug, is_active=True).first()
    if not product:
        return render(request, '404.html')
    
    if request.user.is_authenticated:
        
        
        product.save()

    context = {
        'product': product,
    }
    return render(request, 'website/product/details.html', context)


def login_view(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        password = request.POST['password']

        
        profile = Customer.objects.get(phone=phone)
        user = authenticate(request, username=profile.user.username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Logged in successfully!")

        next_url = request.GET.get('next')
        if next_url:
            next_url = next_url.strip()
        else:
            next_url = "home"
        return redirect(next_url)
    return render(request, 'website/user/login.html')
    
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        dob = request.POST['date_of_birth']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            return render(request, 'website/user/register.html', {'error': 'Username already taken'})
        
        user = User.objects.create_user(username=username, email=email, password=password)
        Customer.objects.create(user=user, phone=phone, date_of_birth=dob, is_active=False)

        generate_otp(email)

        return redirect(f'/backend/verify-otp/?email={email}')

    return render(request, 'website/user/register.html')

def user_logout(request):
    logout(request)
    return redirect('home')

def verify_otp_view(request):
    email = request.GET.get('email')

    if request.method == 'POST':
        otp = request.POST.get('otp')
        otp_obj = EmailOTP.objects.filter(email=email, code=otp).order_by('-created_at').first()

       

        if otp_obj and not otp_obj.is_expired():
            user = User.objects.filter(email=email).first()
            if not user:
                messages.error(request, "User not found. Please register first.")
                return redirect('register')
            customer = Customer.objects.filter(user=user).first()
            if customer:
                customer.is_active = True
                customer.save()
                messages.success(request, "OTP verified successfully. You can now log in.")
            else:
                messages.error(request, "Customer not found. Please contact support.")
            
            return redirect('home')
        else:
            messages.error(request, "Invalid or expired OTP.")

    return render(request, 'website/user/verify_otp.html', {'email': email})      
  
def request_otp_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        generate_otp(email)
        return redirect(f'/backend/verify-otp/?email={email}')
    

def add_or_update_cart(request):

    
    is_authenticated = request.user.is_authenticated
    
    
    if is_authenticated:
        if request.method == 'POST':
            
            customer=Customer.objects.filter(user=request.user).first()
            
            product_id = request.POST.get('product_id')
            quantity = int(request.POST.get('quantity', 0))

            try:
                isRemoved = False

                cart_item, created = OrderCart.objects.update_or_create(
                    customer=customer, product_id=product_id, is_order=False, is_active=True,
                    defaults={'quantity': quantity}
                )
                
                if not created:
                    if quantity <= 0:
                        cart_item.is_active = False
                        isRemoved = True

                    cart_item.quantity = quantity
                    cart_item.save()

                amount_summary = cart_amount_summary(request)

                cart_item_count = OrderCart.objects.filter(customer=customer, is_order=False, is_active=True).count()
                print(f"Cart Item Count: {cart_item_count}")

               

                response = {
                    'status': 'success',
                    'message': 'Cart updated successfully',
                    'is_authenticated': is_authenticated,
                    'isRemoved': isRemoved,
                    'item_price': cart_item.total_amount,
                    'cart_item_count': cart_item_count,
                    'amount_summary': amount_summary,
                }
                
                return JsonResponse(response)
            

            except OrderCart.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Cart item not found', 'is_authenticated': is_authenticated,})

    return JsonResponse({'status': 'error', 'message': 'Invalid request', 'is_authenticated': is_authenticated,}, status=400)


def cart_amount_summary(request):

    sub_total_amount = 0
    total_vat = 0
    total_discount = 0
    grand_total = 0

    if request.user.is_authenticated:
        customer= Customer.objects.filter(user=request.user).first()
        cart_items = OrderCart.objects.filter(customer=customer, is_active=True, is_order=False)
        for item in cart_items:
            sub_total_amount += item.total_amount
            #total_vat += (item.product.price * 0.15)
    grand_total = (sub_total_amount + total_vat) - total_discount 

    return {'sub_total_amount': sub_total_amount, 'total_vat': total_vat, 'total_discount': total_discount, 'grand_total': grand_total}
           

    
