# -*- encoding: utf-8 -*-

from string import ascii_letters, digits
import csv
import codecs
from datetime import date, datetime, timedelta
import json
import sys

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.utils.html import escape
from pytz import timezone

from forms import *
from models import *
from notifications import *


PAGE_SIZE = 20

TZ = timezone('America/Chicago')


##
# home
def home(request):
    now = datetime.now()
    two_weeks_ago = now - timedelta(days=14)

    live_skus = Sku.objects.filter(in_live_deal=True)

    pos = PurchaseOrder.objects.filter(created__gte=two_weeks_ago)
    pos = [po for po in pos if not po.is_fully_received()]
    out_pos = []
    for po in pos:
        polis = dict([(li.sku.id, li.quantity_ordered) for li in po.purchaseorderlineitem_set.all()])
        slis = dict([(li.sku.id, li.quantity_received) for li in ShipmentLineItem.objects.filter(shipment__purchase_order=po)])
        for sku, qty in polis.iteritems():
            if sku in slis:
                if qty <= slis[sku]:
                    pass
                else:
                    out_pos.append((str(po), po.get_absolute_url(), sku, qty, slis[sku]))
            else:
                out_pos.append((str(po), po.get_absolute_url(), sku, qty, 0))

    awa = date.today() - timedelta(days=7)
    a_week_ago = datetime(awa.year, awa.month, awa.day)
    recent_shipments = Shipment.objects.filter(created__gte=a_week_ago)

    live_sku_alert = [sku for sku in Sku.objects.filter(in_live_deal=True, quantity_on_hand__lte=0)]
    if len(live_sku_alert):
        messages.add_message(
            request, messages.ERROR,
            '<b>The following SKUs are live on the site, but are reporting 0 qty:</b><br />%s' %
                ', '.join(['<a href="%s" target="_blank">%s</a>' % (s.get_absolute_url(), s.id) for s in live_sku_alert]),
            extra_tags='alert-danger'
        )

    location_alert = [sku for sku in Sku.objects.filter(in_live_deal=True, location__in=['', None])]
    if len(location_alert):
        messages.add_message(
            request, messages.ERROR,
            '<b>The following SKUs are live on the site, but do not have a location recorded:</b><br />%s' %
                ', '.join(['<a href="%s" target="_blank">%s</a>' % (s.get_absolute_url(), s.id) for s in location_alert]),
            extra_tags='alert-danger'
        )

    return render_to_response(
        'app/home.html',
        {
            'live_skus': live_skus,
            'out_pos': out_pos,
            'recent_shipments': recent_shipments,
        },
        context_instance=RequestContext(request)
    )


