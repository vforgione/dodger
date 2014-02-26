import csv

from django.contrib.auth.decorators import login_required
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext

from forms import *
from models import *


PAGE_SIZE = 20


## adjustments
# cost adjustments
@login_required
def cost_adjustment__view(request, pk=None):
    adj, adjs = None, None

    if pk is not None:
        adj = get_object_or_404(CostAdjustment, pk=pk)

    else:
        adjs = CostAdjustment.objects.order_by('-created')
        paginator = Paginator(adjs, PAGE_SIZE)
        page = request.GET.get('page', 1)
        try:
            adjs = paginator.page(page)
        except PageNotAnInteger:
            adjs = paginator.page(1)
        except EmptyPage:
            adjs = paginator.page(paginator.num_pages)

    return render_to_response(
        'app/cost_adjustment__view.html',
        {
            'adj': adj,
            'adjs': adjs,
        },
        context_instance=RequestContext(request)
    )


@login_required
def cost_adjustment__create(request):
    if request.method == 'GET':
        form = CostAdjustmentForm()
        form.fields['who'].initial = request.user
        form.fields['sku'].queryset = Sku.objects.filter(~Q(name='')).order_by('brand__name')

    else:
        form = CostAdjustmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('app:cost_adjustment__view'))

    return render_to_response(
        'app/cost_adjustment__create.html',
        {
            'form': form,
        },
        context_instance=RequestContext(request)
    )


@login_required
def cost_adjustment__table(request):
    pass


@login_required
def cost_adjustment__export(request):
    pass


# qty adjustments
@login_required
def quantity_adjustment__view(request, pk=None):
    adj, adjs = None, None

    if pk is not None:
        adj = get_object_or_404(QuantityAdjustment, pk=pk)

    else:
        adjs = QuantityAdjustment.objects.order_by('-created')
        paginator = Paginator(adjs, PAGE_SIZE)
        page = request.GET.get('page', 1)
        try:
            adjs = paginator.page(page)
        except PageNotAnInteger:
            adjs = paginator.page(1)
        except EmptyPage:
            adjs = paginator.page(paginator.num_pages)

    return render_to_response(
        'app/quantity_adjustment__view.html',
        {
            'adj': adj,
            'adjs': adjs,
        },
        context_instance=RequestContext(request)
    )


@login_required
def quantity_adjustment__create(request):
    print 'barf'
    if request.method == 'GET':
        form = QuantityAdjustmentForm()
        form.fields['who'].initial = request.user
        form.fields['sku'].queryset = Sku.objects.filter(~Q(name='')).order_by('brand__name')

    else:
        form = QuantityAdjustmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('app:quantity_adjustment__view'))

    return render_to_response(
        'app/quantity_adjustment__create.html',
        {
            'form': form,
        },
        context_instance=RequestContext(request)
    )


@login_required
def quantity_adjustment__table(request):
    pass


@login_required
def quantity_adjustment__export(request):
    pass


##
# skus
@login_required
def sku__view(request, pk=None):
    sku, skus = None, None

    if pk is not None:
        sku = get_object_or_404(Sku, pk=pk)

    else:
        skus = Sku.objects.order_by('-created')
        paginator = Paginator(skus, PAGE_SIZE)
        page = request.GET.get('page', 1)
        try:
            skus = paginator.page(page)
        except PageNotAnInteger:
            skus = paginator.page(1)
        except EmptyPage:
            skus = paginator.page(paginator.num_pages)

    return render_to_response(
        'app/sku__view.html',
        {
            'sku': sku,
            'skus': skus,
        },
        context_instance=RequestContext(request)
    )


@login_required
def sku__create(request):
    if request.method == 'GET':
        form = SkuForm()
        form.fields['owner'].initial = request.user

        formset = SkuAttributeFormset(instance=Sku())

    else:
        form = SkuForm(request.POST)
        if form.is_valid():
            sku = form.save(commit=False)
            formset = SkuAttributeFormset(request.POST, instance=sku)
            if formset.is_valid():
                sku.save()
                formset.save()
                return redirect(reverse('app:sku__view'))
        else:
            formset = SkuAttributeFormset(request.POST, instance=Sku())

    return render_to_response(
        'app/sku__create.html',
        {
            'form': form,
            'formset': formset,
        },
        context_instance=RequestContext(request)
    )


