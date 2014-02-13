from django import forms

from models import *


class PurchaseOrderForm(forms.ModelForm):

    class Meta:
        model = PurchaseOrder
        widgets = {
            'creator': forms.Select(attrs={'class': 'form-control', 'id': 'creator'}),
            'supplier': forms.Select(attrs={'class': 'form-control', 'id': 'supplier'}),
            'contact': forms.Select(attrs={'class': 'form-control', 'id': 'contact'}),
            'ship_to': forms.Select(attrs={'class': 'form-control', 'id': 'ship_to'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'id': 'comments', 'rows': '5'}),
        }
        fields = ('creator', 'supplier', 'contact', 'ship_to', 'comments')


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


PurchaseOrderProductFormset = forms.models.inlineformset_factory(PurchaseOrder, PurchaseOrderProduct,
    form=PurchaseOrderProductForm, extra=5, can_delete=False)


class SupplierForm(forms.ModelForm):

    class Meta:
        model = Supplier
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'terms': forms.TextInput(attrs={'class': 'form-control'}),
        }
        fields = ('name', 'terms', 'ships_products')


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'fax': forms.TextInput(attrs={'class': 'form-control'}),
            'address1': forms.TextInput(attrs={'class': 'form-control'}),
            'address2': forms.TextInput(attrs={'class': 'form-control'}),
            'address3': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control product'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'label': forms.Select(attrs={'class': 'form-control product'}),
            'represents': forms.Select(attrs={'class': 'form-control product'}),
        }
        fields = ('name', 'email', 'phone', 'fax', 'address1', 'address2', 'address3', 'city', 'state', 'zipcode',
            'country', 'represents', 'label')


ContactFormset = forms.models.inlineformset_factory(Supplier, Contact, ContactForm, extra=1, can_delete=False)


class ReceiverForm(forms.ModelForm):

    class Meta:
        model = Receiver
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address1': forms.TextInput(attrs={'class': 'form-control'}),
            'address2': forms.TextInput(attrs={'class': 'form-control'}),
            'address3': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
        }
        fields = ('name', 'address1', 'address2', 'address3', 'city', 'state', 'zipcode', 'country')


class ContactLabelForm(forms.ModelForm):

    class Meta:
        model = ContactLabel
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        fields = ('name', )
