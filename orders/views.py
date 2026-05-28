from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django_ratelimit.decorators import ratelimit

from cart.models import Cart
from .models import Order, OrderItem, ShippingAddress
from .forms import CheckoutForm


# =========================
# CHECKOUT (ANTI FLOOD)
# =========================
@ratelimit(key='ip', rate='10/m', block=True)
@login_required
def checkout(request):

    # безопасная корзина
    cart, created = Cart.objects.get_or_create(user=request.user)

    # если пусто — назад
    if not cart.items.exists():
        messages.error(request, "Корзина пуста")
        return redirect("cart_detail")

    # считаем сумму
    total = sum(item.total_price() for item in cart.items.all())

    # POST
    if request.method == "POST":
        form = CheckoutForm(request.POST)

        if form.is_valid():

            # создаём заказ
            order = Order.objects.create(
                user=request.user,
                card_number=form.cleaned_data["card_number"]
            )

            # адрес доставки
            ShippingAddress.objects.create(
                user=request.user,
                order=order,
                address=form.cleaned_data["address"],
                city=form.cleaned_data["city"],
                postal_code=form.cleaned_data["postal_code"],
                phone=form.cleaned_data["phone"]
            )

            # товары
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

            # очистка корзины
            cart.items.all().delete()

            messages.success(request, "Заказ успешно оформлен!")
            return redirect("order_success")

    else:
        form = CheckoutForm()

    return render(request, "orders/checkout.html", {
        "form": form,
        "cart": cart,
        "total": total
    })


# =========================
# SUCCESS PAGE
# =========================
@login_required
def order_success(request):
    return render(request, "orders/success.html")


# =========================
# HISTORY
# =========================
@login_required
def order_history(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(request, "orders/history.html", {
        "orders": orders
    })