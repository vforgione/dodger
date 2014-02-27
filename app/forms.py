from django import forms

from models import *


# control models
class ControlModelForm(forms.ModelForm):

    class Meta:
        fields = ('name', )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control name'})
        }


class AttributeForm(ControlModelForm):

    class Meta:
        model = Attribute


class BrandForm(ControlModelForm):

    class Meta:
        model = Brand


class CategoryForm(ControlModelForm):

    class Meta:
        model = Category


class ContactLabelForm(ControlModelForm):

    class Meta:
        model = ContactLabel


class CostAdjustmentReasonForm(ControlModelForm):

    class Meta:
        model = CostAdjustmentReason


class QuantityAdjustmentReasonForm(ControlModelForm):

    class Meta:
        model = QuantityAdjustmentReason


class SupplierForm(ControlModelForm):

    class Meta:
        model = Supplier


# adjustment models
class CostAdjustmentForm(forms.ModelForm):

    class Meta:
        model = CostAdjustment
        fields = ('who', 'sku', 'new', 'reason', 'detail')
        widgets = {
            'sku': forms.TextInput(attrs={'class': 'form-control sku'}),
            'old': forms.TextInput(attrs={'class': 'form-control old'}),
            'new': forms.TextInput(attrs={'class': 'form-control new'}),
            'who': forms.Select(attrs={'class': 'form-control who'}),
            'reason': forms.Select(attrs={'class': 'form-control reason'}),
            'detail': forms.TextInput(attrs={'class': 'form-control detail'}),
        }


class QuantityAdjustmentForm(forms.ModelForm):

    class Meta:
        model = QuantityAdjustment
        fields = ('who', 'sku', 'new', 'reason', 'detail')
        widgets = {
            'sku': forms.TextInput(attrs={'class': 'form-control sku'}),
            'old': forms.TextInput(attrs={'class': 'form-control old'}),
            'new': forms.TextInput(attrs={'class': 'form-control new'}),
            'who': forms.Select(attrs={'class': 'form-control who'}),
            'reason': forms.Select(attrs={'class': 'form-control reason'}),
            'detail': forms.TextInput(attrs={'class': 'form-control detail'}),
        }


# detailed models
class SkuForm(forms.ModelForm):

    class Meta:
        model = Sku
        fields = (
            'name', 'upc', 'brand', 'categories', 'quantity_on_hand', 'location', 'owner', 'supplier',
            'lead_time', 'minimum_quantity', 'notify_at_threshold', 'cost', 'supplier_sku', 'case_quantity',
            'in_live_deal', 'is_subscription'
        )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control name'}),
            'upc': forms.TextInput(attrs={'class': 'form-control upc'}),
            'brand': forms.Select(attrs={'class': 'form-control brand'}),
            'categories': forms.SelectMultiple(attrs={'class': 'form-control categories'}),
            'quantity_on_hand': forms.TextInput(attrs={'class': 'form-control quantity-on-hand'}),
            'location': forms.TextInput(attrs={'class': 'form-control location'}),
            'owner': forms.Select(attrs={'class': 'form-control owner'}),
            'supplier': forms.Select(attrs={'class': 'form-control supplier'}),
            'lead_time': forms.TextInput(attrs={'class': 'form-control lead-time'}),
            'minimum_quantity': forms.TextInput(attrs={'class': 'form-control minimum-quantity'}),
            'cost': forms.TextInput(attrs={'class': 'form-control cost'}),
            'supplier_sku': forms.TextInput(attrs={'class': 'form-control supplier-sku'}),
            'case_quantity': forms.TextInput(attrs={'class': 'form-control case-quantity'}),
        }

    def __init__(self, *args, **kwargs):
        super(SkuForm, self).__init__(*args, **kwargs)
        # dynamically restrict fields based on if create or update
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['cost'].widget.attrs['readonly'] = True
            self.fields['quantity_on_hand'].widget.attrs['readonly'] = True


