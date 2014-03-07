from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def shipment_received(po_id, shipment, dat_email):
    sender = 'dodger notifications'
    subject = 'Shipment Received for PO %s' % po_id

    html = render_to_string('email/shipment_received.html', {'shipment': shipment})
    plain = strip_tags(html)

    email = EmailMultiAlternatives(subject, plain, sender, [dat_email, ])
    email.attach_alternative(html, 'text/html')
    email.send(fail_silently=True)
