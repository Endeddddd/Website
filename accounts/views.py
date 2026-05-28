from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django_ratelimit.decorators import ratelimit

from .models import Profile
from orders.models import Order


# =========================
# LOGIN (с защитой от флуда)
# =========================
@ratelimit(key='ip', rate='5/m', block=True)
def login_view(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Вы вошли в аккаунт")
            return redirect("home")
        else:
            messages.error(request, "Неверный логин или пароль")

    return render(request, "accounts/login.html")


# =========================
# REGISTRATION
# =========================
def register_view(request):

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)
        messages.success(request, "Регистрация успешна!")
        return redirect("home")

    return render(request, "accounts/register.html")


# =========================
# LOGOUT (POST only)
# =========================
@require_POST
def logout_view(request):
    logout(request)
    messages.success(request, "Вы вышли из аккаунта")
    return redirect("home")


# =========================
# PROFILE
# =========================
@login_required
def profile_view(request):

    profile, created = Profile.objects.get_or_create(user=request.user)

    orders = Order.objects.filter(
        user=request.user
    ).order_by("-created_at")

    # 💵 total price in USD
    for order in orders:
        total = 0

        for item in order.items.all():
            total += item.price * item.quantity

        order.total_price_usd = round(total, 2)

    if request.method == "POST":
        if "avatar" in request.FILES:
            profile.avatar = request.FILES["avatar"]
            profile.save()

    return render(request, "accounts/profile.html", {
        "profile": profile,
        "orders": orders
    })