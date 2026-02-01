from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Product, Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from cart.forms import CartAddProductForm
from django.db.models import Q


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
    
    # Фильтр по категории
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Фильтр по цене
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    if price_min:
        products = products.filter(price__gte=price_min)
    if price_max:
        products = products.filter(price__lte=price_max)
    
    # Фильтр по скидке
    has_discount = request.GET.get('discount')
    if has_discount:
        products = products.filter(discount__gt=0)
    
    # Сортировка
    sort = request.GET.get('sort', 'name')
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'newest':
        products = products.order_by('-created')
    else:
        products = products.order_by('name')
    
    # Пагинация
    paginator = Paginator(products, 10)
    current_page = paginator.page(int(page))
    
    context = {
        'category': category,
        'categories': categories,
        'products': current_page,
        'slug_url': category_slug,
        'price_min': price_min or '',
        'price_max': price_max or '',
        'has_discount': has_discount,
        'current_sort': sort,
    }
    return render(request, 'main/product/list.html', context)

def page_not_found(request, exception):
    return render(request, 'main/validators/404.html', status=404)


def server_error(request):
    return render(request, 'main/validators/500.html', status=500)

# Поиск 
def search_books(request):
    query = request.GET.get('q', '')
    results = []
    min_lenth = 3 
    
    if query and len(query) >= min_lenth:
        results = Product.objects.filter(
            Q(name__icontains=query) |
            Q(category__name__icontains=query) |
            Q(description__icontains=query),
            available=True
        ).distinct()

    context = {
        'results': results,
        'query': query,
        'min_length': min_lenth
    }

    return render(request, 'main/product/search.html', context)