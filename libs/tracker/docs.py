#!/usr/bin/env python
# -*- coding: utf-8 -*-

# path hack
from os import environ
from os.path import abspath, dirname, join
import sys

PROJ_DIR = abspath(join(dirname(__file__), '..', '..'))

sys.path.insert(0, PROJ_DIR)

environ.setdefault('DJANGO_SETTINGS_MODULE', 'dodger.settings')


# program imports
from datetime import datetime, timedelta
import re

from django.db.utils import IntegrityError
from django.contrib.auth.models import User
import gspread

from app.models import Supplier, Brand, Category, Sku, QuantityAdjustment, QuantityAdjustmentReason,\
    Attribute, SkuAttribute


# get/create user
USER = User.objects.get_or_create(username='VinceForgione')[0]
USER.is_superuser = True
USER.save()

# get/cerate dat owner (default owner)
OWNER = User.objects.get_or_create(username='DAT')[0]
OWNER.email = 'dat@doggyloot.com'
OWNER.save()

# qty adjustment reason
REASON = QuantityAdjustmentReason.objects.get(name='Tracker Sync')


def get_doc(username, password, doc_name, sheet_name):
    """pulls down the doc as a list of dicts - list is reversed (oldest first)"""
    client = gspread.login(username, password)

    workbook = client.open(doc_name)
    sheet = workbook.worksheet(sheet_name)
    rows = sheet.get_all_values()

    header = rows[0]
    doc = [dict(zip(header, row)) for row in rows[1:]]

    doc.reverse()
    return doc


def process_doc(doc):
    """processes the information"""
    def lookup_control_model(model, name):
        try:
            model = model.objects.find(name=name)
        except model.DoesNotExist:
            model = model()
            model.name = name
            model.save()
        return model

    def save_attribute(name, value, sku):
        if not len(value):
            return
        attr = Attribute.objects.get(name=name)
        sa = SkuAttribute()
        sa.attribute = attr
        sa.sku = sku
        sa.value = value
        try:
            sa.save()
        except IntegrityError:
            pass

    # iterate dicts in doc
    for obj in doc:

        # remove n/a values
        for key, value in obj.iteritems():
            if value.lower().endswith('n/a'):
                obj[key] = ''

        skuid = obj['SKU']
        name = obj['Product']
        supplier = obj['Supplier']
        brand = obj['Manufacturer']
        cats = obj['Type (Toy/ Treat/ Chew/  More)']
        qty = obj['Total SKU Quantity']
        location = obj['Location']

        reason = obj['Reason for Update']

        size = obj['Size']
        style = obj['Style']
        color = obj['Color']
        flavor = obj['Flavor']
        coo = obj['Made In']
        exp_date = obj['Expiration']
        bulk = obj['Bulk?']
        weight = obj['size (ounces for treats)']
        real_weight = obj['']  # zack secret col

        # if not id, skip
        skuid = re.match(r'\d+', skuid)
        if skuid is None:
            continue
        else:
            skuid = skuid.group()

        # get qty
        qty = re.match(r'\d+', qty)
        if qty is None:
            qty = 0
        else:
            qty = qty.group()

        # weights
        weight = re.match(r'\d+?\.\d+', weight)
        if weight is None:
            weight = 0
        else:
            weight = weight.group()
        real_weight = re.match(r'\d+?\.\d+', real_weight)
        if real_weight is not None:
            weight = real_weight.group()

        # control models
        supplier = lookup_control_model(Supplier, supplier)
        brand = lookup_control_model(Brand, brand)
        categories = []
        for cat in cats:
            cat = lookup_control_model(Category, cat)
            categories.append(cat)

        # build sku
        sku = Sku()
        sku.id = skuid
        sku.name = name
        sku.location = location
        sku.supplier = supplier
        sku.brand = brand
        sku.owner = OWNER

        # check if sku exists
        try:
            Sku.objects.find(id=skuid)
            requires_adjustment = True
        except Sku.DoesNotExist:
            requires_adjustment = False

        if not requires_adjustment:
            sku.quantity_on_hand = qty
            sku.save()
        else:
            sku.save()
            adj = QuantityAdjustment()
            adj.sku = sku
            adj.new = qty
            adj.reason = REASON
            adj.who = USER
            adj.deatil = reason
            adj.save()

        # save categories m2m field
        for cat in categories:
            sku.add(cat)
        sku.save()

        # set attributes
        save_attribute('Size', size, sku)
        save_attribute('Style', style, sku)
        save_attribute('Weight', weight, sku)
        save_attribute('Color', color, sku)
        save_attribute('Flavor', flavor, sku)
        save_attribute('Is Bulk', bulk, sku)
        save_attribute('Expiration Date', exp_date, sku)
        save_attribute('Country of Origin', coo, sku)


if __name__ == '__main__':
    from gdocs_config import *
    doc = get_doc(USERNAME, PASSWORD, DOC_NAME, SHEET_NAME)
    process_doc(doc)
