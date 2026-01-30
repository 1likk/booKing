from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Product, Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from cart.forms import CartAddProductForm

def popular_list(request):
    products = Product.objects.filter(available=True)[:3]

    return render(request, 
                  'main/index/index.html',
                  {'products': products})

def product_detail(request, slug):
    product = get_object_or_404(Product,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm
    
    return render(request, 'main/product/detail.html',
                  {'product': product,
                  'cart_product_form': cart_product_form})

def product_list(request, category_slug=None):
    page = request.GET.get('page', 1)
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    paginator = Paginator(products, 10)
    current_page = paginator.page(int(page))
    if category_slug:
        category = get_object_or_404(Category, 
                                     slug=category_slug)
        paginator = Paginator(products.filter(category=category), 10)
        current_page = paginator.page(int(page))
    return render(request, 'main/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': current_page, 
                   'slug_url': category_slug})

def page_not_found(request, exception):
    return render(request, 'main/validators/404.html', status=404)


def server_error(request):
    return render(request, 'main/validators/500.html', status=500)