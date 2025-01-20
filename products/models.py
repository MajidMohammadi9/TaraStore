from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    description = models.CharField(max_length=500, blank=True, verbose_name=_('Description'))
    top_product = models.ForeignKey('Product', on_delete=models.SET_NULL, blank=True, null=True, related_name='+', verbose_name=_('Top Product'))

    def __str__(self):
        return self.title


class Discount(models.Model):
    discount = models.FloatField(verbose_name=_('Discount'))
    description = models.CharField(max_length=255, verbose_name=_('Description'))

    def __str__(self):
        return f'{str(self.discount)} | {self.description}'


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Product Name'))
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products', verbose_name=_('Category'))
    slug = models.SlugField(verbose_name=_('Slug'))
    description = models.TextField(verbose_name=_('Description'))
    short_description=models.TextField(blank=True, verbose_name=_('Short Description'))
    unit_price = models.DecimalField(max_digits=6, decimal_places=3, verbose_name=_('Price'))
    inventory = models.IntegerField(validators=[MinValueValidator(0)], verbose_name=_('Inventory'))
    datetime_created = models.DateTimeField(auto_now_add=True, verbose_name=_('Date Time Created'))
    datetime_modified = models.DateTimeField(auto_now=True, verbose_name=_('Date Time Modified'))
    discounts = models.ManyToManyField(Discount, blank=True, verbose_name=_('Discount'))
    active=models.BooleanField(default=True, verbose_name=_('Active'))
    # image=models.ImageField(verbose_name='Product image',upload_to='product/product_cover/',blank=True,)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"pk": self.pk})
    

class CommentManager(models.Manager):
    def get_active_and_approved(self):
        return self.get_queryset().filter(active=True, status=Comment.COMMENT_STATUS_APPROVED).select_related('product', 'author')
    
    def get_active(self):
        return self.get_queryset().filter(active=True).select_related('product', 'author')
    
    def get_approved(self):
        return self.get_queryset().filter(status=Comment.COMMENT_STATUS_APPROVED).select_related('product', 'author')
    

class ActiveCommentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True).select_related('product', 'author')
    

class ApprovedCommentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Comment.COMMENT_STATUS_APPROVED).select_related('product', 'author')
    

class AvtiveApprovedCommentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True, status=Comment.COMMENT_STATUS_APPROVED).select_related('product', 'author')


class Comment(models.Model):
    COMMENT_STATUS_WAITING='w'
    COMMENT_STATUS_APPROVED='a'
    COMMENT_STATUS_NOT_APPROVED='na'

    COMMENT_STATUS=[
        (COMMENT_STATUS_WAITING, _('Waiting')),
        (COMMENT_STATUS_APPROVED, _('Approved')),
        (COMMENT_STATUS_NOT_APPROVED, _('Not Approved'))
    ]

    PRODUCT_STARS=[
        ('1', _('Very Bad')),
        ('2', _('Bad')),
        ('3', _('Normal')),
        ('4', _('Good')),
        ('5', _('Perfect')),
    ]

    product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', verbose_name=_('Product'))
    author=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments', verbose_name=_('Author'))
    body=models.TextField(verbose_name=_('Comment Text'))
    stars=models.CharField(max_length=10, choices=PRODUCT_STARS, verbose_name=_('Product Rating'))
    datetime_created=models.DateTimeField(auto_now_add=True, verbose_name=_('Date Time Created'))
    datetime_modified=models.DateTimeField(auto_now=True, verbose_name=_('Date Time Modified'))
    status=models.CharField(max_length=2, choices=COMMENT_STATUS, default=COMMENT_STATUS_WAITING, verbose_name=_('Status'))
    active=models.BooleanField(default=True, verbose_name=_('Active'))

    # Manager
    objects=CommentManager()
    active_aproved_comment=AvtiveApprovedCommentManager()
    approved_comment=ApprovedCommentManager()
    active_comment=ActiveCommentManager()

    def __str__(self):
        return self.product.name
    
    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"pk": self.pk})
    

