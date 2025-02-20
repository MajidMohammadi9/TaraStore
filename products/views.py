from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Prefetch, Q, Avg, Value, FloatField,Count
from django.contrib import messages
from django.urls import reverse,reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils.text import slugify
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.db.models.functions import Coalesce

from .models import Product, Comment, ProductImage, Category
from .forms import CommentForm, ProductForm


class ProductQuerysetMixin:
    def get_queryset(self):
        queryset = Product.objects.filter(active=True)\
            .prefetch_related('images')\
            .annotate(
                average_rating=Coalesce(Avg('comments__stars'), Value(0, output_field=FloatField())),
                product_stars_count=Count('comments', filter=Q(comments__stars__isnull=False))
            ).order_by('-datetime_created')

        if hasattr(self, 'category_title'):
            queryset = queryset.filter(category__title=self.category_title)

        return queryset


class BaseProductListView(ProductQuerysetMixin, ListView):
    paginate_by = 6
    context_object_name = 'products'
    

class ProductListView(BaseProductListView):
    template_name = 'products/product_list.html'


class ProductWomenListView(BaseProductListView):
    category_title = "womens"
    template_name = 'products/product_women.html'
    context_object_name = 'products_women'


class ProductMenListView(BaseProductListView):
    category_title = "mens"
    template_name = 'products/product_men.html'
    context_object_name = 'products_men'


class ProductKidsListView(BaseProductListView):
    category_title = "kids"
    template_name = 'products/product_kids.html'
    context_object_name = 'products_kids'




class ProductDetailView(ProductQuerysetMixin, DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        return super().get_queryset().prefetch_related(
            Prefetch(
                'comments',
                queryset=Comment.objects.filter(active=True, status='a').select_related('author')
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.product = self.object
            new_comment.author = request.user
            new_comment.save()
            messages.success(request, _('Comment successfully created.'))
            return redirect(self.object.get_absolute_url())
            # return redirect(reverse('product_detail',kwargs={'pk':self.object.pk}))

        # If form is invalid, re-render the page with the invalid form and existing context
        context = self.get_context_data()
        context['comment_form'] = comment_form
        return self.render_to_response(context)


class ProductCreateView(UserPassesTestMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_create.html'
    context_object_name = 'form'

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, _("You don't have permission to add products.(Only admin)"))
        return redirect('product_list')

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.name)

        response = super().form_valid(form)

        # get image file from request
        images = self.request.FILES.getlist('images')
        if images:
            for image in images:
                ProductImage.objects.create(product=self.object, image=image)

        messages.success(self.request, _('Product has been created successfully!'))
        return response
    

class ProductUpdateView(UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_update.html'
    context_object_name = 'product'

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, _("You don't have permission to Edit products.(Only admin)"))
        return redirect(reverse('product_detail', kwargs={'pk': self.get_object().pk})) 
    
    def form_valid(self, form):        
        # Delete selected images
        delete_images = self.request.POST.getlist('delete_images')
        ProductImage.objects.filter(id__in=delete_images).delete()
        
        # Upload new images
        images = self.request.FILES.getlist('images')
        if images:
            for image in images:
                ProductImage.objects.create(product=self.object, image=image)
                
        messages.success(self.request, _('Product has been updated successfully!'))
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print(f"Form errors: {form.errors}")
        messages.error(self.request, _("There are errors in the form. Please fix them."))
        return self.render_to_response(self.get_context_data(form=form))
    

class ProductDeleteView(UserPassesTestMixin, DeleteView):
    model=Product
    template_name='products/product_delete.html'
    success_url=reverse_lazy('product_list')

    def test_func(self):
        return self.request.user.is_staff
    
    def handle_no_permission(self):
        messages.error(self.request, _("You don't have permission to delete products.(Only admin)"))
        return redirect('product_list')
    
    def post(self, request, *args, **kwargs):
        product=self.get_object()
        # messages.success(self.request, _("Product was deleted successfully"))
        messages.success(self.request, _("%(name)s was deleted successfully!") % {"name": product.name})
        return super().post(request, *args, **kwargs)

    
class ProductSearchView(BaseProductListView):
    template_name='products/search.html'

    def get_queryset(self):
        queryset=super().get_queryset() # Get queryset from BaseProductListView
        
        query=self.request.GET.get('q', '')
        if query:
            queryset=queryset.filter(Q(name__icontains=query) | Q(category__title__icontains=query)).distinct()
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query']=self.request.GET.get('q', '')
        # context['total_products']=self.get_queryset().count()
        return context
    

# def product_search(request):
#     query = request.GET.get('q', '')
#     products = Product.objects.filter(
#         Q(name__icontains=query) |
#         Q(category__title__icontains=query)
#     ).distinct().order_by('-datetime_created') if query else []

#     paginator = Paginator(products, 6)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     return render(request, 'products/search.html', {'query': query, 'page_obj': page_obj})

    
