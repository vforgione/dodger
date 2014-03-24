#!/usr/bin/env python
# -*- coding: utf-8 -*-

# path hack
import os
import sys
proj = os.path.abspath(os.path.join(__file__, '..', '..', '..'))
sys.path.insert(0, proj)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dodger.settings.dev')

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from constants import NOTIFICATION_RECIPIENTS
from app.models import Sku


def notify():
    # get sku queryset
    skus = Sku.objects.filter(is_subscription=True)

    # build email
    sender = 'dodger notifications'
    subject = 'Subscription SKUs'
    html = render_to_string('email/subscription_skus.html', {'skus': skus})
    plain = strip_tags(html)

    email = EmailMultiAlternatives(subject, plain, sender, NOTIFICATION_RECIPIENTS)
    email.attach_alternative(html, 'text/html')
    email.send(fail_silently=False)


if __name__ == '__main__':
    notify()
