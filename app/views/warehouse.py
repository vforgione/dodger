from django.contrib.auth.decorators import login_required
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext

from app.forms import SkuQuantityAdjustmentForm, ShipmentForm, ShipmentLineItemFormset
from app.models import SkuQuantityAdjustment, Sku, Shipment, PurchaseOrder


PAGE_SIZE = 20


# sku qty adjustments
@login_required
def sku_qty_adj__view(request, pk=None):
    adj, adjs = None, None

    if pk:
        adj = get_object_or_404(SkuQuantityAdjustment, pk=pk)

    else:
        adjs = SkuQuantityAdjustment.objects.order_by('-when')
        paginator = Paginator(adjs, PAGE_SIZE)
        page = request.GET.get('page', 1)
        try:
            adjs = paginator.page(page)
        except PageNotAnInteger:
            adjs = paginator.page(1)
        except EmptyPage:
            adjs = paginator.page(paginator.num_pages)

    return render_to_response(
        'app/warehouse/sku_qty_adj__view.html',
        {
            'adj': adj,
            'adjs': adjs,
        },
        context_instance=RequestContext(request)
    )


@login_required
def sku_qty_adj__create(request):
    form = SkuQuantityAdjustmentForm()

    if request.method == 'GET':
        form.fields['who'].initial = request.user
        form.fields['sku'].queryset = Sku.objects.filter(~Q(name='')).order_by('brand__name')

    else:
        form = SkuQuantityAdjustmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('app:sku_qty_adj__view'))

    return render_to_response(
        'app/warehouse/sku_qty_adj__create.html',
        {
            'form': form,
        },
        context_instance=RequestContext(request)
    )


# shipments
@login_required
def shipment__view(request, pk=None):
    shipment, shipments = None, None

    if pk:
        shipment = get_object_or_404(Shipment, pk=pk)

    else:
        shipments = Shipment.objects.order_by('-received_on')
        paginator = Paginator(shipments, PAGE_SIZE)
        page = request.GET.get('page', 1)
        try:
            shipments = paginator.page(page)
        except PageNotAnInteger:
            shipments = paginator.page(1)
        except EmptyPage:
            shipments = paginator.page(paginator.num_pages)

    return render_to_response(
        'app/warehouse/shipment__view.html',
        {
            'shipment': shipment,
            'shipments': shipments,
        },
        context_instance=RequestContext(request)
    )


@login_required
def shipment__create(request):
    form = ShipmentForm()
    formset = ShipmentLineItemFormset(instance=Shipment())
    no_pos = False

    if request.method == 'GET':
        form.fields['received_by'].initial = request.user
        received = [x.purchase_order.id for x in Shipment.objects.all()]
        form.fields['purchase_order'].queryset = PurchaseOrder.objects.all().exclude(id__in=received)
        no_pos = len(form.fields['purchase_order'].queryset) == 0
        for _form in formset:
            _form.fields['sku'].queryset = Sku.objects.filter(id=-1)

    else:
        form = ShipmentForm(request.POST)
        if form.is_valid():
            ship = form.save(commit=False)
            formset = ShipmentLineItemFormset(request.POST, instance=ship)
            if formset.is_valid():
                ship.save()
                formset.save()
                return redirect(reverse('app:shipment__view'))

    return render_to_response(
        'app/warehouse/shipment__create.html',
        {
            'form': form,
            'formset': formset,
            'no_pos': no_pos,
        },
        context_instance=RequestContext(request)
    )
