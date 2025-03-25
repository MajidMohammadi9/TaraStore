from django.urls import path

from .views import (
    payment_process,
    payment_callback,
    payment_sandbox_zarinpal,
    callback_sandbox_zarinpal,
    payment_sandbox_paypal,
    callback_sandbox_paypal,
)

app_name='payment'

urlpatterns = [
    path('payment-zarinpal/' , payment_sandbox_zarinpal, name='payment_zarinpal'),
    path('callback-zarinpal/', callback_sandbox_zarinpal, name='callback_zarinpal'),
    path('payment-paypal/' , payment_sandbox_paypal, name='payment_paypal'),
    path('callback-paypal/', callback_sandbox_paypal, name='callback_paypal'),
]
