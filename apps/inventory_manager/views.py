from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext

from forms import *
from models import *


PAGE_SIZE = 20


# products
def product_view(request, pk=None):
    """view a list of products or information about an individual product"""
    product, products = None, None

    if pk:
        product = get_object_or_404(Product, pk=pk)

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


def product_update(request, pk=None):
    products, form, formset = None, None, None

    if pk is None:
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
        form = ProductForm(instance=get_object_or_404(Product, sku=pk))
        formset = ProductAttributeFormset(instance=get_object_or_404(Product, sku=pk))

    else:
        form = ProductForm(request.POST, instance=get_object_or_404(Product, sku=pk))
        if form.is_valid():
            prod = form.save(commit=False)
            formset = ProductAttributeFormset(request.POST, instance=get_object_or_404(Product, sku=pk))
            if formset.is_valid():
                prod.save()
                formset.save()
                return redirect(reverse('inv-mgr:product-view'))
        else:
            formset = ProductAttributeFormset(instance=get_object_or_404(Product, sku=pk))

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
        'inventory_manager/productqtychange-view.html',
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
        'inventory_manager/productqtychange-create.html',
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
        'inventory_manager/productcostchange-view.html',
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
        'inventory_manager/productcostchange-create.html',
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
        'inventory_manager/productpricechange-view.html',
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
        'inventory_manager/productpricechange-create.html',
        {
            'form': form,
        },
        context_instance=RequestContext(request)
    )


# categories
def category_view(request, pk=None):
    cat, cats = None, None

    if pk:
        cat = get_object_or_404(Category, pk=pk)

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
        'inventory_manager/category-view.html',
        {
            'cat': cat,
            'cats': cats,
        },
        context_instance=RequestContext(request)
    )


def category_create(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('inv-mgr:category-view'))

    return render_to_response(
        'inventory_manager/category-create.html',
        {
            'form': form,
        },
        context_instance=RequestContext(request)
    )


# manufacturers
def manufacturer_view(request, pk=None):
    man, mans = None, None

    if pk:
        man = get_object_or_404(Manufacturer, pk=pk)

    else:
        mans = Manufacturer.objects.order_by('name')
        paginator = Paginator(mans, PAGE_SIZE)

        page = request.GET.get('page', 1)
        try:
            mans = paginator.page(page)
        except PageNotAnInteger:
            mans = paginator.page(1)
        except EmptyPage:
            mans = paginator.page(paginator.num_pages)

    return render_to_response(
        'inventory_manager/manufacturer-view.html',
        {
            'man': man,
            'mans': mans,
        },
        context_instance=RequestContext(request)
    )


def manufacturer_create(request):
    form = ManufacturerForm()

    if request.method == 'POST':
        form = ManufacturerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('inv-mgr:manufacturer-view'))

    return render_to_response(
        'inventory_manager/manufacturer-create.html',
        {
            'form': form,
        },
        context_instance=RequestContext(request)
    )


# attributes
def attribute_view(request, pk=None):
    attr, attrs = None, None

    if pk:
        attr = get_object_or_404(Attribute, pk=pk)

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
        'inventory_manager/attribute-view.html',
        {
            'attr': attr,
            'attrs': attrs,
        },
        context_instance=RequestContext(request)
    )


def attribute_create(request):
    form = AttributeForm()

    if request.method == 'POST':
        form = AttributeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('inv-mgr:attribute-view'))

    return render_to_response(
        'inventory_manager/attribute-create.html',
        {
            'form': form,
        },
        context_instance=RequestContext(request)
    )
