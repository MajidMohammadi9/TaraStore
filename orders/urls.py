from django.urls import path

from .views import order_create_view, my_orders_view,order_detail_view


urlpatterns = [
    path('create/', order_create_view, name='order_create'),
    path('my-orders/', my_orders_view, name='my_orders'),
    path('my-orders/<int:order_id>/', order_detail_view, name='order_detail'),
]