@login_required
def sku__update(request, pk=None):
    if pk is None:
        skus = Sku.objects.order_by('-created')
        paginator = Paginator(skus, PAGE_SIZE)
        page = request.GET.get('page', 1)
        try:
            skus = paginator.page(page)
        except PageNotAnInteger:
            skus = paginator.page(1)
        except EmptyPage:
            skus = paginator.page(paginator.num_pages)

        return render_to_response(
            'app/sku__update.html',
            {
                'sku': None,
                'skus': skus,
                'form': None,
                'formset': None,
            },
            context_instance=RequestContext(request)
        )

    else:
        sku = get_object_or_404(Sku, pk=pk)

    if request.method == 'GET':
        form = SkuForm(instance=sku)
        formset = SkuAttributeFormset(instance=sku)

    else:
        form = SkuForm(request.POST, instance=sku)
        if form.is_valid():
            updated = form.save(commit=False)
            formset = SkuAttributeFormset(request.POST, instance=sku)
            if formset.is_valid():
                updated.save()
                formset.save()
                return redirect(sku.get_absolute_url())
        else:
            formset = SkuAttributeFormset(request.POST, instance=sku)

    return render_to_response(
        'app/sku__update.html',
        {
            'sku': sku,
            'skus': None,
            'form': form,
            'formset': formset,
        },
        context_instance=RequestContext(request)
    )


def filter_skus(request):
    brand = request.GET.get('brand', None)
    category = request.GET.get('category', None)
    owner = request.GET.get('owner', None)
    supplier = request.GET.get('supplier', None)
    in_live_deal = request.GET.get('in_live_deal', None)
    name = request.GET.get('name', None)  # icontains
    quantity_on_hand = request.GET.get('quantity_on_hand', None)  # parse and apply filter

    skus = Sku.objects.order_by('id')

    warnings = []

    if brand:
        skus = skus.filter(brand__id=brand)

    if category:
        skus = skus.filter(categories__id=category)

    if owner:
        skus = skus.filter(owner__id=owner)

    if supplier:
        skus = skus.filter(supplier__id=supplier)

    if in_live_deal in (0, 1):
        skus = skus.filter(in_live_deal=in_live_deal)

    if name:
        skus = skus.filter(name__icontains=name)

    if quantity_on_hand:
        keywords = quantity_on_hand.split()

        if len(keywords) == 1:
            skus = skus.filter(quantity_on_hand=quantity_on_hand)

        else:
            if len(keywords) == 2:
                if keywords[0] == '>':
                    skus = skus.filter(quantity_on_hand__gt=keywords[1])
                elif keywords[0] == '>=':
                    skus = skus.filter(quantity_on_hand__gte=keywords[1])
                elif keywords[0] == '<':
                    skus = skus.filter(quantity_on_hand__lt=keywords[1])
                elif keywords[0] == '>=':
                    skus = skus.filter(quantity_on_hand__lte=keywords[1])
                else:
                    warnings.append('Could not parse quantity_on_hand = `%s`' % quantity_on_hand)

            elif len(keywords) == 5:
                try:
                    assert keywords[1] in ('>', '>=', '<', '<=')
                    assert keywords[3] in ('>', '>=', '<', '<=')
                except AssertionError:
                    warnings.append('Could not parse quantity_on_hand = `%s`' % quantity_on_hand)

                min_val = int(keywords[0])
                max_val = int(keywords[4])
                min_op = keywords[1]
                max_op = keywords[3]

                kwargs = {}
                if min_op == '>':
                    kwargs['quantity_on_hand__lt'] = min_val
                elif min_op == '>=':
                    kwargs['quantity_on_hand__lte'] = min_val
                elif min_op == '<':
                    kwargs['quantity_on_hand__gt'] = min_val
                else:
                    kwargs['quantity_on_hand__gte'] = min_val

                if max_op == '>':
                    kwargs['quantity_on_hand__gt'] = max_val
                elif max_op == '>=':
                    kwargs['quantity_on_hand__gte'] = max_val
                elif max_op == '<':
                    kwargs['quantity_on_hand__lt'] = max_val
                else:
                    kwargs['quantity_on_hand__lte'] = max_val

                skus = skus.filter(**kwargs)

            else:
                warnings.append('Could not parse quantity_on_hand = `%s`' % quantity_on_hand)

    return skus, warnings


