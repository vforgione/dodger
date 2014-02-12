from django.contrib.auth.decorators import login_required
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext

from .forms import *
from .models import *


PAGE_SIZE = 20


@login_required
def sku_qty_adj__view(request, pk=None):
    trace, traces = None, None

    if pk:
        trace = get_object_or_404(SkuQuantityAdjustment, pk=pk)

    else:
        traces = SkuQuantityAdjustment.objects.order_by('-when')
        paginator = Paginator(traces, PAGE_SIZE)
        page = request.GET.get('page', 1)
        try:
            traces = paginator.page(page)
        except PageNotAnInteger:
            traces = paginator.page(1)
        except EmptyPage:
            traces = paginator.page(paginator.num_pages)

    return render_to_response(
        'app/sku_qty_adj__view.html',
        {
            'trace': trace,
            'traces': traces,
        },
        context_instance=RequestContext(request)
    )


@login_required
def sku_qty_adj__create(request):
    form = SkuQuantityAdjustmentForm()

    if request.method == 'GET':
        form.fields['who'].initial = request.user

    else:
        form = SkuQuantityAdjustmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('app:sku_qty_adj__view'))

    return render_to_response(
        'app/sku_qty_adj__create.html',
        {
            'form': form,
        },
        context_instance=RequestContext(request)
    )
