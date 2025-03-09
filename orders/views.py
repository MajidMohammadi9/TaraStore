from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _

from .forms import OrderForm
from accounts.models import Customer,Address
from cart.cart import Cart
from .models import OrderItem 

@login_required
def order_create_view(request):
    customer=Customer.objects.select_related('user').get(user=request.user)
    address=Address.objects.filter(customer=customer).first()  # None is returned if no address exists.

    if request.method=='POST':
        order_form=OrderForm(request.POST, customer=customer, address=address)
        cart=Cart(request)

        if len(cart)==0:
            messages.warning(request, _('You can not proceed to checkout page, because your cart is empty!'))
            return redirect('home')

        if order_form.is_valid():
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
            return redirect('payment:payment_process')
            # messages.success(request, _('Your order has successfully placed.'))
            # return redirect('home')
    else:
        order_form=OrderForm(customer=customer, address=address)

    return render(request, 'orders/order_create.html', {'form': order_form})