@login_required
def sku__table(request):

    skus, warnings = filter_skus(request)

    paginator = Paginator(skus, PAGE_SIZE)
    page = request.GET.get('page', 1)
    try:
        skus = paginator.page(page)
    except PageNotAnInteger:
        skus = paginator.page(1)
    except EmptyPage:
        skus = paginator.page(paginator.num_pages)

    brands = Brand.objects.all()
    categories = Category.objects.all()
    owners = User.objects.all()
    suppliers = Supplier.objects.all()

    return render_to_response(
        'app/sku__table.html',
        {
            'skus': skus,
            'warnings': warnings,
            'brands': brands,
            'categories': categories,
            'owners': owners,
            'suppliers': suppliers,
        },
        context_instance=RequestContext(request)
    )

@login_required
def sku__export(request):

    skus, _ = filter_skus(request)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="skus.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'id', 'name', 'upc', 'brand', 'categories', 'qty on hand', 'location', 'owner', 'supplier', 'lead time',
        'min qty', 'notify', 'cost', 'supplier sku', 'case qty', 'in live deal', 'color', 'size',
        'style', 'flavor', 'weight', 'is bulk', 'expiration date', 'country of origin', 'created', 'modified'
    ])

    for sku in skus:
        attrs = SkuAttribute.objects.filter(sku__id=sku.id)
        attrs = dict((attr.attribute.name, attr.value) for attr in attrs)
        writer.writerow([
            sku.id, sku.name, sku.upc, sku.brand.name, ', '.join([cat.name for cat in sku.categories.all()]),
            sku.quantity_on_hand, sku.location, sku.owner.username, sku.supplier.name, sku.lead_time,
            sku.minimum_quantity, sku.notify_at_threshold, sku.cost, sku.supplier_sku, sku.case_quantity,
            sku.in_live_deal, attrs.get('Color', ''), attrs.get('Size', ''), attrs.get('Style', ''),
            attrs.get('Flavor', ''), attrs.get('Weight', ''), attrs.get('Is Bulk', ''), attrs.get('Expiration Date', ''),
            attrs.get('Country of Origin', ''), sku.created.strftime('%m/%d/%Y'), sku.modified.strftime('%m/%d/%Y')
        ])

    return response


##
# purchase orders
@login_required
def purchase_order__view(request, pk=None):
    po, pos = None, None

    if pk is not None:
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
        'app/purchase_order__view.html',
        {
            'po': po,
            'pos': pos,
        },
        context_instance=RequestContext(request)
    )


@login_required
def purchase_order__create(request):
    if request.method == 'GET':
        form = PurchaseOrderForm()
        form.fields['creator'].initial = request.user
        form.fields['contact'].queryset = Contact.objects.filter(name='')

        formset = PurchaseOrderLineItemFormset(instance=PurchaseOrder())
        formset.forms[0].empty_permitted = False
        for f in formset:
            f.fields['sku'].queryset = Sku.objects.filter(id=-1)
            f.fields['unit_cost'].initial = ''

    else:
        form = PurchaseOrderForm(request.POST)
        if form.is_valid():
            po = form.save(commit=False)
            formset = PurchaseOrderLineItemFormset(request.POST, instance=po)
            formset.forms[0].empty_permitted = False
            if formset.is_valid():
                po.save()
                formset.save()
                return redirect(reverse('app:purchase_order__view'))
        else:
            formset = PurchaseOrderLineItemFormset(request.POST, instance=PurchaseOrder())

    return render_to_response(
        'app/purchase_order__create.html',
        {
            'form': form,
            'formset': formset,
        },
        context_instance=RequestContext(request)
    )


