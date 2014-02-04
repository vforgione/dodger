from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext

from forms import *
from models import *


PAGE_SIZE = 20


# products
def product_view(request, sku=None):
    """view a list of products or information about an individual product"""
    product, products = None, None

    if sku:
        product = get_object_or_404(Product, sku=sku)

    else:
        products = Product.objects.order_by('-sku')
        paginator = Paginator(products, PAGE_SIZE)

        page = request.GET.get('page', 1)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

    return render_to_response(
        'inventory_manager/product-view.html',
        {
            'product': product,
            'products': products,
        },
        context_instance=RequestContext(request)
    )


def product_create(request):
    form = ProductForm()
    formset = ProductAttributeFormset(instance=Product())

    if request.method == 'GET':
        form.fields['owner'].initial = request.user
        form.fields['qty_on_hand'].initial = 0
        form.fields['location'].initial = 'unknown'

    else:
        form = ProductForm(request.POST)
        if form.is_valid():
            prod = form.save(commit=False)
            formset = ProductAttributeFormset(request.POST, instance=prod)
            if formset.is_valid():
                prod.save()
                formset.save()
                return redirect(reverse('inv-mgr:product-view'))

    return render_to_response(
        'inventory_manager/product-create.html',
        {
            'form': form,
            'formset': formset,
        },
        context_instance=RequestContext(request)
    )


def product_update(request, sku=None):
    products, form, formset = None, None, None

    if sku is None:
        products = Product.objects.order_by('-sku')
        paginator = Paginator(products, PAGE_SIZE)

        page = request.GET.get('page', 1)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        return render_to_response(
            'inventory_manager/product-update.html',
            {
                'products': products,
                'form': form,
                'formset': formset,
            },
            context_instance=RequestContext(request)
        )

    if request.method == 'GET':
        form = ProductForm(instance=get_object_or_404(Product, sku=sku))
        formset = ProductAttributeFormset(instance=get_object_or_404(Product, sku=sku))

    else:
        form = ProductForm(request.POST, instance=get_object_or_404(Product, sku=sku))
        if form.is_valid():
            prod = form.save(commit=False)
            formset = ProductAttributeFormset(request.POST, instance=get_object_or_404(Product, sku=sku))
            if formset.is_valid():
                prod.save()
                formset.save()
                return redirect(reverse('inv-mgr:product-view'))
        else:
            formset = ProductAttributeFormset(instance=get_object_or_404(Product, sku=sku))

    return render_to_response(
        'inventory_manager/product-update.html',
        {
            'products': products,
            'form': form,
            'formset': formset,
        },
        context_instance=RequestContext(request)
    )


# product qty change
def productqtychange_view(request, pk=None):
    pqc, pqcs = None, None

    if pk:
        pqc = get_object_or_404(ProductQtyChange, pk=pk)

    else:
        pqcs = ProductQtyChange.objects.order_by('-modified')
        paginator = Paginator(pqcs, PAGE_SIZE)

        page = request.GET.get('page', 1)
        try:
            pqcs = paginator.page(page)
        except PageNotAnInteger:
            pqcs = paginator.page(1)
        except EmptyPage:
            pqcs = paginator.page(paginator.num_pages)

    return render_to_response(
        'inventory_manager/pqc-view.html',
        {
            'pqc': pqc,
            'pqcs': pqcs,
        }
    )


def productqtychange_create(request):
    form = ProductQtyChangeForm()

    if request.method == 'GET':
        form.fields['who'].initial = request.user

    else:
        form = ProductQtyChangeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('inv-mgr:pqc-view'))

    return render_to_response(
        'inventory_manager/pqc-create.html',
        {
            'form': form,
        },
        context_instance=RequestContext(request)
    )


# product cost change
def productcostchange_view(request, pk=None):
    pcc, pccs = None, None

    if pk:
        pcc = get_object_or_404(ProductCostChange, pk=pk)

    else:
        pccs = ProductCostChange.objects.order_by('-modified')
        paginator = Paginator(pccs, PAGE_SIZE)

        page = request.GET.get('page', 1)
        try:
            pccs = paginator.page(page)
        except PageNotAnInteger:
            pccs = paginator.page(1)
        except EmptyPage:
            pccs = paginator.page(paginator.num_pages)

    return render_to_response(
        'inventory_manager/pcc-view.html',
        {
            'pcc': pcc,
            'pccs': pccs,
        }
    )


def productcostchange_create(request):
    form = ProductCostChangeForm()

    if request.method == 'GET':
        form.fields['who'].initial = request.user

    else:
        form = ProductCostChangeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('inv-mgr:pcc-view'))

    return render_to_response(
        'inventory_manager/pcc-create.html',
        {
            'form': form,
        },
        context_instance=RequestContext(request)
    )


# product price change
def productpricechange_view(request, pk=None):
    ppc, ppcs = None, None

    if pk:
        ppc = get_object_or_404(ProductPriceChange, pk=pk)

    else:
        ppcs = ProductPriceChange.objects.order_by('-modified')
        paginator = Paginator(ppcs, PAGE_SIZE)

        page = request.GET.get('page', 1)
        try:
            ppcs = paginator.page(page)
        except PageNotAnInteger:
            ppcs = paginator.page(1)
        except EmptyPage:
            ppcs = paginator.page(paginator.num_pages)

    return render_to_response(
        'inventory_manager/ppc-view.html',
        {
            'ppc': ppc,
            'ppcs': ppcs,
        }
    )


def productpricechange_create(request):
    form = ProductPriceChangeForm()

    if request.method == 'GET':
        form.fields['who'].initial = request.user

    else:
        form = ProductPriceChangeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('inv-mgr:ppc-view'))

    return render_to_response(
        'inventory_manager/ppc-create.html',
        {
            'form': form,
        },
        context_instance=RequestContext(request)
    )
