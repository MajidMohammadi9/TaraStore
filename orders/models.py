from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from accounts.models import Customer


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
    first_name=models.CharField(verbose_name=_('First Name'),max_length=100)
    last_name=models.CharField(verbose_name=_('Last Name'),max_length=100)
    phone_number = PhoneNumberField(region="OM", blank=True, verbose_name=_('Phone Number'))
    # address=models.CharField(verbose_name=_('Address'),max_length=700)
    order_note=models.CharField(verbose_name=_('Note'),max_length=700,blank=True)
    status = models.CharField(max_length=1, choices=ORDER_STATUS, default=ORDER_STATUS_UNPAID)
    datetime_created=models.DateTimeField(verbose_name=_('Date Time Created'),auto_now_add=True)
    datetime_modified=models.DateTimeField(verbose_name=_('Date Time Modified'),auto_now=True)

    def __str__(self):
        return f'Order id={self.id}'
