from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name=_('Email'))


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name=_('User'))
    phone_number = PhoneNumberField(region="OM", blank=True, verbose_name=_('Phone Number'))
    birth_date = models.DateField(null=True, blank=True, verbose_name=_('Birth Date'))

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Address(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True, verbose_name=_('Customer'))
    street = models.CharField(max_length=255, verbose_name=_('Street'))
    city = models.CharField(max_length=255, verbose_name=_('City'))
    province = models.CharField(max_length=255, verbose_name=_('Province'))
    postal_code = models.CharField(max_length=20, verbose_name=_('Postal Code'))
    country = models.CharField(max_length=100, verbose_name=_('Country'))

    def __str__(self):
        return f'{self.street}, {self.city}, {self.country}'
    