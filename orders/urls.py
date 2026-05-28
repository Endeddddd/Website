from django.urls import path
from .views import checkout, order_success, order_history

urlpatterns = [
    path("checkout/", checkout, name="checkout"),
    path("success/", order_success, name="order_success"),
    path("history/", order_history, name="order_history"),
]