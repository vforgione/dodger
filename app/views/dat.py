from django.contrib.auth.decorators import login_required
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext

from app.forms import PurchaseOrderForm, PurchaseOrderLineItemFormset
from app.models import PurchaseOrder, Contact, Sku


PAGE_SIZE = 20


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
        'app/dat/po__view.html',
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
    formset.forms[0].empty_permitted = False

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
            formset.forms[0].empty_permitted = False
            if formset.is_valid():
                po.save()
                formset.save()
                return redirect(reverse('app:po__view'))

    return render_to_response(
        'app/dat/po__create.html',
        {
            'form': form,
            'formset': formset,
        },
        context_instance=RequestContext(request)
    )
