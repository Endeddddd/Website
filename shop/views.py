from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.db.models import Q


def home(request):

    products = Product.objects.all()
    categories = Category.objects.all()

    return render(request, "shop/home.html", {
        "products": products,
        "categories": categories
    })


def product_detail(request, slug):

    product = get_object_or_404(Product, slug=slug)

    return render(request, "shop/product_detail.html", {
        "product": product
    })


def category_detail(request, slug):

    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()

    return render(request, "shop/category_detail.html", {
        "category": category,
        "products": products,
        "categories": categories
    })


def search(request):

    query = request.GET.get("q", "")
    products = Product.objects.all()

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(short_description__icontains=query)
        )

    categories = Category.objects.all()

    return render(request, "shop/search.html", {
        "products": products,
        "query": query,
        "categories": categories
    })