##
# search
@login_required
def search(request):
    q = request.GET.get('q', None)

    skus = Sku.objects.all()
    brands = Brand.objects.all()
    contacts = Contact.objects.all()
    suppliers = Supplier.objects.all()
    pos = PurchaseOrder.objects.all()
    shipments = Shipment.objects.all()
    qas = QuantityAdjustment.objects.all()
    cas = CostAdjustment.objects.all()

    if q:
        # hot phrases
        if q == 'live':
            skus = skus.filter(in_live_deal=True)
            brands = brands.filter(id=-1)
            contacts = contacts.filter(id=-1)
            suppliers = suppliers.filter(id=-1)
            shipments = shipments.filter(id=-1)
            pos = pos.filter(id=-1)
            qas = qas.filter(sku__in_libe_deal=True)
            cas = cas.filter(sku__in_libe_deal=True)

        elif q == 'subscription':
            skus = skus.filter(is_subscription=True)
            brands = brands.filter(id=-1)
            contacts = contacts.filter(id=-1)
            suppliers = suppliers.filter(id=-1)
            shipments = shipments.filter(id=-1)
            pos = pos.filter(id=-1)
            qas = qas.filter(sku__is_subscription=True)
            cas = cas.filter(sku__is_subscription=True)

        elif q == 'consignment':
            skus = skus.filter(action__icontains='consignment')
            brands = brands.filter(id=-1)
            contacts = contacts.filter(id=-1)
            suppliers = suppliers.filter(id=-1)
            shipments = shipments.filter(id=-1)
            pos = pos.filter(id=-1)
            qas = qas.filter(id=-1)
            cas = cas.filter(id=-1)

        elif q == 'clearance':
            skus = skus.filter(action__icontains='clearance')
            brands = brands.filter(id=-1)
            contacts = contacts.filter(id=-1)
            suppliers = suppliers.filter(id=-1)
            shipments = shipments.filter(id=-1)
            pos = pos.filter(id=-1)
            qas = qas.filter(sku__action__icontains='clearance')
            cas = cas.filter(sku__action__icontains='clearance')

        elif q == 'open pos':
            _pos = [po.id for po in pos if not po.is_fully_received()]
            pos = pos.filter(id__in=_pos)
            skus = skus.filter(id=-1)
            brands = brands.filter(id=-1)
            contacts = contacts.filter(id=-1)
            suppliers = suppliers.filter(id=-1)
            shipments = shipments.filter(id=-1)
            qas = qas.filter(id=-1)
            cas = cas.filter(id=-1)


        # full search
        else:
            attrs = [obj.sku.id for obj in SkuAttribute.objects.filter(value=q)]
            qa = [obj.sku.id for obj in
                  QuantityAdjustment.objects.filter(Q(reason__name__icontains=q) | Q(who__username__icontains=q))]
            ca = [obj.sku.id for obj in
                  CostAdjustment.objects.filter(Q(reason__name__icontains=q) | Q(who__username__icontains=q))]

            skus = skus.filter(
                Q(id__icontains=q) |
                Q(name__icontains=q) |
                Q(upc__icontains=q) |
                Q(location__icontains=q) |
                Q(last_location__icontains=q) |
                Q(brand__name__icontains=q) |
                Q(owner__username__icontains=q) |
                Q(supplier__name__icontains=q) |
                Q(supplier_sku__icontains=q) |
                Q(id__in=attrs) |
                Q(notes__icontains=q) |
                Q(id__in=qa) |
                Q(id__in=ca)
            )

            brands = brands.filter(name__icontains=q)

            contacts = contacts.filter(
                Q(name__icontains=q) |
                Q(represents__name__icontains=q) |
                Q(label__name__icontains=q) |
                Q(city__icontains=q) |
                Q(state__icontains=q) |
                Q(zipcode__icontains=q)
            )

            suppliers = suppliers.filter(
                Q(name__icontains=q) |
                Q(id__in=[c.represents.id for c in contacts])
            )

            poids = []
            for sku in skus:
                lis = sku.purchaseorderlineitem_set.all()
                for li in lis:
                    poids.append(li.purchase_order.id)
            pos = pos.filter(
                Q(id__icontains=q) |
                Q(supplier__name__icontains=q) |
                Q(contact__name__icontains=q) |
                Q(creator__username__icontains=q) |
                Q(id__in=poids) |
                Q(note__icontains=q) |
                Q(deal__icontains=q)
            )

            sids = []
            for sku in skus:
                lis = sku.shipmentlineitem_set.all()
                for li in lis:
                    sids.append(li.shipment.id)
            shipments = shipments.filter(
                Q(id__icontains=q) |
                Q(creator__username__icontains=q) |
                Q(id__in=sids) |
                Q(purchase_order__id__in=poids)
            )

            qas = qas.filter(
                Q(reason__name__icontains=q) |
                Q(detail__icontains=q) |
                Q(who__username__icontains=q)
            )

            cas = cas.filter(
                Q(reason__name__icontains=q) |
                Q(detail__icontains=q) |
                Q(who__username__icontains=q)
            )

    return render_to_response(
        'app/search.html',
        {
            'skus': skus.distinct(), 'sku_ids': ','.join([str(x.id) for x in skus]),
            'brands': brands.distinct(), 'brand_ids': ','.join([str(x.id) for x in brands]),
            'contacts': contacts.distinct(), 'contact_ids': ','.join([str(x.id) for x in contacts]),
            'suppliers': suppliers.distinct(), 'supp_ids': ','.join([str(x.id) for x in suppliers]),
            'pos': pos.distinct(), 'po_ids': ','.join([str(x.id) for x in pos]),
            'ships': shipments.distinct(), 'ship_ids': ','.join([str(x.id) for x in shipments]),
            'qas': qas.distinct(), 'qas_ids': ','.join([str(x.id) for x in qas]),
            'cas': cas.distinct(), 'ca_ids': ','.join([str(x.id) for x in cas]),
            'q': q,
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
    ids = request.GET.get('ids', None)

    adjs = CostAdjustment.objects.order_by('-created')
    warnings = []
    params = {}

    if ids:
        adjs = adjs.filter(id__in=[id for id in ids.split(',')])

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
    if request.method == 'GET':
        form = QuantityAdjustmentForm()
        form.fields['who'].initial = request.user

    else:
        chain = request.POST['submit'] == 'Save and Create Another Adjustment'
        form = QuantityAdjustmentForm(request.POST)
        if form.is_valid():
            form.save()
            loc = False
            if 'location' in request.POST and len(request.POST['location']):
                loc = True
                sku = Sku.objects.get(id=request.POST['sku'])
                sku.location = request.POST['location']
                sku.save()
            if str(request.POST['new']) == '0':
                sku = Sku.objects.get(id=request.POST['sku'])
                sku.location = None
                sku.save()
                try:
                    sa = SkuAttribute.objects.get(sku=sku, attribute__name='Expiration Date')
                    sa.delete()
                    messages.add_message(request, messages.INFO, "Expiration Date Deleted", extra_tags='alert-info')
                except SkuAttribute.DoesNotExist:
                    pass
            if chain:
                messages.add_message(request, messages.INFO, "Quantity Adjustment Saved", extra_tags='alert-info')
                if loc:
                    messages.add_message(request, messages.INFO, "Location Saved", extra_tags='alert-info')
                return redirect(reverse('app:quantity_adjustment__create'))
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
    ids = request.GET.get('ids', None)

    adjs = QuantityAdjustment.objects.order_by('-created')
    warnings = []
    params = {}

    if ids:
        adjs = adjs.filter(id__in=[id for id in ids.split(',')])

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


@login_required
def quantity_adjustment__mass_zero(request):
    if request.method == 'POST':
        skus = request.POST.getlist('skus')
        for sku in skus:
            sku = Sku.objects.get(id=sku)
            qa = QuantityAdjustment(
                sku=sku,
                new=0,
                reason=QuantityAdjustmentReason.objects.get(name='Done Deal'),
                who=request.user
            )
            try:
                qa.save()
            except Exception, e:
                messages.add_message(request, messages.ERROR, str(e), extra_tags='alert-danger')

        return redirect(reverse('app:quantity_adjustment__view'))


    return render_to_response(
        'app/quantity_adjustment__mass_zero.html',
        {},
        context_instance=RequestContext(request)
    )


##
# skus
@login_required
def sku__view(request, pk=None, order=None):
    sku, skus = None, None

    if pk is not None:
        sku = get_object_or_404(Sku, pk=pk)

    else:
        if order is None:
            order = '-id'
        skus = Sku.objects.order_by(order)
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
    is_popup = bool(request.GET.get('popup', 0))

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
                form.save_m2m()
                formset.save()
                if is_popup or 'popup' in request.REQUEST:
                    return HttpResponse('<script>opener.closeAddPopup(window, "%s", "%s");</script>' %
                                        (escape(sku.pk), escape(sku.description)))
                return redirect(reverse('app:sku__view'))
        else:
            formset = SkuAttributeFormset(request.POST, instance=Sku())

    return render_to_response(
        'app/sku__create.html',
        {
            'form': form,
            'formset': formset,
            'popup': is_popup,
        },
        context_instance=RequestContext(request)
    )


@login_required
def sku__clone(request, pk):
    existing = get_object_or_404(Sku, pk=pk)
    clone = Sku()
    clone.name = existing.name
    clone.upc = existing.upc
    clone.brand = existing.brand
    clone.quantity_on_hand = existing.quantity_on_hand
    clone.location = existing.location
    clone.owner = existing.owner
    clone.supplier = existing.supplier
    clone.lead_time = existing.lead_time
    clone.minimum_quantity = existing.minimum_quantity
    clone.notify_at_threshold = existing.notify_at_threshold
    clone.cost = existing.cost
    clone.supplier_sku = existing.supplier_sku
    clone.case_quantity = existing.case_quantity
    clone.in_live_deal = existing.in_live_deal
    clone.is_subscription = existing.is_subscription
    clone.notes = existing.notes
    clone.action = existing.action
    clone.action_date = existing.action_date
    clone.save()
    messages.add_message(request, messages.INFO, "SKU Cloned - Edit Attributes as Needed", extra_tags='alert-info')
    return redirect(reverse('app:sku__update', args=[str(clone.pk)]))


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
                form.save_m2m()
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
    expiration_date = request.GET.get('expiration_date', None)
    subscription = request.GET.get('is_subscription', None)
    ids = request.GET.get('ids', None)

    skus = Sku.objects.order_by('id')
    warnings = []
    params = {}

    if ids:
        skus = skus.filter(id__in=[id for id in ids.split(',')])
        params['ID'] = ', '.join(ids)

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

    if in_live_deal in ('0', '1', 0, 1):
        skus = skus.filter(in_live_deal=in_live_deal)
        params['In Live Deal'] = in_live_deal

    if name:
        skus = skus.filter(name__icontains=name)
        params['Name'] = name

    if subscription:
        skus = skus.filter(is_subscription=subscription)
        params['Is Subscription'] = subscription

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
                elif keywords[0] == '<=':
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

    if expiration_date:
        sku_ids = [attr.sku.id for attr in SkuAttribute.objects.filter(attribute__name='Expiration Date')]
        skus = skus.filter(id__in=sku_ids)

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

    attributes = [attr.name for attr in Attribute.objects.all()]
    fields = [
        'id', 'name', 'upc', 'brand', 'categories', 'qty on hand', 'location', 'last location', 'owner', 'supplier',
        'lead time', 'min qty', 'notify', 'cost', 'supplier sku', 'case qty', 'in live deal', 'subscription', 'notes',
        'action', 'action_date',
    ]
    fields.extend([a.lower() for a in attributes])
    fields.extend(['created', 'modified'])
    # print('\n\n' + str(fields) + '\n\n')

    writer = csv.writer(response)
    writer.writerow(fields)

    for sku in skus:
        attrs = SkuAttribute.objects.filter(sku__id=sku.id)
        attrs = dict((attr.attribute.name, attr.value) for attr in attrs)
        row = [
            sku.id, sku.name, sku.upc, sku.brand.name, ', '.join([cat.name for cat in sku.categories.all()]),
            sku.quantity_on_hand, sku.location, sku.last_location, sku.owner.username, sku.supplier.name, sku.lead_time,
            sku.minimum_quantity, sku.notify_at_threshold, sku.cost, sku.supplier_sku, sku.case_quantity,
            sku.in_live_deal, sku.is_subscription, sku.notes, sku.action, sku.action_date,
        ]
        for attr in attributes:
            row.append(attrs.get(attr, ''))
        row.extend([sku.created.strftime('%m/%d/%Y'), sku.modified.strftime('%m/%d/%Y')])
        # print('\n\n' + str(row) + '\n\n')
        for cell in row:
            if isinstance(cell, basestring):
                cell = ''.join([c for c in cell if c in ascii_letters+digits])
        try:
            writer.writerow(row)
        except Exception, e:
            sys.stderr.write(str(e))

    return response


def sku__locations(request):
    output = dict([(sku.id, sku.location) for sku in Sku.objects.all()])
    return HttpResponse(json.dumps(output), content_type='application/json')


##
# sku attributes
@login_required
def sku_attribute__delete(request, pk):
    sa = get_object_or_404(SkuAttribute, pk=pk)
    sku = sa.sku.pk
    sa.delete()
    return redirect(reverse('app:sku__update', args=[str(sku)]))


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
    deal = request.GET.get('deal', None)
    ids = request.GET.get('ids', None)

    pos = PurchaseOrder.objects.order_by('-created')
    warnings = []
    params = {}

    if ids:
        pos = pos.filter(id__in=[id for id in ids.split(',')])

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

    if deal:
        pos = pos.filter(deal__icontains=deal)
        params['Deal'] = deal

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
    response['Content-Disposition'] = 'attachment; filename="pos__%s.csv"' % '_'.join(
        [slugify(p) for p in params.values()])

    writer = csv.writer(response)
    writer.writerow([
        'id', 'deal', 'date created', 'dat member', 'supplier', 'contact', 'receiver', 'terms',
        'shipping_cost', 'sales_tax', 'total_cost', 'note', 'shipment ids', 'tracking url'
    ])

    for po in pos:
        writer.writerow([
            po.id, po.deal, po.created.strftime('%m/%d/%Y'), po.creator.username, po.supplier.name, po.contact.name,
            po.receiver.name, po.terms, po.shipping_cost, po.sales_tax, po.total_cost,
            po.note, ', '.join([str(s.id) for s in po.shipment_set.all()]), po.tracking_url
        ])

    return response


@login_required
def purchase_order__print(request, pk):
    po = get_object_or_404(PurchaseOrder, pk=pk)
    return render_to_response(
        'app/purchase_order__print.html',
        {
            'po': po,
        },
        context_instance=RequestContext(request)
    )


# purchase order line items
@login_required
def purchase_order_line_item__update(request, pk):
    li = get_object_or_404(PurchaseOrderLineItem, pk=pk)
    po = li.purchase_order

    if request.method == 'GET':
        form = PurchaseOrderLineItemForm(instance=li)
        form.fields['sku'].queryset = Sku.objects.filter(id=-1)
        form.fields['quantity_ordered'].initial = ''

    else:
        form = PurchaseOrderLineItemForm(request.POST, instance=li)
        if form.is_valid():
            form.save()
            return redirect(reverse('app:purchase_order__view', args=[str(li.purchase_order.pk)]))

    return render_to_response(
        'app/purchase_order_line_item__update.html',
        {
            'li': li,
            'po': po,
            'form': form,
        },
        context_instance=RequestContext(request)
    )


@login_required
def filter_po_lis(request):
    pos = request.GET.get('pos', None)
    skus = request.GET.get('skus', None)
    start = request.GET.get('start', None)
    end = request.GET.get('end', None)
    deal = request.GET.get('deal', None)
    ids = request.GET.get('ids', None)

    lis = PurchaseOrderLineItem.objects.order_by('-purchase_order__id')
    warnings = []
    params = {}

    if ids:
        lis = lis.filter(id__in=[id for id in ids.split(',')])

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

    if deal:
        lis = lis.filter(purchase_order__deal__icontains=deal)
        params['Deal'] = deal

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
    response['Content-Disposition'] = 'attachment; filename="po_line_items__%s.csv"' % '_'.join(
        [slugify(p) for p in params.values()])

    writer = csv.writer(response)
    writer.writerow([
        'po id', 'deal', 'sku id', 'qty ordered', 'disc percent', 'disc dollar'
    ])

    for li in lis:
        writer.writerow([
            li.purchase_order.id, li.purchase_order.deal, li.sku.id, li.quantity_ordered, li.discount_percent,
            li.discount_dollar
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
    pos = PurchaseOrder.objects.filter(~Q(id__in=received)).order_by('created')
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
                shipment_received(shipment.purchase_order.id, shipment, shipment.purchase_order.creator.email)
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
def filter_shipments(request):
    creator = request.GET.get('creator', None)
    pos = request.GET.get('pos', None)
    start = request.GET.get('start', None)
    end = request.GET.get('end', None)
    ids = request.GET.get('ids', None)

    ships = Shipment.objects.order_by('-created')
    warnings = []
    params = {}

    if ids:
        ships = ships.filter(id__in=[id for id in ids.split(',')])

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
    response['Content-Disposition'] = 'attachment; filename="ship__%s.csv"' % \
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


# shipment line items
@login_required
def shipment_line_item__update(request, pk):
    li = get_object_or_404(ShipmentLineItem, pk=pk)
    shipment = li.shipment

    if request.method == 'GET':
        form = ShipmentLineItemForm(instance=li)
        form.fields['sku'].queryset = Sku.objects.filter(id=-1)
        form.fields['quantity_received'].initial = ''

    else:
        form = ShipmentLineItemForm(request.POST, instance=li)
        if form.is_valid():
            # undo previous qty adj
            old_qa = QuantityAdjustment.objects.get(sku=li.sku, detail__contains='href="%s"' % li.shipment.get_absolute_url())
            qa = QuantityAdjustment(
                sku=li.sku,
                reason=QuantityAdjustmentReason.objects.get(name__icontains='rollback'),
                old=li.sku.quantity_on_hand,
                new=li.sku.quantity_on_hand - (old_qa.new - old_qa.old),
                who=request.user,
                detail='undoing adjustment %s -- updating shipping receipt' % old_qa.id
            )
            qa.save()
            # save line item
            form.save()
            return redirect(reverse('app:shipment__view', args=[str(li.shipment.pk)]))

    return render_to_response(
        'app/shipment_line_item__update.html',
        {
            'li': li,
            'shipment': shipment,
            'form': form,
        },
        context_instance=RequestContext(request)
    )


@login_required
def shipment_line_item__delete(request, pk):
    li = get_object_or_404(ShipmentLineItem, pk=pk)


@login_required
def filter_sh_lis(request):
    pos = request.GET.get('pos', None)
    skus = request.GET.get('skus', None)
    start = request.GET.get('start', None)
    end = request.GET.get('end', None)
    ids = request.GET.get('ids', None)

    lis = ShipmentLineItem.objects.order_by('-shipment__purchase_order__id')
    warnings = []
    params = {}

    if ids:
        lis = lis.filter(id__in=[id for id in ids.split(',')])

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


## control models
# attributes
@login_required
def attribute__view(request, pk=None):
    attr, attrs, update_url = None, None, None

    if pk is not None:
        attr = get_object_or_404(Attribute, pk=pk)
        update_url = reverse('app:attribute__update', args=[str(attr.pk)])

    else:
        attrs = Attribute.objects.order_by('name')
        paginator = Paginator(attrs, PAGE_SIZE)
        page = request.GET.get('page', 1)
        try:
            attrs = paginator.page(page)
        except PageNotAnInteger:
            attrs = paginator.page(1)
        except EmptyPage:
            attrs = paginator.page(paginator.num_pages)

    return render_to_response(
        'app/control_model__view.html',
        {
            'obj': attr,
            'objs': attrs,
            'model': 'Attribute',
            'list_url': reverse('app:attribute__view'),
            'update_url': update_url,
        },
        context_instance=RequestContext(request)
    )


@login_required
def attribute__create(request):
    form = AttributeForm()

    if request.method == 'POST':
        form = AttributeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('app:attribute__view'))

    return render_to_response(
        'app/control_model__create.html',
        {
            'form': form,
            'model': 'Attribute',
            'cancel': reverse('app:attribute__view'),
        },
        context_instance=RequestContext(request)
    )


@login_required
def attribute__update(request, pk=None):
    if pk is None:
        attrs = Attribute.objects.order_by('name')
        paginator = Paginator(attrs, PAGE_SIZE)
        page = request.GET.get('page', 1)
        try:
            attrs = paginator.page(page)
        except PageNotAnInteger:
            attrs = paginator.page(1)
        except EmptyPage:
            attrs = paginator.page(paginator.num_pages)

        return render_to_response(
            'app/control_model__update.html',
            {
                'obj': None,
                'objs': attrs,
                'form': None,
                'model': 'Attribute',
                'cancel': reverse('app:attribute__view'),
                'update_url': reverse('app:attribute__update'),
            },
            context_instance=RequestContext(request)
        )

    else:
        attr = get_object_or_404(Attribute, pk=pk)

    if request.method == 'GET':
        form = AttributeForm(instance=attr)

    else:
        form = AttributeForm(request.POST, instance=attr)
        if form.is_valid():
            form.save()
            return redirect(attr.get_absolute_url())

    return render_to_response(
        'app/control_model__update.html',
        {
            'obj': attr,
            'objs': None,
            'form': form,
            'model': 'Attribute',
            'cancel': reverse('app:attribute__view'),
            'update_url': reverse('app:attribute__update', args=[str(attr.pk)]),
        },
        context_instance=RequestContext(request)
    )


# brands
@login_required
def brand__view(request, pk=None):
    brand, brands, update_url = None, None, None

    if pk is not None:
        brand = get_object_or_404(Brand, pk=pk)
        update_url = reverse('app:brand__update', args=[str(brand.pk)])

    else:
        brands = Brand.objects.order_by('name')
        paginator = Paginator(brands, PAGE_SIZE)
        page = request.GET.get('page', 1)
        try:
            brands = paginator.page(page)
        except PageNotAnInteger:
            brands = paginator.page(1)
        except EmptyPage:
            brands = paginator.page(paginator.num_pages)

    return render_to_response(
        'app/control_model__view.html',
        {
            'obj': brand,
            'objs': brands,
            'model': 'Brand',
            'list_url': reverse('app:brand__view'),
            'update_url': update_url,
        },
        context_instance=RequestContext(request)
    )


@login_required
def brand__create(request):
    form = BrandForm()

    is_popup = bool(request.GET.get('popup', 0))

    if request.method == 'POST':
        form = BrandForm(request.POST)
        if form.is_valid():
            brand = form.save()
            if 'popup' in request.REQUEST:
                return HttpResponse('<script>opener.closeAddPopup(window, "%s", "%s");</script>' %
                                    (escape(brand.pk), escape(brand.name)))
            return redirect(reverse('app:brand__view'))

    return render_to_response(
        'app/control_model__create.html',
        {
            'form': form,
            'model': 'Brand',
            'cancel': reverse('app:brand__view'),
            'popup': is_popup,
        },
        context_instance=RequestContext(request)
    )


@login_required
def brand__update(request, pk=None):
    if pk is None:
        brands = Brand.objects.order_by('name')
        paginator = Paginator(brands, PAGE_SIZE)
        page = request.GET.get('page', 1)
        try:
            brands = paginator.page(page)
        except PageNotAnInteger:
            brands = paginator.page(1)
        except EmptyPage:
            brands = paginator.page(paginator.num_pages)

        return render_to_response(
            'app/control_model__update.html',
            {
                'obj': None,
                'objs': brands,
                'form': None,
                'model': 'Brand',
                'cancel': reverse('app:brand__view'),
                'update_url': reverse('app:brand__update'),
            },
            context_instance=RequestContext(request)
        )

    else:
        brand = get_object_or_404(Brand, pk=pk)

    if request.method == 'GET':
        form = BrandForm(instance=brand)

    else:
        form = BrandForm(request.POST, instance=brand)
        if form.is_valid():
            form.save()
            return redirect(brand.get_absolute_url())

    return render_to_response(
        'app/control_model__update.html',
        {
            'obj': brand,
            'objs': None,
            'form': form,
            'model': 'Brand',
            'cancel': reverse('app:brand__view'),
            'update_url': reverse('app:brand__update', args=[str(brand.pk)]),
        },
        context_instance=RequestContext(request)
    )


# categories
@login_required
def category__view(request, pk=None):
    cat, cats, update_url = None, None, None

    if pk is not None:
        cat = get_object_or_404(Category, pk=pk)
        update_url = reverse('app:category__view', args=[str(cat.pk)])

    else:
        cats = Category.objects.order_by('name')
        paginator = Paginator(cats, PAGE_SIZE)
        page = request.GET.get('page', 1)
        try:
            cats = paginator.page(page)
        except PageNotAnInteger:
            cats = paginator.page(1)
        except EmptyPage:
            cats = paginator.page(paginator.num_pages)

    return render_to_response(
        'app/control_model__view.html',
        {
            'obj': cat,
            'objs': cats,
            'model': 'Category',
            'list_url': reverse('app:category__view'),
            'update_url': update_url,
        },
        context_instance=RequestContext(request)
    )


@login_required
def category__create(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('app:category__view'))

    return render_to_response(
        'app/control_model__create.html',
        {
            'form': form,
            'model': 'Category',
            'cancel': reverse('app:category__view'),
        },
        context_instance=RequestContext(request)
    )


@login_required
def category__update(request, pk=None):
    if pk is None:
        cats = Category.objects.order_by('name')
        paginator = Paginator(cats, PAGE_SIZE)
        page = request.GET.get('page', 1)
        try:
            cats = paginator.page(page)
        except PageNotAnInteger:
            cats = paginator.page(1)
        except EmptyPage:
            cats = paginator.page(paginator.num_pages)

        return render_to_response(
            'app/control_model__update.html',
            {
                'obj': None,
                'objss': cats,
                'form': None,
                'model': 'Category',
                'update_url': reverse('app:category__update'),
            },
            context_instance=RequestContext(request)
        )

    else:
        cat = get_object_or_404(Category, pk=pk)

    if request.method == 'GET':
        form = CategoryForm(instance=cat)

    else:
        form = CategoryForm(request.POST, instance=cat)
        if form.is_valid():
            form.save()
            return redirect(cat.get_absolute_url())

    return render_to_response(
        'app/control_model__update.html',
        {
            'obj': cat,
            'objs': None,
            'form': form,
            'model': 'Category',
            'update_url': reverse('app:category__update', args=[str(cat.pk)]),
        },
        context_instance=RequestContext(request)
    )


# contact_labels
@login_required
def contact_label__view(request, pk=None):
    label, labels, update_url = None, None, None

    if pk is not None:
        label = get_object_or_404(ContactLabel, pk=pk)
        update_url = reverse('app:contact_label__update', args=[str(label.pk)])

    else:
        labels = ContactLabel.objects.order_by('name')
        paginator = Paginator(labels, PAGE_SIZE)
        page = request.GET.get('page', 1)
        try:
            labels = paginator.page(page)
        except PageNotAnInteger:
            labels = paginator.page(1)
        except EmptyPage:
            labels = paginator.page(paginator.num_pages)

    return render_to_response(
        'app/control_model__view.html',
        {
            'obj': label,
            'objs': labels,
            'model': 'Contact Label',
            'list_url': reverse('app:contact_label__view'),
            'update_url': update_url,
        },
        context_instance=RequestContext(request)
    )


@login_required
def contact_label__create(request):
    form = ContactLabelForm()

    if request.method == 'POST':
        form = ContactLabelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('app:contact_label__view'))

    return render_to_response(
        'app/control_model__create.html',
        {
            'form': form,
            'model': 'Contact Label',
            'cancel': reverse('app:contact_label__view'),
        },
        context_instance=RequestContext(request)
    )


@login_required
def contact_label__update(request, pk=None):
    if pk is None:
        labels = ContactLabel.objects.order_by('name')
        paginator = Paginator(labels, PAGE_SIZE)
        page = request.GET.get('page', 1)
        try:
            labels = paginator.page(page)
        except PageNotAnInteger:
            labels = paginator.page(1)
        except EmptyPage:
            labels = paginator.page(paginator.num_pages)

        return render_to_response(
            'app/control_model__update.html',
            {
                'obj': None,
                'objs': labels,
                'form': None,
                'model': 'Contact Label',
                'cancel': reverse('app:contact_label__view'),
                'update_url': reverse('app:contact_label__update')
            },
            context_instance=RequestContext(request)
        )

    else:
        label = get_object_or_404(ContactLabel, pk=pk)

    if request.method == 'GET':
        form = ContactLabelForm(instance=label)

    else:
        form = ContactLabelForm(request.POST, instance=label)
        if form.is_valid():
            form.save()
            return redirect(label.get_absolute_url())

    return render_to_response(
        'app/control_model__update.html',
        {
            'obj': label,
            'objs': None,
            'form': form,
            'model': 'Contact Label',
            'update_url': reverse('app:contact_label__update', args=[str(label.pk)])
        },
        context_instance=RequestContext(request)
    )


# cost_adjustment_reasons
@login_required
def cost_adjustment_reason__view(request, pk=None):
    adj, adjs, update_url = None, None, None

    if pk is not None:
        adj = get_object_or_404(CostAdjustmentReason, pk=pk)
        update_url = reverse('app:cost_adjustment_reason__update', args=[str(adj.pk)])

    else:
        adjs = CostAdjustmentReason.objects.order_by('name')
        paginator = Paginator(adjs, PAGE_SIZE)
        page = request.GET.get('page', 1)
        try:
            adjs = paginator.page(page)
        except PageNotAnInteger:
            adjs = paginator.page(1)
        except EmptyPage:
            adjs = paginator.page(paginator.num_pages)

    return render_to_response(
        'app/control_model__view.html',
        {
            'obj': adj,
            'objs': adjs,
            'model': 'Cost Adjustment Reason',
            'list_url': reverse('app:cost_adjustment_reason__view'),
            'update_url': update_url
        },
        context_instance=RequestContext(request)
    )


@login_required
def cost_adjustment_reason__create(request):
    form = CostAdjustmentReasonForm()

    if request.method == 'POST':
        form = CostAdjustmentReasonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('app:cost_adjustment_reason__view'))

    return render_to_response(
        'app/control_model__create.html',
        {
            'form': form,
            'model': 'Cost Adjustment Reason',
            'cancel': reverse('app:cost_adjustment_reason__view'),
        },
        context_instance=RequestContext(request)
    )


@login_required
def cost_adjustment_reason__update(request, pk=None):
    if pk is None:
        adjs = CostAdjustmentReason.objects.order_by('name')
        paginator = Paginator(adjs, PAGE_SIZE)
        page = request.GET.get('page', 1)
        try:
            adjs = paginator.page(page)
        except PageNotAnInteger:
            adjs = paginator.page(1)
        except EmptyPage:
            adjs = paginator.page(paginator.num_pages)

        return render_to_response(
            'app/control_model__update.html',
            {
                'obj': None,
                'objs': adjs,
                'form': None,
                'model': 'Cost Adjustment Reason',
                'cancel': reverse('app:cost_adjustment_reason__view'),
                'update_url': reverse('app:cost_adjustment_reason__update')
            },
            context_instance=RequestContext(request)
        )

    else:
        adj = get_object_or_404(CostAdjustmentReason, pk=pk)

    if request.method == 'GET':
        form = CostAdjustmentReasonForm(instance=adj)

    else:
        form = CostAdjustmentReasonForm(request.POST, instance=adj)
        if form.is_valid():
            form.save()
            return redirect(adj.get_absolute_url())

    return render_to_response(
        'app/control_model__update.html',
        {
            'obj': adj,
            'objs': None,
            'form': form,
            'model': 'Cost Adjustment Reason',
            'cancel': reverse('app:cost_adjustment_reason__view'),
            'update_url': reverse('app:cost_adjustment_reason__update', args=[str(adj.pk)])
        },
        context_instance=RequestContext(request)
    )


# quantity_adjustment_reasons
@login_required
def quantity_adjustment_reason__view(request, pk=None):
    adj, adjs, update_url = None, None, None

    if pk is not None:
        adj = get_object_or_404(QuantityAdjustmentReason, pk=pk)
        update_url = reverse('app:quantity_adjustment_reason__update', args=[str(adj.pk)])

    else:
        adjs = QuantityAdjustmentReason.objects.order_by('name')
        paginator = Paginator(adjs, PAGE_SIZE)
        page = request.GET.get('page', 1)
        try:
            adjs = paginator.page(page)
        except PageNotAnInteger:
            adjs = paginator.page(1)
        except EmptyPage:
            adjs = paginator.page(paginator.num_pages)

    return render_to_response(
        'app/control_model__view.html',
        {
            'obj': adj,
            'objs': adjs,
            'model': 'Quantity Adjustment Reason',
            'list_url': reverse('app:quantity_adjustment_reason__view'),
            'update_url': update_url
        },
        context_instance=RequestContext(request)
    )


@login_required
def quantity_adjustment_reason__create(request):
    form = QuantityAdjustmentReasonForm()

    if request.method == 'POST':
        form = QuantityAdjustmentReasonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('app:quantity_adjustment_reason__view'))

    return render_to_response(
        'app/control_model__create.html',
        {
            'form': form,
            'model': 'Quantity Adjustment Reason',
            'cancel': reverse('app:quantity_adjustment_reason__view'),
        },
        context_instance=RequestContext(request)
    )


