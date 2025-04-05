from django.contrib import admin
from django.db.models import Prefetch
from django.db import connection
from .models import Order,OrderItem


class OrderItemInline(admin.TabularInline):
    model=OrderItem
    fields=['order','product', 'quantity', 'price',]
    extra=0
    # readonly_fields=['product']  # displaying the product name in order items instead of the products list

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('product')
    
    def get_readonly_fields(self, request, obj = None):
        if obj:
            return ['product']
        return []


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=['id', 'customer', 'datetime_created', 'status']
    list_editable=['status']
    inlines=[OrderItemInline,]
    exclude=['customer']  # Prevent displaying the customer field in Order Details.
    readonly_fields=['customer_name']  # displaying the customer name in order details instead of the customers list
    # list_select_related = ['customer', 'customer__user']
    fields = ['customer_name', 'order_note', 'authority','ref_id', 'data', 'status'] # Fields order in the admin form.

    def customer_name(self, obj):
        return obj.customer.full_name
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('customer__user')
    
    # To select the customer name when adding a new order
    # def get_readonly_fields(self, request, obj=None):
    #     if obj:
    #         return ['customer']
    #     return []
    
            
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display=['order', 'product', 'quantity', 'price',]