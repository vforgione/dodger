from django import forms

from models import *


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'categories': forms.CheckboxSelectMultiple(),
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'manufacturer': forms.Select(attrs={'class': 'form-control'}),
            'owner': forms.Select(attrs={'class': 'form-control'}),
            'reorder_threshold': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'cost': forms.TextInput(attrs={'class': 'form-control'}),
            'mfr_sku': forms.TextInput(attrs={'class': 'form-control'}),
            'case_qty': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'qty_on_hand': forms.TextInput(attrs={'class': 'form-control'}),
        }
        fields = ('name', 'supplier', 'manufacturer', 'categories', 'owner', 'reorder_threshold',
            'do_not_disturb', 'price', 'cost', 'mfr_sku', 'location', 'qty_on_hand')

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.sku:
            self.fields['cost'].widget.attrs['readonly'] = True
            self.fields['price'].widget.attrs['readonly'] = True
            self.fields['qty_on_hand'].widget.attrs['readonly'] = True


class ProductAttributeForm(forms.ModelForm):

    class Meta:
        model = ProductAttribute
        widgets = {
            'attribute': forms.Select(attrs={'class': 'form-control'}),
            'value': forms.TextInput(attrs={'class': 'form-control'}),
        }
        fields = ('attribute', 'value')


ProductAttributeFormset = forms.models.inlineformset_factory(Product, ProductAttribute,
    form=ProductAttributeForm, extra=10, can_delete=False)
