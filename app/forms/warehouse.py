from django import forms

from app.models import Shipment, ShipmentLineItem, SkuQuantityAdjustment


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