@login_required
def purchase_order__update(request, pk=None):
    if pk is None:
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
            'app/purchase_order__update.html',
            {
                'po': None,
                'pos': pos,
                'form': None,
                'formset': None,
            },
            context_instance=RequestContext(request)
        )

    else:
        po = get_object_or_404(PurchaseOrder, pk=pk)

    if request.method == 'GET':
        form = PurchaseOrderForm(instance=po)
        formset = PurchaseOrderLineItemFormset(instance=po)

    else:
        form = PurchaseOrderForm(request.POST, instance=po)
        if form.is_valid():
            updated = form.save(commit=False)
            formset = PurchaseOrderLineItemFormset(request.POST, instance=po)
            if formset.is_valid():
                updated.save()
                formset.save()
                return redirect(po.get_absolute_url())
        else:
            formset = PurchaseOrderLineItemFormset(request.POST, instance=po)

    return render_to_response(
        'app/purchase_order__update.html',
        {
            'po': po,
            'pos': None,
            'form': form,
            'formset': formset,
        },
        context_instance=RequestContext(request)
    )


@login_required
def purchase_order__table(request):
    pass


@login_required
def purchase_order__export(request):
    pass


##
# shipments
@login_required
def shipment__view(request, pk=None):
    ship, ships = None, None

    if pk is not None:
        ship = get_object_or_404(Shipment, pk=pk)

    else:
        ships = Shipment.objects.order_by('-created')
        paginator = Paginator(ships, PAGE_SIZE)
        page = request.GET.get('page', 1)
        try:
            ships = paginator.page(page)
        except PageNotAnInteger:
            ships = paginator.page(1)
        except EmptyPage:
            ships = paginator.page(paginator.num_pages)

    return render_to_response(
        'app/shipment__view.html',
        {
            'ship': ship,
            'ships': ships,
        },
        context_instance=RequestContext(request)
    )


@login_required
def shipment__create(request):
    received = [po.id for po in PurchaseOrder.objects.all() if po.is_fully_received()]
    pos = PurchaseOrder.objects.filter(~Q(id__in=received))
    if not len(pos):
        return render_to_response(
            'app/shipment__create.html',
            {
                'form': None,
                'formset': None,
                'no_pos': True,
            },
            context_instance=RequestContext(request)
        )

    if request.method == 'GET':
        form = ShipmentForm()
        form.fields['creator'].initial = request.user
        form.fields['purchase_order'].queryset = pos

        formset = ShipmentLineItemFormset(instance=Shipment())
        for f in formset:
            f.fields['sku'].queryset = Sku.objects.filter(id=-1)

    else:
        form = ShipmentForm(request.POST)
        if form.is_valid():
            shipment = form.save(commit=False)
            formset = ShipmentLineItemFormset(request.POST, instance=shipment)
            if formset.is_valid():
                shipment.save()
                formset.save()
                return redirect(reverse('app:shipment__view'))
        else:
            formset = ShipmentLineItemFormset(request.POST, instance=Shipment())

    return render_to_response(
        'app/shipment__create.html',
        {
            'form': form,
            'formset': formset,
            'no_pos': False,
        },
        context_instance=RequestContext(request)
    )


@login_required
def shipment__update(request, pk=None):
    if pk is None:
        ships = Shipment.objects.order_by('-created')
        paginator = Paginator(ships, PAGE_SIZE)
        page = request.GET.get('page', 1)
        try:
            ships = paginator.page(page)
        except PageNotAnInteger:
            ships = paginator.page(1)
        except EmptyPage:
            ships = paginator.page(paginator.num_pages)

        return render_to_response(
            'app/shipment__update.html',
            {
                'ship': None,
                'ships': ships,
                'form': None,
                'formset': None,
            },
            context_instance=RequestContext(request)
        )

    else:
        ship = get_object_or_404(Shipment, pk=pk)

    if request.method == 'GET':
        form = ShipmentForm(instance=ship)
        formset = ShipmentLineItemFormset(instance=ship)

    else:
        form = ShipmentForm(request.POST, instance=ship)
        if form.is_valid():
            updated = form.save(commit=False)
            formset = ShipmentLineItemFormset(request.POST, instance=ship)
            if formset.is_valid():
                updated.save()
                formset.save()
                return redirect(ship.get_absolute_url())
        else:
            formset = ShipmentLineItemFormset(request.POST, instance=ship)

    return render_to_response(
        'app/shipment__update.html',
        {
            'ship': ship,
            'ships': None,
            'form': form,
            'formset': formset,
        },
        context_instance=RequestContext(request)
    )


@login_required
def shipment__table(request):
    pass


@login_required
def shipment__export(request):
    pass
