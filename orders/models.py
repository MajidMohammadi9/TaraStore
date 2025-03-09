from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from accounts.models import Customer
from products.models import Product


class Order(models.Model):
    ORDER_STATUS_PAID = 'p'
    ORDER_STATUS_UNPAID = 'u'
    ORDER_STATUS_CANCELED = 'c'
    ORDER_STATUS = [
        (ORDER_STATUS_PAID,'Paid'),
        (ORDER_STATUS_UNPAID,'Unpaid'),
        (ORDER_STATUS_CANCELED,'Canceled'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='orders')
    order_note=models.CharField(verbose_name=_('Note'),max_length=700,blank=True)
    authority=models.CharField(max_length=255, blank=True, verbose_name=_('Authority'))
    ref_id=models.CharField(max_length=255, blank=True, verbose_name=_('Reference ID'))
    data=models.TextField(blank=True)
    status = models.CharField(max_length=1, choices=ORDER_STATUS, default=ORDER_STATUS_UNPAID)
    datetime_created=models.DateTimeField(verbose_name=_('Date Time Created'),auto_now_add=True)
    datetime_modified=models.DateTimeField(verbose_name=_('Date Time Modified'),auto_now=True)

    def __str__(self):
        return f'Order id={self.id}'
    
    def get_total_price(self):
        return sum(item.quantity*item.price for item in self.items.all())
    

class OrderItem(models.Model):
    order=models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items',verbose_name=_('Order'))
    product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items',verbose_name=_('Product'))
    quantity=models.PositiveIntegerField(verbose_name=_('Quantity'),default=1)
    price=models.PositiveIntegerField(verbose_name=_('Price'))

    def __str__(self):
        return f'Order Item {self.id}: {self.product} x {self.quantity}'
