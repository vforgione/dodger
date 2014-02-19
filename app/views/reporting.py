import csv

from django.contrib.auth.decorators import login_required
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from app.models import PurchaseOrderLineItem, Sku, SkuAttribute


PAGE_SIZE = 50


# skus
@login_required
def sku__table(request):

    name = request.GET.get('name', None)
    category = request.GET.get('category', None)
    brand = request.GET.get('brand', None)
    owner = request.GET.get('owner', None)

    skus = Sku.objects.order_by('-id')
    params = []

    if name:
        skus = skus.filter(name__icontains=name)
        params.append(name)

    if category:
        skus = skus.filter(categories__name__icontains=category)
        params.append(category)

    if brand:
        skus = skus.filter(brand__name__icontains=brand)
        params.append(brand)

    if owner:
        skus = skus.filter(owner__username__icontains=owner)
        params.append(owner)

    paginator = Paginator(skus, PAGE_SIZE)
    page = request.GET.get('page', 1)
    try:
        skus = paginator.page(page)
    except PageNotAnInteger:
        skus = paginator.page(1)
    except EmptyPage:
        skus = paginator.page(paginator.num_pages)

    return render_to_response(
        'app/reporting/sku__table.html',
        {
            'skus': skus,
            'params': params,
        },
        context_instance=RequestContext(request)
    )


@login_required
def sku__export(request):
    name = request.GET.get('name', None)
    category = request.GET.get('category', None)
    brand = request.GET.get('brand', None)
    owner = request.GET.get('owner', None)

    skus = Sku.objects.order_by('-id')
    params = []

    if name:
        skus = skus.filter(name__icontains=name)
        params.append(name)

    if category:
        skus = skus.filter(categories__name__icontains=category)
        params.append(category)

    if brand:
        skus = skus.filter(brand__name__icontains=brand)
        params.append(brand)

    if owner:
        skus = skus.filter(owner__username__icontains=owner)
        params.append(owner)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="skus__%s.csv"' % '_'.join(params)

    writer = csv.writer(response)
    writer.writerow([
        'id', 'name', 'categories', 'supplier', 'brand', 'owner', 'reorder threshold', 'notify at threshold', 'cost',
        'mfr sku', 'case qty', 'location', 'qty on hand', 'in live deal', 'created', 'updated', 'color', 'size',
        'style', 'flavor', 'weight', 'is bulk', 'expiration date', 'country of origin'
    ])

    for sku in skus:
        attrs = SkuAttribute.objects.filter(sku__id=sku.id)
        attrs = dict((attr.attribute.name, attr.value) for attr in attrs)
        writer.writerow([
            sku.id, sku.name, ', '.join([cat.name for cat in sku.categories.all()]), sku.supplier, sku.brand, sku.owner.username,
            sku.reorder_threshold, sku.notify_at_threshold, sku.cost, sku.mfr_sku, sku.case_qty, sku.location,
            sku.qty_on_hand, sku.in_live_deal, sku.created.strftime('%m/%d/%Y'), sku.modified.strftime('%m/%d/%Y'),
            attrs.get('Color', ''), attrs.get('Size', ''), attrs.get('Style', ''), attrs.get('Flavor', ''),
            attrs.get('Weight', ''), attrs.get('Is Bulk', ''), attrs.get('Expiration Date', ''),
            attrs.get('Country of Origin', '')
        ])

    return response


# purchase orders reports
@login_required
def po__export(request):

    if request.method == 'POST':
        return redirect('/purchase-order/csv/%s/%s/' % (request.POST['start'], request.POST['end']))

    return render_to_response(
        'app/reporting/po__export.html',
        {},
        context_instance=RequestContext(request)
    )


@login_required
def po__csv(request, start, end):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="purchase_orders__%s__%s.csv"' % (start, end)

    items = PurchaseOrderLineItem.objects.filter(
        purchase_order__created__gte=start, purchase_order__created__lte=end
    )

    writer = csv.writer(response)
    writer.writerow([
        'po id', 'sku id', 'qty ordered', 'unit cost', 'line disc dollar', 'line disc percent', 'line total', 'date'
    ])
    for item in items:
        if item.disc_percent:
            dp = float(item.disc_percent) / 100
        else:
            dp = 0.0
        if item.disc_dollar:
            dd = float(item.disc_dollar)
        else:
            dd = 0.0
        total = (item.qty_ordered * float(item.unit_cost) - dd) * (1 - dp)
        writer.writerow([
            item.purchase_order.id, item.sku.id, item.qty_ordered, item.unit_cost, dd, dp, total,
            item.purchase_order.created.strftime('%x')
        ])

    return response
