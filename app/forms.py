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
        fields = ('sku', 'qty_ordered', 'disc_percent', 'disc_dollar')
        widgets = {
            'sku': forms.Select(attrs={'class': 'form-control sku'}),
            'disc_dollar': forms.TextInput(attrs={'class': 'form-control'}),
            'disc_percent': forms.TextInput(attrs={'class': 'form-control'}),
            'qty_ordered': forms.TextInput(attrs={'class': 'form-control'}),
        }


PurchaseOrderLineItemFormset = forms.models.inlineformset_factory(
    PurchaseOrder, PurchaseOrderLineItem,
    form=PurchaseOrderLineItemForm, extra=5, can_delete=False
)


class ShipmentForm(forms.ModelForm):

    class Meta:
        model = Shipment
        fields = ('received_by', 'purchase_order')
        widgets = {
            'purchase_order': forms.Select(attrs={'class': 'form-control'}),
            'received_by': forms.Select(attrs={'class': 'form-control'}),
        }


class ShipmentLineItemForm(forms.ModelForm):

    class Meta:
        model = ShipmentLineItem
        widgets = {
            'sku': forms.Select(attrs={'class': 'form-control product'}),
            'qty_received': forms.TextInput(attrs={'class': 'form-control'}),
        }
        fields = ('sku', 'qty_received')


ShipmentLineItemFormset = forms.models.inlineformset_factory(
    Shipment, ShipmentLineItem,
    form=ShipmentLineItemForm, extra=5, can_delete=False
)
