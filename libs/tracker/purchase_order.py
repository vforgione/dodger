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

from app.models import Supplier, Contact, PurchaseOrder, PurchaseOrderLineItem, Sku, Receiver


def import_purchase_orders(filename):
    with codecs.open(filename, 'r', encoding='utf8') as fh:
        reader = csv.DictReader(fh)

        pos = {}
        receiver = Receiver.objects.get(name='Ogden Warehouse')

        for row in reader:

            for key, value in row.iteritems():
                row[key] = ''.join([c for c in value if ord(c) < 128])
                if not len(value):
                    row[key] = None

            po = row['po_delimiter']
            if po is None:
                continue
            pos.setdefault(po, {})

            qty = int(float(row['qty']))
            skuid = row['sku']
            unit_cost = float(row['unit'])
            supplier = row['supplier']
            contact = row['contact']
            email = row['creator'].lower()
            terms = row['terms']

            supplier = Supplier.objects.get(name=supplier)
            contact = Contact.objects.get(name=contact)

            try:
                sku = Sku.objects.get(id=skuid)
            except Sku.DoesNotExist:
                print skuid
                raise

            try:
                creator = User.objects.get(email=email)
            except User.DoesNotExist:
                if email == 'nick@doggyloot.com':
                    creator = User.objects.create_user('NickRosa', email, first_name='Nick', last_name='Rosa')
                elif email == 'jim@doggyloot.com':
                    creator = User.objects.create_user('JimSiegel', email, first_name='Jim', last_name='Siegel')
                else:
                    creator = User.objects.create_user('NickPhillips', email, first_name='Nick', last_name='Phillips')

            pos[po]['creator'] = creator
            pos[po]['supplier'] = supplier
            pos[po]['contact'] = contact
            pos[po]['receiver'] = receiver
            pos[po]['terms'] = terms
            pos[po].setdefault('line_items', [])
            pos[po]['line_items'].append({'qty': qty, 'sku': sku, 'cost': unit_cost})

        for group, po_data in pos.iteritems():
            po = PurchaseOrder()
            po.creator = po_data['creator']
            po.supplier = po_data['supplier']
            po.contact = po_data['contact']
            po.receiver = po_data['receiver']
            po.terms = po_data['terms']
            po.save()
            print po

            for lih in po_data['line_items']:
                li = PurchaseOrderLineItem()
                li.sku = lih['sku']
                li.quantity_ordered = lih['qty']
                li.unit_cost = lih['cost']
                li.purchase_order = po
                li.save()
                print li


if __name__ == '__main__':
    import sys
    filename = sys.argv[1]
    import_purchase_orders(filename)
