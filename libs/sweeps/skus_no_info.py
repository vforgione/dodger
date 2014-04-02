#!/usr/bin/env python
# -*- coding: utf-8 -*-

# path hack
import os
import sys
proj = os.path.abspath(os.path.join(__file__, '..', '..', '..'))
sys.path.insert(0, proj)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dodger.settings.dev')

import codecs
import csv

from app.models import Sku


def brand():
    skus = sorted([
        (sku.id, sku.name, ', '.join(['(%s) %s' % (a.attribute.name, a.value) for a in sku.skuattribute_set.all()]))
        for sku in Sku.objects.filter(brand__name='')
    ], key=lambda s: s[0])

    with codecs.open('/tmp/skus_no_brand.csv', 'w', encoding='utf8') as fh:
        writer = csv.writer(fh)
        writer.writerow(['id', 'name', 'description', 'brand'])
        for id, name, desc in skus:
            writer.writerow([id, name, desc, ''])


def supplier():
    skus = sorted([
        (sku.id, sku.name, ', '.join(['(%s) %s' % (a.attribute.name, a.value) for a in sku.skuattribute_set.all()]))
        for sku in Sku.objects.filter(supplier__name='')
    ], key=lambda s: s[0])

    with codecs.open('/tmp/skus_no_supplier.csv', 'w', encoding='utf8') as fh:
        writer = csv.writer(fh)
        writer.writerow(['id', 'name', 'description', 'supplier'])
        for id, name, desc in skus:
            writer.writerow([id, name, desc, ''])


def name():
    skus = sorted([
        (sku.id, ', '.join(['(%s) %s' % (a.attribute.name, a.value) for a in sku.skuattribute_set.all()]))
        for sku in Sku.objects.filter(name='')
    ], key=lambda s: s[0])

    with codecs.open('/tmp/skus_no_name.csv', 'w', encoding='utf8') as fh:
        writer = csv.writer(fh)
        writer.writerow(['id', 'description', 'name'])
        for id, desc in skus:
            writer.writerow([id, desc, ''])


if __name__ == '__main__':
    brand()
    supplier()
    name()
