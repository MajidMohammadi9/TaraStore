from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Customer, Address


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'username')

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "usable_password", "password1", "password2"),
            },
        ),
    )
   

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=['first_name', 'last_name', 'email']
    list_per_page=10
    search_fields=['user__last_name__istartwith', 'user__first_name__istartwith']
    ordering=['user__last_name', 'user__first_name']

    def first_name(self, customer):
        return customer.user.first_name
    
    def last_name(self, customer):
        return customer.user.last_name
    
    def email(self, customer):
        return customer.user.email
    
    
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display=['full_name', 'street', 'city', 'province']
    list_per_page=10
    search_fields=['province', 'city', 'street']

    def full_name(self, address):
        return address.customer.full_name

