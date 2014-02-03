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
