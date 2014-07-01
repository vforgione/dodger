from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from models import PurchaseOrderLineItem, ShipmentLineItem, Sku


def shipment_received(po_id, shipment, dat_email):
    sender = 'dodger notifications'
    subject = '[dodger notifications] Shipment Received for PO %s' % po_id

    po_li = dict((li.sku.id, li.quantity_ordered)
                 for li in PurchaseOrderLineItem.objects.filter(purchase_order__id=po_id))
    sh_li = {}
    lis = ShipmentLineItem.objects.filter(shipment__purchase_order__id=po_id)
    for li in lis:
        sh_li.setdefault(li.sku.id, 0)
        sh_li[li.sku.id] += li.quantity_received

    line_items = []
    missing = []
    extra = []
    for sku, qo in po_li.iteritems():
        if sku in sh_li:
            s = Sku.objects.get(id=sku)
            name = '(%s) %s' % (s.supplier.name, s.description)
            if qo == sh_li[sku]:
                line_items.append((name, qo, sh_li[sku], '#000'))
            else:
                line_items.append((name, qo, sh_li[sku], '#f00'))
            del sh_li[sku]
        else:
            missing.append((sku, qo))
    for sku, qr in sh_li.iteritems():
        extra.append((sku, qr))

    html = render_to_string('email/shipment_received.html',
        {'shipment': shipment, 'line_items': line_items, 'missing': missing, 'extra': extra})
    plain = strip_tags(html)

    email = EmailMultiAlternatives(subject, plain, sender, [dat_email, 'epark@sandboxindustries.com',
                                                            'jim@doggyloot.com', 'mike@doggyloot.com',
                                                            shipment.creator.email])
    email.attach_alternative(html, 'text/html')
    email.send(fail_silently=True)
