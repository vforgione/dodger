#!/usr/bin/env python
# -*- coding: utf-8 -*-

# path hack
import os
import sys
proj = os.path.abspath(os.path.join(__file__, '..', '..', '..'))
sys.path.insert(0, proj)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dodger.settings.prod')

import json

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import requests

from constants import URI_LIVE_DEALS_WITH_SKUS, NOTIFICATION_RECIPIENTS
from app.models import Sku


def notify():
    # get skus from doggyloot
    res = requests.get(URI_LIVE_DEALS_WITH_SKUS)
    res = json.loads(res.text)
    sku_ids = {}
    for obj in res:
        deal = obj['deal']
        for sku in obj['skus']:
            sku_ids[sku] = deal

    # get sku queryset
    skus = Sku.objects.filter(id__in=sku_ids.keys())
    for sku in skus:
        sku.deal = sku_ids[str(sku.id)]
    unknown = set([sku for sku in sku_ids if sku not in [s.id for s in skus]])

    # build email
    sender = 'dodger notifications'
    subject = '[dodger notifications] Live SKUs with 0 Qty'
    html = render_to_string('email/0_qty.html', {'skus': skus, 'unknown': unknown})
    plain = strip_tags(html)

    email = EmailMultiAlternatives(subject, plain, sender, NOTIFICATION_RECIPIENTS)
    email.attach_alternative(html, 'text/html')
    email.send(fail_silently=False)


if __name__ == '__main__':
    notify()
