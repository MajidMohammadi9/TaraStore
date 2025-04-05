from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import Q, Sum
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
            return float(sum(item.quantity * item.price for item in self.items.all() if self.status == self.ORDER_STATUS_PAID or item.product.active))
    
    # def get_total_price(self):
    #     return float(self.items.filter(
    #         Q(order__status='p') | Q(product__active=True)  
    #     ).aggregate(total=Sum(models.F('quantity') * models.F('price')))['total'] or 0)
    

class OrderItem(models.Model):
    order=models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items',verbose_name=_('Order'))
    """
        We used models.PROTECT instead of models.CASCADE in the product field because, with CASCADE, if a product was deleted from the database,
        it would also be removed from all OrderItem records that belonged to an Order—both paid and unpaid.
        However, only unpaid OrderItems should be deleted.
        To prevent deletion, we used PROTECT and relied on the active field in the Product table.
        For unpaid orders, if a product becomes inactive, it will no longer be displayed.
    """
    product=models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items',verbose_name=_('Product'))
    quantity=models.PositiveIntegerField(verbose_name=_('Quantity'),default=1)
    price=models.DecimalField(max_digits=7, decimal_places=3, verbose_name=_('Price'))
    # price=models.PositiveIntegerField(verbose_name=_('Price'))

    def __str__(self):
        return f'Order Item {self.id}: {self.product} x {self.quantity}'
