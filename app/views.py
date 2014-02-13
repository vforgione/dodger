from django.contrib.auth.decorators import login_required
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext

from .forms import *
from .models import *


PAGE_SIZE = 20


# sku qty adjustments
@login_required
def sku_qty_adj__view(request, pk=None):
    trace, traces = None, None

    if pk:
        trace = get_object_or_404(SkuQuantityAdjustment, pk=pk)

    else:
        traces = SkuQuantityAdjustment.objects.order_by('-when')
        paginator = Paginator(traces, PAGE_SIZE)
        page = request.GET.get('page', 1)
        try:
            traces = paginator.page(page)
        except PageNotAnInteger:
            traces = paginator.page(1)
        except EmptyPage:
            traces = paginator.page(paginator.num_pages)

    return render_to_response(
        'app/sku_qty_adj__view.html',
        {
            'trace': trace,
            'traces': traces,
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
        'app/sku_qty_adj__create.html',
        {
            'form': form,
        },
        context_instance=RequestContext(request)
    )


# purchase orders
@login_required
def po__view(request, pk=None):
    po, pos = None, None

    if pk:
        po = get_object_or_404(PurchaseOrder, pk=pk)

    else:
        pos = PurchaseOrder.objects.order_by('-created')
        paginator = Paginator(pos, PAGE_SIZE)
        page = request.GET.get('page', 1)
        try:
            pos = paginator.page(page)
        except PageNotAnInteger:
            pos = paginator.page(1)
        except EmptyPage:
            pos = paginator.page(paginator.num_pages)

    return render_to_response(
        'app/po__view.html',
        {
            'po': po,
            'pos': pos,
        },
        context_instance=RequestContext(request)
    )


@login_required
def po__create(request):
    form = PurchaseOrderForm()
    formset = PurchaseOrderLineItemFormset(instance=PurchaseOrder())

    if request.method == 'GET':
        form.fields['creator'].initial = request.user
        form.fields['contact'].queryset = Contact.objects.filter(name='')
        for _form in formset:
            _form.fields['sku'].queryset = Sku.objects.filter(name='projectile vomit')

    else:
        form = PurchaseOrderForm(request.POST)
        if form.is_valid():
            po = form.save(commit=False)
            formset = PurchaseOrderLineItemFormset(request.POST, instance=po)
            if formset.is_valid():
                po.save()
                formset.save()
                return redirect(reverse('app:po__view'))

    return render_to_response(
        'app/po__create.html',
        {
            'form': form,
            'formset': formset,
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
        'app/shipment__view.html',
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
        'app/shipment__create.html',
        {
            'form': form,
            'formset': formset,
            'no_pos': no_pos,
        },
        context_instance=RequestContext(request)
    )