@login_required
def quantity_adjustment_reason__update(request, pk=None):
    if pk is None:
        adjs = QuantityAdjustmentReason.objects.order_by('name')
        paginator = Paginator(adjs, PAGE_SIZE)
        page = request.GET.get('page', 1)
        try:
            adjs = paginator.page(page)
        except PageNotAnInteger:
            adjs = paginator.page(1)
        except EmptyPage:
            adjs = paginator.page(paginator.num_pages)

        return render_to_response(
            'app/control_model__update.html',
            {
                'obj': None,
                'objs': adjs,
                'form': None,
                'model': 'Quantity Adjustment Reason',
                'cancel': reverse('app:quantity_adjustment_reason__view'),
                'update_url': reverse('app:quantity_adjustment_reason__update')
            },
            context_instance=RequestContext(request)
        )

    else:
        adj = get_object_or_404(QuantityAdjustmentReason, pk=pk)

    if request.method == 'GET':
        form = QuantityAdjustmentReasonForm(instance=adj)

    else:
        form = QuantityAdjustmentReasonForm(request.POST, instance=adj)
        if form.is_valid():
            form.save()
            return redirect(adj.get_absolute_url())

    return render_to_response(
        'app/control_model__update.html',
        {
            'obj': adj,
            'objs': None,
            'form': form,
            'model': 'Quantity Adjustment Reason',
            'cancel': reverse('app:quantity_adjustment_reason__view'),
            'update_url': reverse('app:quantity_adjustment_reason__update', args=[str(adj.pk)]),
        },
        context_instance=RequestContext(request)
    )


