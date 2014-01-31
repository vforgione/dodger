from django import forms

from models import *


class PurchaseOrderForm(forms.ModelForm):

    class Meta:
        model = PurchaseOrder
        exclude = ('name', )
        widgets = {
            'dat_member': forms.Select(attrs={'class': 'form-control', 'id': 'dat_member'}),
            'supplier': forms.Select(attrs={'class': 'form-control', 'id': 'supplier'}),
            'contact': forms.Select(attrs={'class': 'form-control', 'id': 'contact'}),
            'ship_to': forms.Select(attrs={'class': 'form-control', 'id': 'ship_to'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'id': 'comments', 'rows': '5'}),
        }
        fields = ('dat_member', 'supplier', 'contact', 'ship_to', 'comments')


class PurchaseOrderProductForm(forms.ModelForm):

    class Meta:
        model = PurchaseOrderProduct
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control product'}),
            'disc_dollar': forms.TextInput(attrs={'class': 'form-control'}),
            'disc_percent': forms.TextInput(attrs={'class': 'form-control'}),
            'qty_ordered': forms.TextInput(attrs={'class': 'form-control'}),
        }
        fields = ('product', 'disc_dollar', 'disc_percent', 'qty_ordered')
        exclude = ('DELETE', )


PurchaseOrderProductFormset = forms.models.inlineformset_factory(PurchaseOrder, PurchaseOrderProduct,
    form=PurchaseOrderProductForm, extra=5, can_delete=False)


class SupplierForm(forms.ModelForm):

    class Meta:
        model = Supplier
        excludes = ('id', )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'terms': forms.TextInput(attrs={'class': 'form-control'}),
        }
        fields = ('name', 'terms', 'ships_products')
