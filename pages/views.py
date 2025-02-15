from django.views.generic import TemplateView
from django.utils.translation import gettext as _
from django.views.generic import ListView
from django.db.models import Prefetch,Q,Avg,Value,FloatField,Count
from django.db.models.functions import Coalesce

from products.models import Product, Category



class HomePageView(ListView):
    
    queryset = Category.objects.prefetch_related(
            Prefetch(
                'products',
                queryset=Product.objects.annotate(
                    average_rating=Coalesce(Avg('comments__stars'), Value(0, output_field=FloatField())),
                    product_stars_count=Count('comments', filter=Q(comments__stars__isnull=False))
                ).prefetch_related('images').order_by('-datetime_created')
            )
        )
    
    template_name = 'pages/home.html'
    context_object_name = 'categories'


class AboutUsPageView(TemplateView):
    template_name = 'pages/aboutus.html'


class ContactUsPageView(TemplateView):
    template_name = 'pages/contact_us.html'
