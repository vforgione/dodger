from django import forms

from app.models import Sku, SkuAttribute


class SkuForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SkuForm, self).__init__(*args, **kwargs)
        # dynamically restrict fields based on if create or update
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['cost'].widget.attrs['readonly'] = True
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
