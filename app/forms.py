from django import forms

from .models import *


class SkuQuantityAdjustmentForm(forms.ModelForm):

    class Meta:
        model = SkuQuantityAdjustment
        fields = ('who', 'sku', 'new', 'reason', 'detail')
        widgets = {
            'who': forms.Select(attrs={'class': 'form-control'}),
            'sku': forms.Select(attrs={'class': 'form-control'}),
            'new': forms.TextInput(attrs={'class': 'form-control'}),
            'reason': forms.Select(attrs={'class': 'form-control'}),
            'detail': forms.Textarea(attrs={'class': 'form-control'})
        }
