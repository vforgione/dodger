#!/usr/bin/env python
# -*- coding: utf-8 -*-

# path hack
from os import environ
from os.path import abspath, dirname, join
import sys
PROJ_DIR = abspath(join(dirname(__file__), '..', '..'))
sys.path.insert(0, PROJ_DIR)
environ.setdefault('DJANGO_SETTINGS_MODULE', 'dodger.settings.prod')


# program imports
import codecs
import csv
from datetime import date, datetime
import re

from django.db.utils import IntegrityError
from django.contrib.auth.models import User
import gspread

from app.models import Supplier, Brand, Category, Sku, QuantityAdjustment, QuantityAdjustmentReason,\
    Attribute, SkuAttribute


# get/create user
USER = User.objects.get_or_create(username='DAT')[0]
USER.is_superuser = True
USER.save()

# get/cerate dat owner (default owner)
OWNER = USER

# qty adjustment reason
REASON = QuantityAdjustmentReason.objects.get(name='Tracker Sync')


def read_csv(filename):
    with codecs.open(filename, 'r', encoding='utf8') as fh:
        reader = csv.DictReader(fh)
        for row in reader:

            for key, value in row.iteritems():
                row[key] = ''.join([c for c in value if ord(c) < 128])
                if not len(value):
                    row[key] = None

            supplier, _ = Supplier.objects.get_or_create(name=row['supplier'] or '')
            brand, _ = Brand.objects.get_or_create(name=row['brand'] or '')
            category, _ = Category.objects.get_or_create(name=row['category'] or '')

            sku = Sku(
                id=int(row['id']),
                supplier=supplier,
                brand=brand,
                name=row['name'] or '',
                quantity_on_hand=0,
                location=row['location'],
                notes=row['notes'],
                action=row['action'],
                action_date=row['act_date'],
                owner=USER,
                created=datetime.now()
            )
            sku.save(gdocs=True)
            sku.categories.add(category)
            print sku

            try:
                qty = int(float(row['qty']))
            except ValueError:
                qty = 0
            qa = QuantityAdjustment(
                sku=sku,
                new=qty,
                reason=REASON,
                who=USER,
                detail='%s %s' % (row['date'], row['reason'])
            )
            qa.save()
            print qa

            attrs = {'Size': 'size', 'Weight': 'weight', 'Style': 'style', 'Color': 'color', 'Flavor': 'flavor',
                     'Country of Origin': 'coo', 'Expiration Date': 'exp_date'}
            for name, key in attrs.iteritems():
                if row[key] is not None:
                    attr, _ = Attribute.objects.get_or_create(name=name)
                    sa = SkuAttribute(
                        attribute=attr,
                        sku=sku,
                        value=row[key]
                    )
                    sa.save()
                    print sa


if __name__ == '__main__':
    import sys
    filename = sys.argv[1]
    read_csv(filename)


