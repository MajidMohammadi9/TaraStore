from django.contrib import messages
from django.utils.translation import gettext as _

from products.models import Product


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

    def add(self, product, quantity=1):
        """
         Add the specified product to the cart if it exists.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': quantity}
        else:
            self.cart[product_id]['quantity'] += quantity

        messages.success(self.request, _('Product added to cart successfully.'))
        self.save()

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

        messages.success(self.request, _('product removed from the cart successfully.'))
        self.save()

    def __iter__(self):
        product_ids=self.cart.keys()
        products=Product.objects.filter(id__in=product_ids)

        cart=self.cart.copy()

        for product in products:
            cart[product.id]['product_obj']=product

        for item in cart.values():
            item['total_price']=item['quantity']*item['product_obj'].price
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
    
    # def get_total_price(self):
    #     return sum(item['quantity']*item['product_obj'].price for item in self.cart.values())
    
    def get_total_price(self):
        return sum(item['total_price'] for item in self)  # Using the generated value in __iter__

        