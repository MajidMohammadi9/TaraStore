from django.views.generic import TemplateView
from django.utils.translation import gettext as _
from django.views.generic import ListView
from django.db.models import Prefetch,Q,Avg,Value,FloatField,Count
from django.db.models.functions import Coalesce
from django.shortcuts import render,redirect
from django.contrib import messages
from django.core.mail import send_mail

from products.models import Product, Category
from .forms import ContactForm



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


# class ContactUsPageView(TemplateView):
#     template_name = 'pages/contact_us.html'

def contact_us_view(request):
    if request.method=='POST':
        form=ContactForm(request.POST)
        if form.is_valid():
            name=form.cleaned_data['name']
            email=form.cleaned_data['email']
            message=form.cleaned_data['message']
            form.save()
            form=ContactForm()
            messages.success(request, _('Your message sent successfully'))

            # Send user message to my email
            # send_mail(
            #     subject=f'New email from {name}',
            #     message=message,
            #     from_email=email,
            #     recipient_list='majid@majid.com',
            #     fail_silently=False
            # )

            # Send email to user
            send_mail(
                subject='Confirm message receipt',
                message=f'dear {name}: We received your message and will respond soon.',
                from_email='TaraStore@gmail.com',
                recipient_list=[email],
                fail_silently=False
            )
            return redirect('contactus')
    else:
        form=ContactForm()
    return render(request, 'pages/contact_us.html', context={'form': form})

