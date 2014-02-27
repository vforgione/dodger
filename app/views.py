import csv
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.template.defaultfilters import slugify
from pytz import timezone

from forms import *
from models import *


PAGE_SIZE = 20

TZ = timezone('America/Chicago')


##
# search
@login_required
def search(request):
    q = request.GET.get('q', None)

    skus = Sku.objects.all()

    if q:
        attrs = [obj.sku.id for obj in SkuAttribute.objects.filter(value=q)]

        skus = skus.filter(
            Q(id__icontains=q) |
            Q(name__icontains=q) |
            Q(upc__icontains=q) |
            Q(location__icontains=q) |
            Q(brand__name__icontains=q) |
            Q(owner__username__icontains=q) |
            Q(supplier__name__icontains=q) |
            Q(supplier_sku__icontains=q) |
            Q(id__in=attrs)
        )

    return render_to_response(
        'app/search.html',
        {
            'skus': skus,
        },
        context_instance=RequestContext(request)
    )


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
def filter_cost_adjs(request):
    creator = request.GET.get('creator', None)
    skus = request.GET.get('skus', None)
    start = request.GET.get('start', None)
    end = request.GET.get('end', None)

    adjs = CostAdjustment.objects.order_by('-created')
    warnings = []
    params = {}

    if creator:
        adjs = adjs.filter(who__id=creator)
        params['Creator'] = get_object_or_404(User, id=creator)

    if skus:
        adjs = adjs.filter(sku__id__in=[sku.rstrip() for sku in skus.split(',')])
        params['SKUs'] = skus

    if start and end:
        s, e = start, end
        start = datetime(*(int(x) for x in start.split('-')), hour=0, minute=0, second=0, tzinfo=TZ)
        end = datetime(*(int(x) for x in end.split('-')), hour=23, minute=59, second=59, tzinfo=TZ)
        adjs = adjs.filter(created__range=[start, end])
        params['Date Created Range'] = '%s to %s' % (s, e)

    return adjs, warnings, params


@login_required
def cost_adjustment__table(request):
    adjs, warnings, params = filter_cost_adjs(request)

    paginator = Paginator(adjs, PAGE_SIZE)
    page = request.GET.get('page', 1)
    try:
        adjs = paginator.page(page)
    except PageNotAnInteger:
        adjs = paginator.page(1)
    except EmptyPage:
        adjs = paginator.page(paginator.num_pages)

    creators = User.objects.all()

    return render_to_response(
        'app/cost_adjustment__table.html',
        {
            'adjs': adjs,
            'warnings': warnings,
            'params': params,
            'creators': creators,
        },
        context_instance=RequestContext(request)
    )


@login_required
def cost_adjustment__export(request):
    adjs, _, params = filter_cost_adjs(request)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="cost_adjs__%s.csv"' % \
          '_'.join([slugify(p) for p in params.values()])

    writer = csv.writer(response)
    writer.writerow([
        'id', 'creator', 'sku', 'old', 'new', 'reason', 'detail', 'date'
    ])

    for adj in adjs:
        writer.writerow([
            adj.id, adj.who.username, adj.sku.id, adj.old, adj.new, adj.reason.name, adj.detail,
            adj.created.strftime('%m/%d/%Y')
        ])

    return response


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
def filter_qty_adjs(request):
    creator = request.GET.get('creator', None)
    skus = request.GET.get('skus', None)
    start = request.GET.get('start', None)
    end = request.GET.get('end', None)

    adjs = QuantityAdjustment.objects.order_by('-created')
    warnings = []
    params = {}

    if creator:
        adjs = adjs.filter(who__id=creator)
        params['Creator'] = get_object_or_404(User, id=creator)

    if skus:
        adjs = adjs.filter(sku__id__in=[sku.rstrip() for sku in skus.split(',')])
        params['SKUs'] = skus

    if start and end:
        s, e = start, end
        start = datetime(*(int(x) for x in start.split('-')), hour=0, minute=0, second=0, tzinfo=TZ)
        end = datetime(*(int(x) for x in end.split('-')), hour=23, minute=59, second=59, tzinfo=TZ)
        adjs = adjs.filter(created__range=[start, end])
        params['Date Created Range'] = '%s to %s' % (s, e)

    return adjs, warnings, params


