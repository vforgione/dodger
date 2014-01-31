from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.forms.models import inlineformset_factory
from django.shortcuts import get_object_or_404, get_list_or_404, render_to_response
from django.template import RequestContext

from forms import *
from models import *

from inventory_manager.models import Product


PAGE_SIZE = 20


def home(request):
    pass


# purchase orders
def po_view(request, pk=None):
    """view purchase order or paginated list of purchase orders"""
    if pk:
        try:
            po = get_object_or_404(PurchaseOrder, pk=pk)
        except:
            po = get_object_or_404(PurchaseOrder, name=pk)
        pos = [po, ]
    else:
        pos = get_list_or_404(PurchaseOrder.objects.order_by('-name'))
        paginator = Paginator(pos, PAGE_SIZE)

        page = request.GET.get('page', 1)
        try:
            pos = paginator.page(page)
        except PageNotAnInteger:
            pos = paginator.page(1)
        except EmptyPage:
            pos = paginator.page(paginator.num_pages)

    display_pages = len(pos) > 1
    return render_to_response(
        'dat/po-view.html',
        {
            'pos': pos,
            'display_pages': display_pages
        },
        context_instance=RequestContext(request)
    )


def po_create(request):
    form = PurchaseOrderForm()
    form.fields['dat_member'].initial = request.user
    form.fields['contact'].queryset = Contact.objects.filter(name='')
    prod_formset = inlineformset_factory(PurchaseOrder, PurchaseOrderProduct, form=PurchaseOrderProductForm, extra=5, can_delete=False)
    formset = prod_formset(instance=PurchaseOrder())
    for _form in formset:
        _form.fields['product'].queryset = Product.objects.filter(name='')
    return render_to_response(
        'dat/po-create.html',
        {
            'form': form,
            'formset': formset,
        },
        context_instance=RequestContext(request)
    )


# suppliers
def supplier_view(request, pk=None):
    pass


def supplier_create(request):
    pass


def supplier_update(request, pk):
    pass


# contacts
def contact_view(request, pk=None):
    pass


def contact_create(request):
    pass


def contact_update(request, pk):
    pass


# contact labels
def cl_view(request, pk=None):
    pass


def cl_create(request):
    pass


def cl_update(request, pk):
    pass


# receivers
def receiver_view(request, pk=None):
    pass


def receiver_create(request):
    pass


def receiver_update(request, pk):
    pass