# suppliers
@login_required
def supplier__view(request, pk=None):
    supplier, suppliers, update_url = None, None, None

    if pk is not None:
        supplier = get_object_or_404(Supplier, pk=pk)
        update_url = reverse('app:supplier__update', args=[str(supplier.pk)])

    else:
        suppliers = Supplier.objects.order_by('name')
        paginator = Paginator(suppliers, PAGE_SIZE)
        page = request.GET.get('page', 1)
        try:
            suppliers = paginator.page(page)
        except PageNotAnInteger:
            suppliers = paginator.page(1)
        except EmptyPage:
            suppliers = paginator.page(paginator.num_pages)

    return render_to_response(
        'app/control_model__view.html',
        {
            'obj': supplier,
            'objs': suppliers,
            'model': 'Supplier',
            'list_url': reverse('app:supplier__view'),
            'update_url': update_url,
        },
        context_instance=RequestContext(request)
    )


@login_required
def supplier__create(request):
    form = SupplierForm()
    formset = SupplierContactFormset(instance=Supplier())

    is_popup = bool(request.GET.get('popup', 0))

    if request.method == 'POST':
        if is_popup or 'popup' in request.REQUEST:
            form = SupplierForm(request.POST)
            if form.is_valid():
                supp = form.save()
                return HttpResponse('<script>opener.closeAddPopup(window, "%s", "%s");</script>' %
                                    (escape(supp.pk), escape(supp.name)))
        else:
            form = SupplierForm(request.POST)
            if form.is_valid():
                supplier = form.save(commit=False)
                formset = SupplierContactFormset(request.POST, instance=supplier)
                if formset.is_valid():
                    supplier.save()
                    formset.save()
                    return redirect(reverse('app:supplier__view'))

    return render_to_response(
        'app/supplier__create.html',
        {
            'form': form,
            'formset': formset,
            'is_popup': is_popup
        },
        context_instance=RequestContext(request)
    )


