from django.contrib import messages
from django.utils.translation import gettext as _
from django.db.models import Prefetch
from django.db.models import OuterRef, Subquery

from products.models import Product,ProductImage
from .forms import AddToCartProductForm


class Cart:
    def __init__(self, request):
        """
        Initialize the cart
        """
        self.request = request
        self.session = request.session

        # cart=self.session.get('cart')
        # if not cart:
        #     self.session['cart']={}
        #     cart=self.session['cart']
        # self.cart=cart
        self.cart = self.session.setdefault('cart', {})

    def add(self, product, quantity=1, replace_current_quantity=False):
        """
         Add the specified product to the cart if it exists.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0}

        if replace_current_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        if self.cart[product_id]['quantity'] <= product.inventory:
            self.save()
            messages.success(self.request, _('Product added to cart successfully.'))
        else:
            messages.error(self.request, _('Sorry, The selected quantity exceeds the available stock.'))

    def save(self):
        """
         Mark session as modified to save changes
        """
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart
        """
        product_id=str(product.id)
        
        if product_id in self.cart:
            del self.cart[product_id]
            # self.cart.pop(product_id, None)

        messages.success(self.request, _('product removed from the cart successfully.'))
        self.save()

    def __iter__(self):
        product_ids = self.cart.keys()

        first_image_subquery = ProductImage.objects.filter(
            product=OuterRef('pk')
        ).order_by('id').values('image')[:1]

        products = Product.objects.filter(id__in=product_ids).annotate(
            first_image=Subquery(first_image_subquery)
        )

        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product_obj'] = product

        for item in cart.values():
            item['total_price'] = item['quantity'] * item['product_obj'].unit_price
            # This is used in cart_detail.html to refresh the quantity
            item['product_update_quantity_form']=AddToCartProductForm(initial={'quantity': item['quantity'], 'inplace' :True})
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def clear(self):
        del self.session['cart']
        self.save()

    def is_empty(self):
        if self.cart:
            return False
        return True
    
    def get_total_price(self):
        return sum(item['quantity']*item['product_obj'].unit_price for item in self.cart.values())
    


        