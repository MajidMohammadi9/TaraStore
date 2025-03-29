from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from django.db import transaction
from django.db.models import Prefetch
from django.views.decorators.cache import cache_control
from django.utils.decorators import method_decorator

from .forms import OrderForm
from accounts.models import Customer,Address
from cart.cart import Cart
from .models import OrderItem,Order

@login_required
def order_create_view(request):
    customer=Customer.objects.select_related('user').get(user=request.user)
    address=Address.objects.filter(customer=customer).first()  # None is returned if no address exists.

    if request.method=='POST':
        payment_method = request.POST.get('payment-method')
        order_form=OrderForm(request.POST, customer=customer, address=address)
        cart=Cart(request)

        if len(cart)==0:
            messages.warning(request, _('You can not proceed to checkout page, because your cart is empty!'))
            return redirect('home')

        if order_form.is_valid() and payment_method in ['zarinpal', 'paypal']:
            with transaction.atomic():
                order_obj=order_form.save(commit=False)
                order_obj.customer=customer
                order_obj.save()

                for item in cart:
                    product=item['product_obj']
                    OrderItem.objects.create(
                        order=order_obj,
                        product=product,
                        quantity=item['quantity'],
                        price=product.unit_price
                    )
                cart.clear()

                customer.user.first_name=order_form.cleaned_data['first_name']
                customer.user.last_name = order_form.cleaned_data['last_name']
                customer.phone_number = order_form.cleaned_data['phone_number']
                customer.user.email = order_form.cleaned_data['email']
                customer.user.save()
                customer.save()

                address_data = {
                        'street': order_form.cleaned_data['street'],
                        'city': order_form.cleaned_data['city'],
                        'province': order_form.cleaned_data['province'],
                        'postal_code': order_form.cleaned_data['postal_code'],
                        'country': order_form.cleaned_data['country'],
                    }
                
                if address:
                    Address.objects.filter(customer=customer).update(**address_data)
                else:
                    Address.objects.create(customer=customer, **address_data)
                
                request.session['order_id']=order_obj.id
                if payment_method == 'paypal':
                    return redirect('payment:payment_paypal')
                elif payment_method == 'zarinpal':
                    return redirect('payment:payment_zarinpal')
                
        else:
            messages.error(request, _('Please fill in all fields and select a payment method.'))
    else:
        order_form=OrderForm(customer=customer, address=address)

    return render(request, 'orders/order_create.html', {'form': order_form})

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def my_orders_view(request):
    orders=Order.objects.filter(customer__user=request.user)\
        .select_related('customer')\
            .prefetch_related(Prefetch('items', queryset=OrderItem.objects.select_related('product')))\
                .order_by('-datetime_created')

    # items_to_update=[]
    # for order in orders:
    #     if order.status==order.ORDER_STATUS_UNPAID:
    #         for item in order.items.all():
    #             if item.product.unit_price != item.price:
    #                 item.price=item.product.unit_price
    #                 items_to_update.append(item)
    # if items_to_update:
    #     OrderItem.objects.bulk_update(items_to_update, ['price'])
            
    return render(request, 'orders/my_orders.html', context={'orders': orders})

@login_required
def order_detail_view(request, order_id):
    # order=get_object_or_404(Order.objects.prefetch_related('items__product'), id=order_id)
    order=get_object_or_404(Order.objects.prefetch_related(
        Prefetch('items', queryset=OrderItem.objects.select_related('product'))
    ), id=order_id)

    return render(request, 'orders/order_detail.html', context={'order': order})