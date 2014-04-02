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

from app.models import Brand


def count():
    freqs = sorted([
        (brand.name, len(brand.sku_set.all()))
        for brand in Brand.objects.all()
    ], key=lambda s: s[0])

    with codecs.open('/tmp/brand_frequencies.csv', 'w', encoding='utf8') as fh:
        writer = csv.writer(fh)
        writer.writerow(['brand', 'num skus'])
        for brand, freq in freqs:
            writer.writerow([brand, freq])


if __name__ == '__main__':
    count()
