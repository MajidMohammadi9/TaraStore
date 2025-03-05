
from django import forms
from django.utils.translation import gettext_lazy as _

from orders.models import Order
from phonenumber_field.formfields import PhoneNumberField

class OrderForm(forms.ModelForm):
    first_name = forms.CharField(label=_("first name"), max_length=150,)
    last_name = forms.CharField(label=_("last name"), max_length=150,)
    phone_number = PhoneNumberField(label=_('Phone Number'), region="OM",)
    email = forms.EmailField(label=_("email address"))

    street = forms.CharField(label=_('Street'), max_length=255)
    city = forms.CharField(label=_('City'), max_length=255, )
    province = forms.CharField(label=_('Province'), max_length=255, )
    postal_code = forms.CharField(label=_('Postal Code'), max_length=20, )
    country = forms.CharField(label=_('Country'), max_length=100, )

    class Meta:
        model=Order
        fields=[
            'first_name', 'last_name', 'phone_number','email',
            'street', 'city', 'province', 'postal_code', 'country', 'order_note'
            ]
        widgets={
            'order_note':forms.Textarea(attrs={'rows':5,'placeholder':_('If you have any notes, please enter here otherwise leave it empty.')}),
        }

    def __init__(self, *args, **kwargs):

        # Removing customer from kwargs and assign it to self.customer
        self.customer = kwargs.pop('customer', None)

        # or use the lines below instead of the line above (kwargs is a dictionary)
        # self.customer=kwargs.get('customer', None)
        # del kwargs['customer'] 

        self.address = kwargs.pop('address', None)   
        
        super().__init__(*args, **kwargs)
        if self.customer:
            self.fields['first_name'].initial=self.customer.user.first_name
            self.fields['last_name'].initial=self.customer.user.last_name
            self.fields['phone_number'].initial=self.customer.phone_number
            self.fields['email'].initial=self.customer.user.email

        if self.address:
            self.fields['street'].initial = self.address.street
            self.fields['city'].initial = self.address.city
            self.fields['province'].initial = self.address.province
            self.fields['postal_code'].initial = self.address.postal_code
            self.fields['country'].initial = self.address.country
