from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, get_list_or_404, redirect, render_to_response
from django.template import RequestContext

from forms import *
from models import *

from dat.models import PurchaseOrder, PurchaseOrderProduct


PAGE_SIZE = 20


# shipments
def shipment_view(request, pk=None):
    """view a list of received shipments or an individual shipment"""
    if pk:
        try:
            shipment = get_object_or_404(Shipment, pk=pk)
        except:
            shipment = get_object_or_404(Shipment, name=pk)
        shipments = [shipment, ]
    else:
        shipments = get_list_or_404(Shipment.objects.order_by('-received_on'))
        paginator = Paginator(shipments, PAGE_SIZE)

        page = request.GET.get('page', 1)
        try:
            shipments = paginator.page(page)
        except PageNotAnInteger:
            shipments = paginator.page(1)
        except EmptyPage:
            shipments = paginator.page(paginator.num_pages)

    display_pages = len(shipments) > 1
    return render_to_response(
        'warehouse/shipment-view.html',
        {
            'shipments': shipments,
            'display_pages': display_pages,
        },
        context_instance=RequestContext(request)
    )


def shipment_create(request):
    """receive a shipment"""
    form = ShipmentForm()
    formset = ShipmentProductFormset(instance=Shipment())

    if request.method == 'GET':
        form.fields['received_by'].initial = request.user
        received = [x.purchase_order.id for x in Shipment.objects.all()]
        form.fields['purchase_order'].queryset = PurchaseOrder.objects.all().exclude(id__in=received)
        for _form in formset:
            _form.fields['product'].queryset = PurchaseOrderProduct.objects.filter(id=-1)

    else:
        form = ShipmentForm(request.POST)
        if form.is_valid():
            ship = form.save(commit=False)
            formset = ShipmentProductFormset(request.POST, instance=ship)
            if formset.is_valid():
                ship.save()
                formset.save()
                return redirect(reverse('warehouse:shipment-view'))

    return render_to_response(
        'warehouse/shipment-create.html',
        {
            'form': form,
            'formset': formset,
        },
        context_instance=RequestContext(request)
    )
