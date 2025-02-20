from django.db import models
from django.utils.translation import gettext_lazy as _


class Contact(models.Model):
    name=models.CharField(max_length=100, verbose_name=_('Name'))
    email=models.EmailField(verbose_name=_('Email'))
    message=models.TextField(verbose_name=_('message'))
    datetime_created=models.DateTimeField(auto_now_add=True, verbose_name=_('Date Time Created'))
