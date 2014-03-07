#!/usr/bin/env python
# -*- coding: utf-8 -*-

# path hack
import os
import sys
proj = os.path.abspath(os.path.join(__file__, '..', '..', '..'))
sys.path.insert(0, proj)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dodger.settings')

from datetime import date, timedelta
import json

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import requests

from constants import URI_DONE_SKUS, NOTIFICATION_RECIPIENTS
from app.models import Sku


TODAY = date.today()
YESTERDAY = TODAY - timedelta(days=1)


def notify():
    # get skus from doggyloot
    res = requests.get(URI_DONE_SKUS)
    sku_ids = json.loads(res.text)

    # get sku queryset
    skus = Sku.objects.filter(id__in=sku_ids)
    unknown = [sku for sku in sku_ids if sku not in [s.id for s in skus]]

    # build email
    sender = 'dodger notifications'
    subject = 'Done Deal SKUs for %s' % TODAY.strftime('%x')
    html = render_to_string('email/done_deal.html', {'skus': skus, 'unknown': unknown, 'yesterday': YESTERDAY})
    plain = strip_tags(html)

    email = EmailMultiAlternatives(subject, plain, sender, NOTIFICATION_RECIPIENTS)
    email.attach_alternative(html, 'text/html')
    email.send(fail_silently=False)


if __name__ == '__main__':
    notify()
