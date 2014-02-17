import csv

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from app.models import PurchaseOrderLineItem


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
    writer.writerow(['po id', 'sku id', 'qty ordered', 'unit cost', 'line total'])
    for item in items:
        writer.writerow([
            item.purchase_order.id, item.sku.id, item.qty_ordered, item.sku.cost, item.qty_ordered * item.sku.cost
        ])

    return response