class SkuAttributeForm(forms.ModelForm):

    class Meta:
        model = SkuAttribute
        fields = ('sku', 'attribute', 'value')
        widgets = {
            'sku': forms.Select(attrs={'class': 'form-control sku'}),
            'attribute': forms.Select(attrs={'class': 'form-control attribute'}),
            'value': forms.TextInput(attrs={'class': 'form-control value'}),
        }


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = (
            'name', 'represents', 'label', 'email', 'phone', 'fax', 'address1', 'address2', 'address3',
            'city', 'state', 'zipcode', 'country'
        )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control name'}),
            'represents': forms.Select(attrs={'class': 'form-contro representsl'}),
            'label': forms.Select(attrs={'class': 'form-control label'}),
            'email': forms.TextInput(attrs={'class': 'form-control email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control phone'}),
            'fax': forms.TextInput(attrs={'class': 'form-control fax'}),
            'address1': forms.TextInput(attrs={'class': 'form-control address1'}),
            'address2': forms.TextInput(attrs={'class': 'form-control address2'}),
            'address3': forms.TextInput(attrs={'class': 'form-control address3'}),
            'city': forms.TextInput(attrs={'class': 'form-control city'}),
            'state': forms.Select(attrs={'class': 'form-control state'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-control zipcode'}),
            'country': forms.TextInput(attrs={'class': 'form-control country'}),
        }


class ReceiverForm(forms.ModelForm):

    class Meta:
        model = Receiver
        fields = ('name', 'address1', 'address2', 'address3', 'city', 'state', 'zipcode', 'country')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control name'}),
            'address1': forms.TextInput(attrs={'class': 'form-control address1'}),
            'address2': forms.TextInput(attrs={'class': 'form-control address2'}),
            'address3': forms.TextInput(attrs={'class': 'form-control address3'}),
            'city': forms.TextInput(attrs={'class': 'form-control city'}),
            'state': forms.Select(attrs={'class': 'form-control state'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-control zipcode'}),
            'country': forms.TextInput(attrs={'class': 'form-control country'}),
        }


class PurchaseOrderForm(forms.ModelForm):

    class Meta:
        model = PurchaseOrder
        fields = ('creator', 'receiver', 'supplier', 'contact', 'terms', 'expected_arrival', 'note')
        widgets = {
            'creator': forms.Select(attrs={'class': 'form-control creator'}),
            'supplier': forms.Select(attrs={'class': 'form-control supplier'}),
            'contact': forms.Select(attrs={'class': 'form-control contact'}),
            'receiver': forms.Select(attrs={'class': 'form-control receiver'}),
            'terms': forms.TextInput(attrs={'class': 'form-control terms'}),
            'expected_arrival': forms.TextInput(attrs={'class': 'form-control expected-arrival'}),
            'note': forms.TextInput(attrs={'class': 'form-control note'}),
        }


class PurchaseOrderLineItemForm(forms.ModelForm):

    class Meta:
        model = PurchaseOrderLineItem
        fields = ('sku', 'quantity_ordered', 'unit_cost', 'discount_percent', 'discount_dollar')
        widgets = {
            'sku': forms.Select(attrs={'class': 'form-control sku'}),
            'quantity_ordered': forms.TextInput(attrs={'class': 'form-control quantity-ordered'}),
            'unit_cost': forms.TextInput(attrs={'class': 'form-control unit-cost'}),
            'discount_percent': forms.TextInput(attrs={'class': 'form-control discount-percent'}),
            'discount_dollar': forms.TextInput(attrs={'class': 'form-control discount-dollar'}),
        }


class ShipmentForm(forms.ModelForm):

    class Meta:
        model = Shipment
        fields = ('creator', 'purchase_order', 'note')
        widgets = {
            'creator': forms.Select(attrs={'class': 'form-control creator'}),
            'purchase_order': forms.Select(attrs={'class': 'form-control purchase-order'}),
            'note': forms.TextInput(attrs={'class': 'form-control note'}),
        }


class ShipmentLineItemForm(forms.ModelForm):

    class Meta:
        model = ShipmentLineItem
        fields = ('sku', 'quantity_received')
        widgets = {
            'sku': forms.Select(attrs={'class': 'form-control sku'}),
            'quantity_received': forms.TextInput(attrs={'class': 'form-control quantity-received'}),
        }


# formsets
SkuAttributeFormset = forms.models.inlineformset_factory(
    Sku, SkuAttribute, form=SkuAttributeForm, extra=8, can_delete=False
)


PurchaseOrderLineItemFormset = forms.models.inlineformset_factory(
    PurchaseOrder, PurchaseOrderLineItem, form=PurchaseOrderLineItemForm, extra=5, can_delete=False
)


ShipmentLineItemFormset = forms.models.inlineformset_factory(
    Shipment, ShipmentLineItem, form=ShipmentLineItemForm, extra=5, can_delete=False
)
