from django.contrib.auth.decorators import login_required
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext

# from app.forms import
from app.models import Sku


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
    pass


def sku__update(request, pk=None):
    pass
