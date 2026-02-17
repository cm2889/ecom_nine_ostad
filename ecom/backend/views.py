from multiprocessing import context
from pyexpat.errors import messages
from urllib import request
from django.shortcuts import redirect, render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import authenticate, login, logout

from backend.models import Brand, Category, Product,ProductCategory
from backend.common_func import checkUserPermission
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

    context = {
        'product': product,
    }
    return render(request, 'website/product/details.html', context)