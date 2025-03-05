from django.contrib import admin

from .models import Order,OrderItem


class OrderItemInline(admin.TabularInline):
    model=OrderItem
    fields=['order', 'product', 'quantity', 'price',]
    extra=0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=['customer', 'datetime_created', 'status']
    list_editable=['status']
    inlines=[OrderItemInline,]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display=['order', 'product', 'quantity', 'price',]