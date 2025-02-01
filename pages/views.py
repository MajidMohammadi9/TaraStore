from django.views.generic import TemplateView
from django.utils.translation import gettext as _
from django.views.generic import ListView
from django.db.models import Q

from products.models import Product


class HomePageView(ListView):
        model=Product
        template_name='pages/home.html'

        def get_queryset(self):
            # queryset=Product.objects.filter(category__title__in=["women's", "men's"], active=True).order_by('-datetime_created')
            queryset=Product.objects.select_related('category').filter(
                 Q(category__title="women's")|Q(category__title="men's")|Q(category__title="kid's"),
                   active=True).order_by('-datetime_created')
            return queryset
        

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            queryset=self.get_queryset()
            context["products_women"] = [product for product in queryset if product.category.title=="women's"]
            context["products_men"] = [product for product in queryset if product.category.title=="men's"]
            context["products_kids"] = [product for product in queryset if product.category.title=="kid's"]
            return context
        

class AboutUsPageView(TemplateView):
    template_name='pages/aboutus.html'


class ContactUsPageView(TemplateView):
     template_name='pages/contact_us.html'