@login_required
def supplier__update(request, pk=None):
    if pk is None:
        suppliers = Supplier.objects.order_by('name')
        paginator = Paginator(suppliers, PAGE_SIZE)
        page = request.GET.get('page', 1)
        try:
            suppliers = paginator.page(page)
        except PageNotAnInteger:
            suppliers = paginator.page(1)
        except EmptyPage:
            suppliers = paginator.page(paginator.num_pages)

        return render_to_response(
            'app/control_model__update.html',
            {
                'obj': None,
                'objs': suppliers,
                'form': None,
                'model': 'Supplier',
                'cancel': reverse('app:supplier__view'),
                'update_url': reverse('app:supplier__update'),
            },
            context_instance=RequestContext(request)
        )

    else:
        supplier = get_object_or_404(Supplier, pk=pk)

    if request.method == 'GET':
        form = SupplierForm(instance=supplier)

    else:
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect(supplier.get_absolute_url())

    return render_to_response(
        'app/control_model__update.html',
        {
            'obj': supplier,
            'objs': None,
            'form': form,
            'model': 'Supplier',
            'cancel': reverse('app:supplier__view'),
            'update_url': reverse('app:supplier__update', args=[str(supplier.pk)]),
        },
        context_instance=RequestContext(request)
    )


## po endpoints
# contacts
@login_required
def contact__view(request, pk=None):
    contact, contacts, update_url = None, None, None

    if pk is not None:
        contact = get_object_or_404(Contact, pk=pk)
        update_url = reverse('app:contact__update', args=[str(contact.pk)])

    else:
        contacts = Contact.objects.order_by('name')
        paginator = Paginator(contacts, PAGE_SIZE)
        page = request.GET.get('page', 1)
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)

    return render_to_response(
        'app/purchase_order_endpoint__view.html',
        {
            'obj': contact,
            'objs': contacts,
            'model': 'Contact',
            'list_url': reverse('app:contact__view'),
            'update_url': update_url
        },
        context_instance=RequestContext(request)
    )


