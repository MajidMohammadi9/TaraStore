from django.shortcuts import render,get_object_or_404,redirect

from .cart import Cart
from products.models import Product
from .forms import AddToCartProductForm


def cart_detail_view(request):
    cart=Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart':cart})

def add_to_cart_view(requset, product_id):
    cart=Cart(requset)

    product=get_object_or_404(Product, id=product_id)
    form=AddToCartProductForm(requset.POST)

    if form.is_valid():
        cleaned_data=form.cleaned_data
        quantity=cleaned_data['quantity']
        print(f'quantity={quantity}')
        cart.add(product, quantity)
    return redirect('cart:cart_detail')
