from django import forms

from app.models import PurchaseOrder, PurchaseOrderLineItem


class PurchaseOrderForm(forms.ModelForm):

    class Meta:
        model = PurchaseOrder
        fields = ('creator', 'supplier', 'contact', 'receiver', 'comments')
        widgets = {
            'creator': forms.Select(attrs={'class': 'form-control'}),
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'contact': forms.Select(attrs={'class': 'form-control'}),
            'receiver': forms.Select(attrs={'class': 'form-control'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': '5'}),
        }


class PurchaseOrderLineItemForm(forms.ModelForm):

    class Meta:
        model = PurchaseOrderLineItem
        fields = ('sku', 'unit_cost', 'qty_ordered', 'disc_percent', 'disc_dollar')
        widgets = {
            'sku': forms.Select(attrs={'class': 'form-control sku'}),
            'disc_dollar': forms.TextInput(attrs={'class': 'form-control'}),
            'disc_percent': forms.TextInput(attrs={'class': 'form-control'}),
            'qty_ordered': forms.TextInput(attrs={'class': 'form-control'}),
            'unit_cost': forms.TextInput(attrs={'class': 'form-control'}),
        }


PurchaseOrderLineItemFormset = forms.models.inlineformset_factory(
    PurchaseOrder, PurchaseOrderLineItem,
    form=PurchaseOrderLineItemForm, extra=5, can_delete=False
)
