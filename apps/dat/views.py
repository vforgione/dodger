from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext

from forms import *
from models import *

from apps.inventory_manager.models import Product


PAGE_SIZE = 20


# purchase orders
def purchaseorder_view(request, pk=None):
    """view purchase order or paginated list of purchase orders"""
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
        'dat/purchaseorder-view.html',
        {
            'po': po,
            'pos': pos,
        },
        context_instance=RequestContext(request)
    )


def purchaseorder_create(request):
    form = PurchaseOrderForm()
    formset = PurchaseOrderProductFormset(instance=PurchaseOrder())

    if request.method == 'GET':
        form.fields['creator'].initial = request.user
        form.fields['contact'].queryset = Contact.objects.filter(name='')
        for _form in formset:
            _form.fields['product'].queryset = Product.objects.filter(name='')

    else:
        form = PurchaseOrderForm(request.POST)
        if form.is_valid():
            po = form.save(commit=False)
            formset = PurchaseOrderProductFormset(request.POST, instance=po)
            if formset.is_valid():
                po.save()
                formset.save()
                return redirect(reverse('dat:purchaseorder-view'))

    return render_to_response(
        'dat/purchaseorder-create.html',
        {
            'form': form,
            'formset': formset,
        },
        context_instance=RequestContext(request)
    )


# suppliers
def supplier_view(request, pk=None):
    if pk:
        supplier = get_object_or_404(Supplier, pk=pk)
        suppliers = [supplier, ]
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

    display_pages = len(suppliers) > 1
    return render_to_response(
        'dat/supplier-view.html',
        {
            'suppliers': suppliers,
            'display_pages': display_pages,
        },
        context_instance=RequestContext(request)
    )


def supplier_create(request):
    if request.method == 'GET':
        form = SupplierForm()

    else:
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('dat:supplier-view'))

    return render_to_response(
        'dat/supplier-create.html',
        {
            'form': form,
        },
        context_instance=RequestContext(request)
    )


def supplier_update(request, pk):
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

        display_pages = len(suppliers) > 1
        return render_to_response(
            'dat/supplier-update.html',
            {
                'suppliers': suppliers,
                'display_pages': display_pages,
            },
            context_instance=RequestContext(request)
        )

    if request.method == 'GET':
        form = SupplierForm(instance=get_object_or_404(Supplier, pk=pk))

    else:
        form = SupplierForm(request.POST, instance=get_object_or_404(Supplier, pk=pk))
        if form.is_valid():
            form.save()
            return redirect(reverse('dat:supplier-view'))

    return render_to_response(
        'dat/supplier-update.html',
        {
            'form': form,
        },
        context_instance=RequestContext(request)
    )


# contacts
def contact_view(request, pk=None):
    if pk:
        contact = get_object_or_404(Contact, pk=pk)
        contacts = [contact, ]
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

    display_pages = len(contacts) > 1
    return render_to_response(
        'dat/contact-view.html',
        {
            'contacts': contacts,
            'display_pages': display_pages,
        },
        context_instance=RequestContext(request)
    )


def contact_create(request):
    if request.method == 'GET':
        form = ContactForm()

    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('dat:contact-view'))

    return render_to_response(
        'dat/contact-create.html',
        {
            'form': form,
        },
        context_instance=RequestContext(request)
    )


def contact_update(request, pk):
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

        display_pages = len(contacts) > 1
        return render_to_response(
            'dat/contact-update.html',
            {
                'contacts': contacts,
                'display_pages': display_pages,
            },
            context_instance=RequestContext(request)
        )

    if request.method == 'GET':
        form = ContactForm(instance=get_object_or_404(Contact, pk=pk))

    else:
        form = ContactForm(request.POST, instance=get_object_or_404(Contact, pk=pk))
        if form.is_valid():
            form.save()
            return redirect(reverse('dat:contact-view'))

    return render_to_response(
        'dat/contact-update.html',
        {
            'form': form,
        },
        context_instance=RequestContext(request)
    )


# contact labels
def contactlabel_view(request, pk=None):
    if pk:
        cl = get_object_or_404(ContactLabel, pk=pk)
        cls = [cl, ]
    else:
        cls = ContactLabel.objects.order_by('name')
        paginator = Paginator(cls, PAGE_SIZE)

        page = request.GET.get('page', 1)
        try:
            cls = paginator.page(page)
        except PageNotAnInteger:
            cls = paginator.page(1)
        except EmptyPage:
            cls = paginator.page(paginator.num_pages)

    display_pages = len(cls) > 1
    return render_to_response(
        'dat/contactlabel-view.html',
        {
            'cls': cls,
            'display_pages': display_pages,
        },
        context_instance=RequestContext(request)
    )


def contactlabel_create(request):
    if request.method == 'GET':
        form = ContactLabelForm()

    else:
        form = ContactLabelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('dat:contactlabel-view'))

    return render_to_response(
        'dat/contactlabel-create.html',
        {
            'form': form,
        },
        context_instance=RequestContext(request)
    )


# receivers
def receiver_view(request, pk=None):
    if pk:
        receiver = get_object_or_404(Receiver, pk=pk)
        receivers = [receiver, ]
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

    display_pages = len(receivers) > 1
    return render_to_response(
        'dat/receiver-view.html',
        {
            'receivers': receivers,
            'display_pages': display_pages,
        },
        context_instance=RequestContext(request)
    )


def receiver_create(request):
    if request.method == 'GET':
        form = ReceiverForm()

    else:
        form = ReceiverForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('dat:receiver-view'))

    return render_to_response(
        'dat/receiver-create.html',
        {
            'form': form,
        },
        context_instance=RequestContext(request)
    )


def receiver_update(request, pk):
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

        display_pages = len(receivers) > 1
        return render_to_response(
            'dat/receiver-update.html',
            {
                'receivers': receivers,
                'display_pages': display_pages,
            },
            context_instance=RequestContext(request)
        )

    if request.method == 'GET':
        form = ReceiverForm(instance=get_object_or_404(Receiver, pk=pk))

    else:
        form = ReceiverForm(request.POST, instance=get_object_or_404(Receiver, pk=pk))
        if form.is_valid():
            form.save()
            return redirect(reverse('dat:receiver-view'))

    return render_to_response(
        'dat/receiver-update.html',
        {
            'form': form,
        },
        context_instance=RequestContext(request)
    )