@login_required
def quantity_adjustment__table(request):
    adjs, warnings, params = filter_qty_adjs(request)

    paginator = Paginator(adjs, PAGE_SIZE)
    page = request.GET.get('page', 1)
    try:
        adjs = paginator.page(page)
    except PageNotAnInteger:
        adjs = paginator.page(1)
    except EmptyPage:
        adjs = paginator.page(paginator.num_pages)

    creators = User.objects.all()

    return render_to_response(
        'app/quantity_adjustment__table.html',
        {
            'adjs': adjs,
            'warnings': warnings,
            'params': params,
            'creators': creators,
        },
        context_instance=RequestContext(request)
    )


@login_required
def quantity_adjustment__export(request):
    adjs, _, params = filter_qty_adjs(request)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="qty_adjs__%s.csv"' % \
          '_'.join([slugify(p) for p in params.values()])

    writer = csv.writer(response)
    writer.writerow([
        'id', 'creator', 'sku', 'old', 'new', 'reason', 'detail', 'date'
    ])

    for adj in adjs:
        writer.writerow([
            adj.id, adj.who.username, adj.sku.id, adj.old, adj.new, adj.reason.name, adj.detail,
            adj.created.strftime('%m/%d/%Y')
        ])

    return response


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


@login_required
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
    params = {}

    if brand:
        skus = skus.filter(brand__id=brand)
        params['Brand'] = get_object_or_404(Brand, id=brand)

    if category:
        skus = skus.filter(categories__id=category)
        params['Category'] = get_object_or_404(Category, id=category)

    if owner:
        skus = skus.filter(owner__id=owner)
        params['Owner'] = get_object_or_404(User, id=owner)

    if supplier:
        skus = skus.filter(supplier__id=supplier)
        params['Supplier'] = get_object_or_404(Supplier, id=supplier)

    if in_live_deal in (0, 1):
        skus = skus.filter(in_live_deal=in_live_deal)
        params['In Live Deal'] = in_live_deal

    if name:
        skus = skus.filter(name__icontains=name)
        params['Name'] = name

    if quantity_on_hand:
        keywords = quantity_on_hand.split()
        params['Qty on Hand'] = quantity_on_hand

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

    return skus, warnings, params


@login_required
def sku__table(request):
    skus, warnings, params = filter_skus(request)

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
            'params': params,
            'brands': brands,
            'categories': categories,
            'owners': owners,
            'suppliers': suppliers,
        },
        context_instance=RequestContext(request)
    )

@login_required
def sku__export(request):
    skus, _, params = filter_skus(request)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="skus__%s.csv"' % \
          '_'.join([slugify(p) for p in params.values()])

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
def filter_pos(request):
    creator = request.GET.get('creator', None)
    supplier = request.GET.get('supplier', None)
    contact = request.GET.get('contact', None)
    notes = request.GET.get('notes', None)
    start = request.GET.get('start', None)
    end = request.GET.get('end', None)

    pos = PurchaseOrder.objects.order_by('-created')
    warnings = []
    params = {}

    if creator:
        pos = pos.filter(creator__id=creator)
        params['DAT Member'] = get_object_or_404(User, id=creator)

    if supplier:
        pos = pos.filter(supplier__id=supplier)
        params['Supplier'] = get_object_or_404(Supplier, id=supplier)

    if contact:
        pos = pos.filter(contact__id=contact)
        params['Contact'] = get_object_or_404(Contact, id=contact)

    if notes:
        orig = len(pos)
        pos = pos.filter(notes__icontains=notes)
        params['Notes (contains)'] = notes
        if len(pos) == orig:
            warnings.append('No POs contained "%s" in their notes.' % notes)

    if start and end:
        s, e = start, end
        start = datetime(*(int(x) for x in start.split('-')), hour=0, minute=0, second=0, tzinfo=TZ)
        end = datetime(*(int(x) for x in end.split('-')), hour=23, minute=59, second=59, tzinfo=TZ)
        pos = pos.filter(created__range=[start, end])
        params['Date Created Range'] = '%s to %s' % (s, e)

    return pos, warnings, params