@login_required
def contact__create(request):
    form = ContactForm()

    is_popup = bool(request.GET.get('popup', 0))

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cont = form.save()
            if 'popup' in request.REQUEST:
                return HttpResponse('<script>opener.closeAddPopup(window, "%s", "%s");</script>' %
                                    (escape(cont.pk), escape(cont.name)))
            return redirect(reverse('app:contact__view'))

    return render_to_response(
        'app/purchase_order_endpoint__create.html',
        {
            'form': form,
            'model': 'Contact',
            'cancel': reverse('app:contact__view'),
            'popup': is_popup,
        },
        context_instance=RequestContext(request)
    )


@login_required
def contact__update(request, pk=None):
    if pk is None:
        contacts = Contact.objects.order_by('name')
        paginator = Paginator(contacts, PAGE_SIZE)
        page = request.GET.get('page', 1)
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)

        return render_to_response(
            'app/purchase_order_endpoint__update.html',
            {
                'obj': None,
                'objs': contacts,
                'form': None,
                'model': 'Contact',
                'cancel': reverse('app:contact__view'),
                'update_url': reverse('app:contact__update'),
            },
            context_instance=RequestContext(request)
        )

    else:
        contact = get_object_or_404(Contact, pk=pk)

    if request.method == 'GET':
        form = ContactForm(instance=contact)

    else:
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect(contact.get_absolute_url())

    return render_to_response(
        'app/purchase_order_endpoint__update.html',
        {
            'obj': contact,
            'objs': None,
            'form': form,
            'model': 'Contact',
            'cancel': reverse('app:contact__view'),
            'update_url': reverse('app:contact__update', args=[str(contact.pk)]),
        },
        context_instance=RequestContext(request)
    )


