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
            'notify_at_threshold', 'price', 'cost', 'mfr_sku', 'location', 'qty_on_hand')

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        # dynamically restrict fields based on if create or update
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


class ProductQtyChangeForm(forms.ModelForm):

    class Meta:
        model = ProductQtyChange
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'who': forms.Select(attrs={'class': 'form-control'}),
            'reason': forms.Select(attrs={'class': 'form-control'}),
            'old_qty': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'new_qty': forms.TextInput(attrs={'class': 'form-control'}),
        }
        fields = ('who', 'product', 'reason', 'old_qty', 'new_qty')


class ProductCostChangeForm(forms.ModelForm):

    class Meta:
        model = ProductCostChange
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'who': forms.Select(attrs={'class': 'form-control'}),
            'reason': forms.Select(attrs={'class': 'form-control'}),
            'old_cost': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'new_cost': forms.TextInput(attrs={'class': 'form-control'}),
        }
        fields = ('who', 'product', 'reason', 'old_cost', 'new_cost')


class ProductPriceChangeForm(forms.ModelForm):

    class Meta:
        model = ProductPriceChange
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'who': forms.Select(attrs={'class': 'form-control'}),
            'reason': forms.Select(attrs={'class': 'form-control'}),
            'old_price': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'new_price': forms.TextInput(attrs={'class': 'form-control'}),
        }
        fields = ('who', 'product', 'reason', 'old_price', 'new_price')


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        fields = ('name', )


class ManufacturerForm(forms.ModelForm):

    class Meta:
        model = Manufacturer
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        fields = ('name', )


class AttributeForm(forms.ModelForm):

    class Meta:
        model = Attribute
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        fields = ('name', )