@login_required
def purchase_order__table(request):
    pos, warnings, params = filter_pos(request)

    paginator = Paginator(pos, PAGE_SIZE)
    page = request.GET.get('page', 1)
    try:
        pos = paginator.page(page)
    except PageNotAnInteger:
        pos = paginator.page(1)
    except EmptyPage:
        pos = paginator.page(paginator.num_pages)

    creators = User.objects.all()
    suppliers = Supplier.objects.all()
    contacts = Contact.objects.all()

    return render_to_response(
        'app/purchase_order__table.html',
        {
            'pos': pos,
            'warnings': warnings,
            'params': params,
            'creators': creators,
            'suppliers': suppliers,
            'contacts': contacts,
        },
        context_instance=RequestContext(request)
    )


@login_required
def purchase_order__export(request):
    pos, _, params = filter_pos(request)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="pos__%s.csv"' % \
          '_'.join([slugify(p) for p in params.values()])

    writer = csv.writer(response)
    writer.writerow([
        'id', 'date created', 'dat member', 'supplier', 'contact', 'receiver', 'terms', 'expected arrival', 'note',
        'shipment ids'
    ])

    for po in pos:
        writer.writerow([
            po.id, po.created.strftime('%m/%d/%Y'), po.creator.username, po.supplier.name, po.contact.name,
            po.receiver.name, po.terms, po.expected_arrival, po.note,
            ', '.join([str(s.id) for s in po.shipment_set.all()])
        ])

    return response


##
# purchase order line items
@login_required
def filter_po_lis(request):
    pos = request.GET.get('pos', None)
    skus = request.GET.get('skus', None)
    start = request.GET.get('start', None)
    end = request.GET.get('end', None)

    lis = PurchaseOrderLineItem.objects.order_by('-purchase_order__id')
    warnings = []
    params = {}

    if pos:
        lis = lis.filter(purchase_order__id__in=[po.rstrip() for po in pos.split(',')])
        params['POs'] = pos

    if skus:
        lis = lis.filter(sku__id__in=[sku.rstrip() for sku in skus.split(',')])
        params['SKUs'] = skus

    if start and end:
        s, e = start, end
        start = datetime(*(int(x) for x in start.split('-')), hour=0, minute=0, second=0, tzinfo=TZ)
        end = datetime(*(int(x) for x in end.split('-')), hour=23, minute=59, second=59, tzinfo=TZ)
        lis = lis.filter(purchase_order__created__range=[start, end])
        params['Date Created Range'] = '%s to %s' % (s, e)

    return lis, warnings, params


@login_required
def purchase_order_line_item__table(request):
    lis, warnings, params = filter_po_lis(request)

    paginator = Paginator(lis, PAGE_SIZE)
    page = request.GET.get('page', 1)
    try:
        lis = paginator.page(page)
    except PageNotAnInteger:
        lis = paginator.page(1)
    except EmptyPage:
        lis = paginator.page(paginator.num_pages)

    return render_to_response(
        'app/purchase_order_line_item__table.html',
        {
            'lis': lis,
            'warnings': warnings,
            'params': params,
        },
        context_instance=RequestContext(request)
    )


@login_required
def purchase_order_line_item__export(request):
    lis, _, params = filter_po_lis(request)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="po_line_items__%s.csv"' % \
          '_'.join([slugify(p) for p in params.values()])

    writer = csv.writer(response)
    writer.writerow([
        'po id', 'sku id', 'qty ordered', 'disc percent', 'disc dollar'
    ])

    for li in lis:
        writer.writerow([
            li.purchase_order.id, li.sku.id, li.quantity_ordered, li.discount_percent, li.discount_dollar
        ])

    return response


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


