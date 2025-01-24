from django import forms

from ckeditor.widgets import CKEditorWidget

from .models import Comment,Product


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body', 'stars']
        widget={
              'body': CKEditorWidget(),
        }


class ProductForm(forms.ModelForm):
            class Meta:
                model = Product
                fields=['name', 'category', 'description', 'short_description', 'unit_price', 'inventory',]
                widgets = {
                    'description': CKEditorWidget(),
                }
