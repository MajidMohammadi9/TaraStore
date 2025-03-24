from django.urls import path

from .views import (
    payment_process,
    payment_callback,
    payment_process_sandbox,
    payment_callback_sandbox,
    payment_sandbox_paypal,
    callback_sandbox_paypal,
)

app_name='payment'

urlpatterns = [
    # path('process/' ,payment_process_sandbox, name='payment_process'),
    # path('callback/',payment_callback_sandbox, name='payment_callback'),
    path('process/' ,payment_sandbox_paypal, name='payment_process'),
    path('callback/',callback_sandbox_paypal, name='payment_callback'),
]