# receivers
@login_required
def receiver__view(request, pk=None):
    receiver, receivers, update_url = None, None, None

    if pk is not None:
        receiver = get_object_or_404(Receiver, pk=pk)
        update_url = reverse('app:receiver__update', args=[str(receiver.pk)])

    else:
        receivers = Receiver.objects.order_by('name')
        paginator = Paginator(receivers, PAGE_SIZE)
        page = request.GET.get('page', 1)
        try:
            receivers = paginator.page(page)
        except PageNotAnInteger:
            receivers = paginator.page(1)
        except EmptyPage:
            receivers = paginator.page(paginator.num_pages)

    return render_to_response(
        'app/purchase_order_endpoint__view.html',
        {
            'obj': receiver,
            'objs': receivers,
            'model': 'Receiver',
            'list_url': reverse('app:receiver__view'),
            'update_url': update_url
        },
        context_instance=RequestContext(request)
    )


@login_required
def receiver__create(request):
    form = ReceiverForm()

    is_popup = bool(request.GET.get('popup', 0))

    if request.method == 'POST':
        form = ReceiverForm(request.POST)
        if form.is_valid():
            rcv = form.save()
            if 'popup' in request.REQUEST:
                return HttpResponse('<script>opener.closeAddPopup(window, "%s", "%s");</script>' %
                                    (escape(rcv.pk), escape(rcv.name)))
            return redirect(reverse('app:receiver__view'))

    return render_to_response(
        'app/purchase_order_endpoint__create.html',
        {
            'form': form,
            'model': 'Receiver',
            'cancel': reverse('app:receiver__view'),
            'popup': is_popup,
        },
        context_instance=RequestContext(request)
    )


