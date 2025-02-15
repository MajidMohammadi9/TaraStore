from django import forms
from django.utils.translation import gettext as _
from ckeditor.widgets import CKEditorWidget

from .models import Comment, Product


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body', 'stars']
        widget = {
            'body': CKEditorWidget(),
            'stars': forms.HiddenInput(),
        }


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        
        fields = ['name', 'category', 'description', 'short_description', 'unit_price', 'inventory']
        widgets = {
            'description': CKEditorWidget(),
        }
