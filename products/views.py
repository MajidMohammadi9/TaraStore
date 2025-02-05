from django.shortcuts import redirect,render
from django.db.models import Prefetch
from django.contrib import messages
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import ListView,DetailView,CreateView
from django.utils.text import slugify
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Product,Comment
from .forms import CommentForm,ProductForm


class ProductListView(ListView):
    queryset=Product.objects.filter(active=True).order_by('-datetime_created')
    paginate_by=6
    template_name='products/product_list.html'
    context_object_name='products'


class ProductDetailView(DetailView):
    model=Product
    template_name='products/product_detail.html'
    context_object_name='product'

    def get_queryset(self):
        return super().get_queryset().prefetch_related(
            Prefetch(
                'comments',
                queryset = Comment.objects.filter(active=True, status='a').select_related('author'),
                # you can also use the Comment Manager, like the line below istead of the code above:
                # queryset = Comment.active_aproved_comment.all()
                # queryset = Comment.objects.get_active_and_approved()

                # to_attr='active_comments' # stores filtered comments (To display active comments in template, use ptroduct.active_comments)
            )
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] =CommentForm() 
        return context
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        self.object=self.get_object()
        comment_form=CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment=comment_form.save(commit=False)
            new_comment.product=self.object
            new_comment.author=request.user
            new_comment.save()
            messages.success(request, _('Comment successfully created.'))
            return redirect(self.object.get_absolute_url())
            # return redirect(reverse('product_detail',kwargs={'pk':self.object.pk}))
        
        # If form is invalid, re-render the page with the invalid form and existing context
        context=self.get_context_data()
        context['comment_form']=comment_form
        return self.render_to_response(context)
    

class ProductCreateView(UserPassesTestMixin,CreateView):
    model=Product
    # fields=['name', 'category', 'description', 'short_description', 'unit_price', 'inventory',]
    form_class=ProductForm
    template_name='products/product_create.html'
    context_object_name='form'

    def test_func(self):
        return self.request.user.is_staff
    
    def handle_no_permission(self):
        messages.error(self.request, _("You don't have permission to access this page."))
        return redirect('product_list')
    
    # def get_form(self, form_class = None):
    #     form=super().get_form(form_class)
    #     form.fields['description'].widget = CKEditorWidget()
    #     return form
   
    def form_valid(self, form):
        form.instance.slug=slugify(form.instance.name)
        messages.success(self.request, _('Product has been created successfully!'))
        return super().form_valid(form)
    
        
class ProductWomenListView(ListView):
    queryset=Product.objects.filter(category__title="women's", active=True).order_by('-datetime_created')
    paginate_by=6
    template_name='products/product_women.html'
    context_object_name='products_women'


class ProductMenListView(ListView):
    queryset=Product.objects.filter(category__title="men's", active=True).order_by('-datetime_created')
    paginate_by=6
    template_name='products/product_men.html'
    context_object_name='products_men'


class ProductKidsListView(ListView):
    queryset=Product.objects.filter(category__title="kid's", active=True).order_by('-datetime_created')
    paginate_by=6
    template_name='products/product_kids.html'
    context_object_name='products_kids'


def product_search(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(
        Q(name__icontains=query) | 
        Q(category__title__icontains=query)
        ).distinct().order_by('-datetime_created') if query else []

    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'products/search.html', {'query': query, 'page_obj': page_obj})