def filter_shipments(request):
    creator = request.GET.get('creator', None)
    pos = request.GET.get('pos', None)
    start = request.GET.get('start', None)
    end = request.GET.get('end', None)

    ships = Shipment.objects.order_by('-created')
    warnings = []
    params = {}

    if creator:
        ships = ships.filter(creator__id=creator)
        params['Received By'] = get_object_or_404(User, id=creator)

    if pos:
        ships = ships.filter(purchase_order__id__in=[po.rstrip() for po in pos.split(',')])
        params['POs'] = pos

    if start and end:
        s, e = start, end
        start = datetime(*(int(x) for x in start.split('-')), hour=0, minute=0, second=0, tzinfo=TZ)
        end = datetime(*(int(x) for x in end.split('-')), hour=23, minute=59, second=59, tzinfo=TZ)
        ships = ships.filter(created__range=[start, end])
        params['Date Created Range'] = '%s to %s' % (s, e)

    return ships, warnings, params


@login_required
def shipment__table(request):
    ships, warnings, params = filter_shipments(request)

    paginator = Paginator(ships, PAGE_SIZE)
    page = request.GET.get('page', 1)
    try:
        ships = paginator.page(page)
    except PageNotAnInteger:
        ships = paginator.page(1)
    except EmptyPage:
        ships = paginator.page(paginator.num_pages)

    creators = User.objects.all()

    return render_to_response(
        'app/shipment__table.html',
        {
            'ships': ships,
            'warnings': warnings,
            'params': params,
            'creators': creators,
        },
        context_instance=RequestContext(request)
    )


@login_required
def shipment__export(request):
    ships, _, params = filter_shipments(request)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="pos__%s.csv"' % \
          '_'.join([slugify(p) for p in params.values()])

    writer = csv.writer(response)
    writer.writerow([
        'id', 'date received', 'received by', 'po id', 'note'
    ])

    for ship in ships:
        writer.writerow([
            ship.id, ship.created.strftime('%m/%d/%Y'), ship.creator.username, ship.purchase_order.id, ship.note
        ])

    return response


##
# shipment line items
@login_required
def filter_sh_lis(request):
    pos = request.GET.get('pos', None)
    skus = request.GET.get('skus', None)
    start = request.GET.get('start', None)
    end = request.GET.get('end', None)

    lis = ShipmentLineItem.objects.order_by('-shipment__purchase_order__id')
    warnings = []
    params = {}

    if pos:
        lis = lis.filter(shipment__purchase_order__id__in=[po.rstrip() for po in pos.split(',')])
        params['POs'] = pos

    if skus:
        lis = lis.filter(sku__id__in=[sku.rstrip() for sku in skus.split(',')])
        params['SKUs'] = skus

    if start and end:
        s, e = start, end
        start = datetime(*(int(x) for x in start.split('-')), hour=0, minute=0, second=0, tzinfo=TZ)
        end = datetime(*(int(x) for x in end.split('-')), hour=23, minute=59, second=59, tzinfo=TZ)
        lis = lis.filter(shipment__created__range=[start, end])
        params['Date Created Range'] = '%s to %s' % (s, e)

    return lis, warnings, params


@login_required
def shipment_line_item__table(request):
    lis, warnings, params = filter_sh_lis(request)

    paginator = Paginator(lis, PAGE_SIZE)
    page = request.GET.get('page', 1)
    try:
        lis = paginator.page(page)
    except PageNotAnInteger:
        lis = paginator.page(1)
    except EmptyPage:
        lis = paginator.page(paginator.num_pages)

    return render_to_response(
        'app/shipment_line_item__table.html',
        {
            'lis': lis,
            'warnings': warnings,
            'params': params,
        },
        context_instance=RequestContext(request)
    )


@login_required
def shipment_line_item__export(request):
    lis, _, params = filter_sh_lis(request)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sh_line_items__%s.csv"' % \
          '_'.join([slugify(p) for p in params.values()])

    writer = csv.writer(response)
    writer.writerow([
        'po id', 'sku id', 'qty received'
    ])

    for li in lis:
        writer.writerow([
            li.shipment.purchase_order.id, li.sku.id, li.quantity_received
        ])

    return response