# DEBUG = True
#
#
# def get_doc(username, password, doc_name, sheet_name):
#     """pulls down the doc as a list of dicts - list is reversed (oldest first)"""
#     if DEBUG:
#         print 'making gspread client'
#     client = gspread.login(username, password)
#
#     if DEBUG:
#         print 'getting workbook'
#     workbook = client.open(doc_name)
#     if DEBUG:
#         print 'getting worksheet'
#     sheet = workbook.worksheet(sheet_name)
#     if DEBUG:
#         print 'getting values'
#     rows = sheet.get_all_values()
#
#     if DEBUG:
#         print 'making local doc'
#     header = rows[0]
#     doc = [dict(zip(header, row)) for row in rows[1:]]
#
#     if DEBUG:
#         print 'first date: %s' % doc[0]['Date Received / Updated']
#         print 'last date: %s' % doc[-1]['Date Received / Updated']
#
#     return doc
#
#
# def process_doc(doc):
#     """processes the information"""
#     def lookup_control_model(model, name):
#         try:
#             model = model.objects.get(name=name)
#         except model.DoesNotExist:
#             model = model()
#             model.name = name
#             model.save()
#         return model
#
#     def save_attribute(name, value, sku):
#         if not len(str(value)):
#             return
#         attr = Attribute.objects.get(name=name)
#         sa = SkuAttribute()
#         sa.attribute = attr
#         sa.sku = sku
#         sa.value = value
#         try:
#             sa.save()
#         except IntegrityError:
#             pass
#
#     # iterate dicts in doc
#     for obj in doc[::-1]:  # step backwards through doc
#
#         if DEBUG:
#             print '\n'
#             print 'working on obj %s' % str(obj)
#
#         # remove n/a values
#         for key, value in obj.iteritems():
#             if value.lower().endswith('n/a'):
#                 obj[key] = ''
#
#         # removed non-ascii characters
#         for key, value in obj.iteritems():
#             obj[key] = ''.join([c for c in value if ord(c) < 128])
#
#         skuid = obj['SKU']
#         name = obj['Product']
#         supplier = obj['Supplier']
#         brand = obj['Manufacturer']
#         categories = obj['Type (Toy/ Treat/ Chew/  More)']
#         qty = obj['Total SKU Quantity']
#         location = obj['Location']
#         detail = obj['Reason for Update']
#         date = obj['Date Received / Updated']
#         action = obj['Action']
#         action_date = obj['Month Year']
#
#         size = obj['Size']
#         style = obj['Style']
#         color = obj['Color']
#         flavor = obj['Flavor']
#         coo = obj['Made In']
#         exp_date = obj['Expiration']
#         bulk = obj['Bulk?']
#         weight = obj['size (ounces for treats)']
#
#         # if not id, skip
#         skuid = re.match(r'\d+', skuid)
#         if skuid is None:
#             if DEBUG:
#                 print 'no id found - skipping obj'
#             continue
#         else:
#             skuid = skuid.group()
#
#         # get qty
#         qty = re.match(r'\d+', qty)
#         if qty is None:
#             qty = 0
#         else:
#             qty = qty.group()
#
#         # control models
#         supplier = lookup_control_model(Supplier, supplier)
#         brand = lookup_control_model(Brand, brand)
#         categories = lookup_control_model(Category, categories)
#
#         # build sku
#         sku = Sku()
#         sku.id = skuid
#         sku.name = name
#         sku.location = location
#         sku.supplier = supplier
#         sku.brand = brand
#         sku.owner = OWNER
#         sku.action_date = action_date
#         sku.action = action
#
#         # check if sku exists
#         try:
#             Sku.objects.get(id=skuid)
#             requires_adjustment = True
#         except Sku.DoesNotExist:
#             requires_adjustment = False
#
#         if not requires_adjustment:
#             sku.quantity_on_hand = qty
#             sku.save(gdocs=True)
#         else:
#             if detail in ['', None]:
#                 detail = '%s : unknown' % date
#             else:
#                 detail = ' : '.join([date, detail])
#             sku = Sku.objects.get(id=skuid)
#             adj = QuantityAdjustment()
#             adj.sku = sku
#             adj.new = qty
#             adj.reason = REASON
#             adj.who = USER
#             adj.detail = detail
#             adj.save()
#
#         # save categories m2m field
#         sku.categories.add(categories)
#
#         # set attributes
#         save_attribute('Size', size, sku)
#         save_attribute('Style', style, sku)
#         save_attribute('Weight', weight, sku)
#         save_attribute('Color', color, sku)
#         save_attribute('Flavor', flavor, sku)
#         save_attribute('Is Bulk', bulk, sku)
#         save_attribute('Expiration Date', exp_date, sku)
#         save_attribute('Country of Origin', coo, sku)
#
#
# def update_location(doc):
#
#     for obj in doc[::-1]:  # step backwards through doc
#
#         if DEBUG:
#             print '\n'
#             print 'working on obj %s' % str(obj)
#
#         # remove n/a values
#         for key, value in obj.iteritems():
#             if value.lower().endswith('n/a'):
#                 obj[key] = ''
#
#         # removed non-ascii characters
#         for key, value in obj.iteritems():
#             obj[key] = ''.join([c for c in value if ord(c) < 128])
#
#         location = obj['Location']
#         skuid = obj['SKU']
#
#         if location in ['', None]:
#             continue
#
#         sku = Sku.objects.get(id=skuid)
#         sku.location = location
#         sku.save()
#
#
# if __name__ == '__main__':
#     import json
#     # from gdocs_config import *
#     # doc = get_doc(USERNAME, PASSWORD, DOC_NAME, SHEET_NAME)
#     # with codecs.open('/tmp/tracker.json', 'w', encoding='utf8') as fh:
#     #    json.dump(doc, fh)
#     doc = json.load(codecs.open('/tmp/tracker.json', 'r', encoding='utf8'))
#     process_doc(doc)
#     update_location(doc)
