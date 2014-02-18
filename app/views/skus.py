from django.contrib.auth.decorators import login_required
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext

from app.forms import SkuForm, SkuAttributeFormset, SupplierForm
from app.models import Sku, Supplier


PAGE_SIZE = 20


# skus
@login_required
def sku__view(request, pk=None):
    sku, skus = None, None

    if pk:
        sku = get_object_or_404(Sku, pk=pk)

    else:
        skus = Sku.objects.order_by('-id')
        paginator = Paginator(skus, PAGE_SIZE)
        page = request.GET.get('page', 1)
        try:
            skus = paginator.page(page)
        except PageNotAnInteger:
            skus = paginator.page(1)
        except EmptyPage:
            skus = paginator.page(paginator.num_pages)

    return render_to_response(
        'app/skus/sku__view.html',
        {
            'sku': sku,
            'skus': skus,
        },
        context_instance=RequestContext(request)
    )


def sku__create(request):
    form = SkuForm()
    formset = SkuAttributeFormset(instance=Sku())

    if request.method == 'GET':
        form.fields['owner'].initial = request.user


    else:
        form = SkuForm(request.POST)
        if form.is_valid():
            sku = form.save(commit=False)
            formset = SkuAttributeFormset(request.POST, instance=sku)
            if formset.is_valid():
                sku.save()
                formset.save()
                return redirect(reverse('app:sku__view'))

    return render_to_response(
        'app/skus/sku__create.html',
        {
            'form': form,
            'formset': formset,
        },
        context_instance=RequestContext(request)
    )


def sku__update(request, pk=None):
    skus, form, formset = None, None, None

    if pk is None:
        skus = Sku.objects.order_by('-id')
        paginator = Paginator(skus, PAGE_SIZE)
        page = request.GET.get('page', 1)
        try:
            skus = paginator.page(page)
        except PageNotAnInteger:
            skus = paginator.page(1)
        except EmptyPage:
            skus = paginator.page(paginator.num_pages)
        return render_to_response(
            'app/skus/sku__update.html',
            {
                'skus': skus,
                'form': form,
                'formset': formset,
            }
        )

    sku = get_object_or_404(Sku, pk=pk)

    if request.method == 'GET':
        form = SkuForm(instance=sku)
        formset = SkuAttributeFormset(instance=sku)
        # TODO: optimize brands based on supplier

    else:
        form = SkuForm(request.POST, instance=sku)
        if form.is_valid():
            updated = form.save(commit=False)
            formset = SkuAttributeFormset(request.POST, instance=sku)
            if formset.is_valid():
                updated.save()
                formset.save()
                return redirect(reverse('app:sku__view'))

    return render_to_response(
        'app/skus/sku__update.html',
        {
            'skus': skus,
            'form': form,
            'formset': formset,
        }
    )


# suppliers
@login_required
def supplier__view(request, pk=None):
    supplier, suppliers = None, None

    if pk:
        supplier = get_object_or_404(Supplier, pk=pk)

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
        'app/skus/supplier__view.html',
        {
            'supplier': supplier,
            'suppliers': suppliers,
        },
        context_instance=RequestContext(request)
    )


@login_required
def supplier__create(request):
    form = SupplierForm()

    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            return redirect(reverse('app:supplier__view'))

    return render_to_response(
        'app/skus/supplier__create.html',
        {
            'form': form,
        },
        context_instance=RequestContext(request)
    )


@login_required
def supplier__update(request, pk=None):
    suppliers, form = None, None

    if pk is None:
        suppliers = Supplier.objects.order_by('-id')
        paginator = Paginator(suppliers, PAGE_SIZE)
        page = request.GET.get('page', 1)
        try:
            suppliers = paginator.page(page)
        except PageNotAnInteger:
            suppliers = paginator.page(1)
        except EmptyPage:
            suppliers = paginator.page(paginator.num_pages)

    if request.method == 'GET':
        if pk:
            form = SupplierForm(instance=get_object_or_404(Supplier, pk=pk))
        else:
            form = SupplierForm()

    else:
        form = SupplierForm(request.POST)
        if form.is_valid():
            return redirect(reverse('app:supplier__view'))

    return render_to_response(
        'app/skus/supplier__update.html',
        {
            'form': form,
            'suppliers': suppliers,
        },
        context_instance=RequestContext(request)
    )
