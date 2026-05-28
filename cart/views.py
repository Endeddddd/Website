from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django_ratelimit.decorators import ratelimit

from shop.models import Product
from .models import Cart, CartItem


def get_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return cart


# =========================
# CART PAGE
# =========================
@login_required
def cart_detail(request):
    cart = get_cart(request)

    return render(request, "cart/cart.html", {
        "cart": cart
    })


# =========================
# ADD TO CART (ANTI FLOOD)
# =========================
@ratelimit(key='ip', rate='30/m', block=True)
@login_required
def cart_add(request, product_id):

    cart = get_cart(request)
    product = get_object_or_404(Product, id=product_id)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        item.quantity += 1
        item.save()

    messages.success(request, "Товар добавлен в корзину")

    return redirect("cart_detail")


# =========================
# REMOVE ITEM
# =========================
@login_required
def cart_remove(request, item_id):

    item = get_object_or_404(CartItem, id=item_id)
    item.delete()

    messages.success(request, "Товар удалён из корзины")

    return redirect("cart_detail")


# =========================
# INCREASE QTY
# =========================
@login_required
def cart_increase(request, item_id):

    item = get_object_or_404(CartItem, id=item_id)

    item.quantity += 1
    item.save()

    messages.success(request, "Количество увеличено")

    return redirect("cart_detail")


# =========================
# DECREASE QTY
# =========================
@login_required
def cart_decrease(request, item_id):

    item = get_object_or_404(CartItem, id=item_id)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    messages.success(request, "Количество уменьшено")

    return redirect("cart_detail")