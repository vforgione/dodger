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

from app.models import Supplier


def count():
    freqs = sorted([
        (supplier.name, len(supplier.sku_set.all()))
        for supplier in Supplier.objects.all()
    ], key=lambda s: s[0])

    with codecs.open('/tmp/supplier_frequencies.csv', 'w', encoding='utf8') as fh:
        writer = csv.writer(fh)
        writer.writerow(['supplier', 'num skus'])
        for supplier, freq in freqs:
            writer.writerow([supplier, freq])


if __name__ == '__main__':
    count()
