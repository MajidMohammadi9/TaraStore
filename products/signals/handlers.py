from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

from products.models import Product
from orders.models import Order, OrderItem

# @receiver(post_save, sender=Product)
# def update_order_items_price(sender, instance, update_fields, **kwargs):
#     print(f'update_fields={update_fields}')
#     if update_fields and 'unit_price' in update_fields:
#         old_price = sender.objects.get(pk=instance.pk).unit_price
#         if old_price != instance.unit_price:
#             orders = Order.objects.filter(status=Order.ORDER_STATUS_UNPAID)
#             for order in orders:
#                 items=OrderItem.objects.filter(order=order, product=instance)
#                 for item in items:
#                     item.price = instance.unit_price
#                     item.save()
# @receiver(post_save, sender=Product)
# def update_order_items_price(sender, instance, created, **kwargs):
#     print(f'created={created}')
#     if not created:
#         old_price = instance.__class__.objects.get(pk=instance.pk).unit_price
#         if old_price != instance.unit_price:
#             unpaid_orders = Order.objects.filter(status=Order.ORDER_STATUS_UNPAID)
#             for order in unpaid_orders:
#                 for item in order.items.all():
#                     if item.product == instance:
#                         item.price = instance.unit_price
#                         item.save()

@receiver(pre_save, sender=Product)
def update_order_items_price(sender, instance, **kwargs):
    try:       
        old_product = Product.objects.get(pk=instance.pk)
    except ObjectDoesNotExist:
        return  
    
    if old_product.unit_price != instance.unit_price:
        orders = Order.objects.filter(status=Order.ORDER_STATUS_UNPAID)

        for order in orders:
            items = OrderItem.objects.filter(order=order, product=instance)
            for item in items:
                item.price = instance.unit_price
                item.save()

