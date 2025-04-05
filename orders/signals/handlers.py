from django.db.models.signals import post_delete
from django.dispatch import receiver
from orders.models import OrderItem, Order

# it deletes orders that have no order items
@receiver(post_delete, sender=OrderItem)
def delete_empty_order(sender, instance, **kwargs):
    order = instance.order
    if not order.items.exists():
        order.delete()
