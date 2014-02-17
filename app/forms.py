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
        fields = ('sku', 'qty_received')
        widgets = {
            'sku': forms.Select(attrs={'class': 'form-control sku'}),
            'qty_received': forms.TextInput(attrs={'class': 'form-control'}),
        }


ShipmentLineItemFormset = forms.models.inlineformset_factory(
    Shipment, ShipmentLineItem,
    form=ShipmentLineItemForm, extra=5, can_delete=False
)


class SkuForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SkuForm, self).__init__(*args, **kwargs)
        # dynamically restrict fields based on if create or update
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            # self.fields['cost'].widget.attrs['readonly'] = True
            # self.fields['price'].widget.attrs['readonly'] = True
            self.fields['qty_on_hand'].widget.attrs['readonly'] = True

    class Meta:
        model = Sku
        fields = (
            'name', 'categories', 'supplier', 'brand', 'owner', 'reorder_threshold',
            'notify_at_threshold', 'cost', 'mfr_sku', 'case_qty', 'location', 'qty_on_hand'
        )
        widgets = {
            'id': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'categories': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'brand': forms.Select(attrs={'class': 'form-control'}),
            'owner': forms.Select(attrs={'class': 'form-control'}),
            'reorder_threshold': forms.TextInput(attrs={'class': 'form-control'}),
            'cost': forms.TextInput(attrs={'class': 'form-control'}),
            'mfr_sku': forms.TextInput(attrs={'class': 'form-control'}),
            'case_qty': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'qty_on_hand': forms.TextInput(attrs={'class': 'form-control'}),
        }


class SkuAttributeForm(forms.ModelForm):

    class Meta:
        model = SkuAttribute
        fields = ('attribute', 'value')
        widgets = {
            'attribute': forms.Select(attrs={'class': 'form-control'}),
            'value': forms.TextInput(attrs={'class': 'form-control'}),
        }


SkuAttributeFormset = forms.models.inlineformset_factory(
    Sku, SkuAttribute, form=SkuAttributeForm, extra=8, can_delete=False
)