@login_required
def receiver__update(request, pk=None):
    if pk is None:
        receivers = Receiver.objects.order_by('name')
        paginator = Paginator(receivers, PAGE_SIZE)
        page = request.GET.get('page', 1)
        try:
            receivers = paginator.page(page)
        except PageNotAnInteger:
            receivers = paginator.page(1)
        except EmptyPage:
            receivers = paginator.page(paginator.num_pages)

        return render_to_response(
            'app/purchase_order_endpoint__update.html',
            {
                'obj': None,
                'objs': receivers,
                'form': None,
                'model': 'Receiver',
                'cancel': reverse('app:receiver__view'),
                'update_url': reverse('app:receiver__update'),
            },
            context_instance=RequestContext(request)
        )

    else:
        receiver = get_object_or_404(Receiver, pk=pk)

    if request.method == 'GET':
        form = ReceiverForm(instance=receiver)

    else:
        form = ReceiverForm(request.POST, instance=receiver)
        if form.is_valid():
            receiver = form.save()
            return redirect(receiver.get_absolute_url())

    return render_to_response(
        'app/purchase_order_endpoint__update.html',
        {
            'obj': receiver,
            'objs': None,
            'form': form,
            'model': 'Receiver',
            'cancel': reverse('app:receiver__view'),
            'update_url': reverse('app:receiver__update', args=[str(receiver.pk)]),
        },
        context_instance=RequestContext(request)
    )
