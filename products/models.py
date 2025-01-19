from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings
from django.urls import reverse



class Category(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500, blank=True)
    top_product = models.ForeignKey('Product', on_delete=models.SET_NULL, blank=True, null=True, related_name='+')

    def __str__(self):
        return self.title


class Discount(models.Model):
    discount = models.FloatField()
    description = models.CharField(max_length=255)

    def __str__(self):
        return f'{str(self.discount)} | {self.description}'


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    slug = models.SlugField()
    description = models.TextField()
    short_description=models.TextField(verbose_name='short description',blank=True)
    unit_price = models.DecimalField(max_digits=6, decimal_places=3)
    inventory = models.IntegerField(validators=[MinValueValidator(0)])
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    discounts = models.ManyToManyField(Discount, blank=True)
    active=models.BooleanField(verbose_name='active',default=True)
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
        (COMMENT_STATUS_WAITING, 'Waiting'),
        (COMMENT_STATUS_APPROVED, 'Approved'),
        (COMMENT_STATUS_NOT_APPROVED, 'Not Approved')
    ]

    PRODUCT_STARS=[
        ('1', 'Very Bad'),
        ('2', 'Bad'),
        ('3', 'Normal'),
        ('4', 'Good'),
        ('5', 'Perfect'),
    ]

    product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    author=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    body=models.TextField()
    stars=models.CharField(max_length=10, choices=PRODUCT_STARS)
    datetime_created=models.DateTimeField(auto_now_add=True)
    datetime_modified=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=2, choices=COMMENT_STATUS, default=COMMENT_STATUS_WAITING)
    active=models.BooleanField(default=True)

    # Manager
    objects=CommentManager()
    active_aproved_comment=AvtiveApprovedCommentManager()
    approved_comment=ApprovedCommentManager()
    active_comment=ActiveCommentManager()

    def __str__(self):
        return self.product.name
    
    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"pk": self.pk})
    

