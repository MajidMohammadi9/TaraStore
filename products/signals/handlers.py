from django.db.models.signals import pre_save, post_delete, pre_delete
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sessions.models import Session
from django.utils.timezone import now, timedelta

from products.models import Product
from orders.models import Order, OrderItem


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

# if a pruduct is deleted from database, it will also be removed from cart
def remove_product_from_cart(instance):
    # active_sessions = Session.objects.all()
    active_sessions = Session.objects.filter(expire_date__gte=now() - timedelta(days=1)) # filter for 24 hours
    for session in active_sessions:
        session_data = session.get_decoded()
        if 'cart' in session_data and str(instance.id) in session_data['cart']:
            del session_data['cart'][str(instance.id)]
            session.session_data = Session.objects.encode(session_data)
            session.save()

@receiver(pre_delete, sender=Product)
def remove_product_on_delete(sender, instance, **kwargs):
    remove_product_from_cart(instance)

@receiver(pre_save, sender=Product)
def remove_product_on_inactive(sender, instance, **kwargs):
    try:
        old_product = Product.objects.get(pk=instance.pk)
    except ObjectDoesNotExist:
        return
    
    if old_product.active and not instance.active:
        remove_product_from_cart(instance)

# If the inventory becomes zero, the value of active will be set to False, and if it becomes greater than zero, the value of active will be set to True.    
# @receiver(pre_save, sender=Product)
# def update_status(sender, instance, **kwargs):
#     instance.active = instance.inventory > 0
    # no need to save the instatance, because the signal is pre_save