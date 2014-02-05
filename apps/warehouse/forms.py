from django import forms

from models import *
from apps.inventory_manager.models import Product


class ShipmentForm(forms.ModelForm):

    class Meta:
        model = Shipment
        widgets = {
            'purchase_order': forms.Select(attrs={'class': 'form-control', 'id': 'purchase-order'}),
            'received_by': forms.Select(attrs={'class': 'form-control'}),
        }
        fields = ('received_by', 'purchase_order')


class ShipmentProductForm(forms.ModelForm):

    class Meta:
        model = ShipmentProduct
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control product'}),
            'qty_received': forms.TextInput(attrs={'class': 'form-control'}),
        }
        fields = ('product', 'qty_received')


ShipmentProductFormset = forms.models.inlineformset_factory(Shipment, ShipmentProduct,
    form=ShipmentProductForm, extra=5, can_delete=False)
