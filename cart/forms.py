from django import forms

class AddToCartProductForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'input-text qty text',
            'step': '1',
            'size': '4',
            'title': 'Qty'
        })
    )
