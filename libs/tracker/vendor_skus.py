#!/usr/bin/env python
# -*- coding: utf-8 -*-

# path hack
from os import environ
from os.path import abspath, dirname, join
import sys
PROJ_DIR = abspath(join(dirname(__file__), '..', '..'))
sys.path.insert(0, PROJ_DIR)
environ.setdefault('DJANGO_SETTINGS_MODULE', 'dodger.settings.dev')

import codecs
import csv

from django.contrib.auth.models import User

from app.models import Sku


def import_purchase_orders(filename):
    with codecs.open(filename, 'r', encoding='utf8') as fh:
        reader = csv.DictReader(fh)

        for row in reader:

            for key, value in row.iteritems():
                row[key] = ''.join([c for c in value if ord(c) < 128])
                if not len(value):
                    row[key] = None

            skuid = row['sku']
            supplier = row['supplier']

            sku = Sku.objects.get(id=skuid)
            sku.supplier_sku = supplier
            sku.save()
            print '%s: %s' % (sku.id, sku.supplier_sku)


if __name__ == '__main__':
    import sys
    filename = sys.argv[1]
    import_purchase_orders(filename)
