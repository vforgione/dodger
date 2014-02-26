#!/usr/bin/env python
# -*- coding: utf-8 -*-

# normally i hate shit like this, but the path hack is necessary
import sys
sys.path.insert(0, '/Users/vince/Development/dodger-env/dodger')

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dodger.settings')

from datetime import datetime, timedelta
import re

from django.db.utils import IntegrityError
from django.contrib.auth.models import User
import gspread

from app.models import Sku, QuantityAdjustmentReason, QuantityAdjustment, \
    Supplier, Brand, Category, Attribute, SkuAttribute


NOW = datetime.now()
DELTA = timedelta(minutes=20)


def get_fresh_doc(username, password, doc_name, sheet_name):
    """pulls down doc as list of dicts"""
    try:
        client = gspread.login(username, password)
        workbook = client.open(doc_name)
        sheet = workbook.worksheet(sheet_name)
        rows = sheet.get_all_values()
        header = rows[0]
        doc = [dict(zip(header, row)) for row in rows[1:]]
        doc = filter(
            lambda r:
                re.match(r'\d{1,2}/\d{1,2}/\d{4} \d{2}:\d{2}:\d{2}', r['modtime'])
                and NOW - datetime.strptime(r['modtime'], '%m/%d/%Y %H:%M:%S') <= DELTA
                and r['SKU'].lower() not in ('n/a', '')
            , doc
        )
    except Exception, e:
        print e
        # sys.exit(1)
    return doc


def get_full_doc(username, password, doc_name, sheet_name):
    """pulls down doc as list of dicts"""
    try:
        client = gspread.login(username, password)
        workbook = client.open(doc_name)
        sheet = workbook.worksheet(sheet_name)
        rows = sheet.get_all_values()
        header = rows[0]
        doc = [dict(zip(header, row)) for row in rows[1:]]
        skus = set([r['SKU'] for r in doc if len(r['SKU']) and not r['SKU'].lower().endswith('n/a')])
        filtered = []
        for sku in skus:
            filtered.append(  # get latest row for the sku
                max(
                    filter(lambda r: r['SKU'] == sku, doc),
                    key=lambda r:
                        datetime.strptime(r['Date Received / Updated'], '%m/%d/%Y')
                        if re.match('\d{1,2}/\d{1,2}/\d{4}', r['Date Received / Updated'])
                        else datetime(1985, 8, 3)
                )
            )
    except Exception, e:
        print e
        sys.exit(1)
    return filtered


def rip_doc(doc):
    """rips the document and updates the db using the orm"""

    def set_attr(sku, obj, attr, key):
        """super redundant - sets value for sku-attribute"""
        if obj[key] in ('0' or ''):
            return
        attr = Attribute.objects.get(name=attr)
        sa = SkuAttribute()
        sa.sku = sku
        sa.attribute = attr
        sa.value = obj[key]
        try:
            sa.save()
        except IntegrityError:
            pass

    def remove_na(obj):
        for key, value in obj.iteritems():
            if value.lower().endswith('n/a'):
                obj[key] = ''
        return obj

    for obj in doc:

        obj = remove_na(obj)

        try:  # if sku already exists
            try:
                id = int(obj['SKU'].split()[0])
            except:
                continue
            sku = Sku.objects.get(id=id)
            if sku.location != obj['Location']:
                sku.location = obj['Location']
                sku.save()

            # check to perform qty change
            try:
                qty = int(obj['Total SKU Quantity'])
            except:
                qty = sku.qty_on_hand
            if sku.qty_on_hand != qty:
                adj = QuantityAdjustment()
                adj.sku = sku
                adj.who = User.objects.get(username='vince@doggyloot.com')
                adj.reason = QuantityAdjustmentReason.objects.get(name='Tracker Sync')
                adj.new = obj['Total SKU Quantity']
                adj.save()

        except Sku.DoesNotExist:  # make a new one
            try:
                id = int(obj['SKU'].split()[0])
            except:
                continue
            sku = Sku()
            sku.id = id
            sku.name = obj['Product']

            # get or create supplier
            try:
                supplier = Supplier.objects.get(name=obj['Supplier'])
            except Supplier.DoesNotExist:
                if obj['Supplier'] == '':
                    supplier = Supplier.objects.get(name='(unknown)')
                else:
                    supplier = Supplier()
                    supplier.name = obj['Supplier']
                    supplier.terms = '?'
                    supplier.save()
            sku.supplier = supplier

            # get or create brand
            try:
                brand = Brand.objects.get(name=obj['Manufacturer'])
            except Brand.DoesNotExist:
                if obj['Manufacturer'] == '':
                    brand = Brand.objects.get(name='(unknown)')
                else:
                    brand = Brand()
                    brand.name = obj['Manufacturer']
                    brand.save()
            sku.brand = brand

            # split and set categories
            cats = re.split(r'/|\- ', obj['Type (Toy/ Treat/ Chew/  More)'])
            cats = [cat for cat in cats if len(cat)]
            if not len(cats):
                cats = ['More', ]
            for cat in cats:
                try:
                    category = Category.objects.get(name=cat)
                except Category.DoesNotExist:
                    category = Category()
                    category.name = cat
                    category.save()
                sku.categories.add(category)

            # set dummy values
            sku.owner = User.objects.get(username='dat@doggyloot.com')
            sku.reorder_threshold = 0
            sku.price = 0.00
            sku.cost = 0.00
            sku.case_qty = 0
            try:
                sku.qty_on_hand = int(float(obj['Total SKU Quantity'].split()[0]))
            except:
                sku.qty_on_hand = 0

        # save with gdocs flag - won't trip qty change sanity check
        sku.save(gdocs=True)

        # set attribute values
        set_attr(sku, obj, 'Weight', 'size (ounces for treats)')
        set_attr(sku, obj, 'Style', 'Style')
        set_attr(sku, obj, 'Size', 'Size')
        set_attr(sku, obj, 'Color', 'Color')
        set_attr(sku, obj, 'Flavor', 'Flavor')
        set_attr(sku, obj, 'Is Bulk', 'Bulk?')
        set_attr(sku, obj, 'Expiration Date', 'Expiration')
        set_attr(sku, obj, 'Country of Origin', 'Made In')
