#!/usr/bin/env python
# -*- coding: utf-8 -*-

# path hack
import os
import sys
proj = os.path.abspath(os.path.join(__file__, '..', '..', '..'))
sys.path.insert(0, proj)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dodger.settings')

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from app.models import Sku


NOTIFICATION_RECIPIENTS = [
    'vince@doggyloot.com',
]


def notify():
    # get skus
    skus = Sku.objects.filter(quantity_on_hand__gt=0, location__in=[None, ''])

    # build email
    sender = 'dodger notification'
    subject = 'SKUs with no Location'
    html = render_to_string(
        'email/qty_no_location.html',
        {'skus': skus}
    )
    plain = strip_tags(html)

    email = EmailMultiAlternatives(subject, plain, sender, NOTIFICATION_RECIPIENTS)
    email.attach_alternative(html, 'text/html')
    email.send(fail_silently=False)


if __name__ == '__main__':
    notify()
