from django.contrib import admin
from .models import Order, OrderItem, ShippingAddress


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "quantity", "price")


class ShippingAddressInline(admin.StackedInline):
    model = ShippingAddress
    extra = 0
    readonly_fields = ("address", "city", "postal_code", "phone")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at")
    list_filter = ("created_at", "user")
    search_fields = ("user__username",)

    inlines = [OrderItemInline, ShippingAddressInline]

    readonly_fields = ("user", "card_number", "created_at")

    def has_add_permission(self, request):
        return False