#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

# path hack
import os
import sys
proj = os.path.abspath(os.path.join(__file__, '..', '..', '..'))
sys.path.insert(0, proj)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dodger.settings')

import codecs
import csv
from datetime import date, datetime
import zipfile

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from app.models import Sku


NOTIFICATION_RECIPIENTS = [
    'vince@doggyloot.com',
]


def notify():
    # get skus
    skus = Sku.objects.all()

    # build csv
    header = ['sku', 'brand', 'product', 'attributes', 'qty', 'modified', 'why']
    fname = os.path.join('/', 'tmp', 'skus.csv')
    with codecs.open(fname, 'w', encoding='utf8') as fh:
        writer = csv.writer(fh)
        writer.writerow(header)
        for sku in skus:
            # build attribute string
            attrs = sku.skuattribute_set.all()
            attributes = '; '.join(['(%s) %s' % (attr.attribute.name, attr.value) for attr in attrs])
            # get adjustment - find most recent
            qa = sku.quantityadjustment_set.all()
            ca = sku.costadjustment_set.all()
            adjs = []
            for adj in qa:
                why = adj.detail
                if why in [None, '']:
                    why = adj.reason
                adjs.append([adj.created, why])
            for adj in ca:
                why = adj.detail
                if why in [None, '']:
                    why = adj.reason
                adjs.append([adj.created, why])
            try:
                most_recent = max(adjs, key=lambda x: x[0])
                if ':' in most_recent[1]:
                    imported_date = most_recent[1].split(':')[0].strip()
                    imported_date = datetime.strptime(imported_date, '%m/%d/%Y')
                    most_recent[0] = imported_date
            except ValueError:
                most_recent = (date.today(), 'unknown')
            # write row
            writer.writerow([
                sku.id, sku.brand.name, sku.name, attributes, sku.quantity_on_hand,
                most_recent[0].strftime('%Y-%m-%d'), most_recent[1]
            ])

    # zip file
    zfname = fname + '.zip'
    with zipfile.ZipFile(zfname, 'w') as zfile:
        zfile.write(fname)

    # build email
    sender = 'dodger data'
    subject = 'SKU data for Inventory'
    html = render_to_string('email/inventory_csv.html', {})
    plain = strip_tags(html)

    email = EmailMultiAlternatives(subject, plain, sender, NOTIFICATION_RECIPIENTS)
    email.attach_file(zfname, 'application/csv')
    email.send(fail_silently=False)


if __name__ == '__main__':
    notify()
