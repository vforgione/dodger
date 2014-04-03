#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
procedure used to load in inventory results while accounting for quantity adjustments that happened while
the count was under way
"""

# path hack
import os
import sys
proj = os.path.abspath(os.path.join(__file__, '..', '..', '..'))
sys.path.insert(0, proj)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dodger.settings.dev')

import codecs
import csv
from datetime import datetime, timedelta

from django.contrib.auth.models import User
from app.models import QuantityAdjustment, QuantityAdjustmentReason, Sku


QAR, _ = QuantityAdjustmentReason.objects.get_or_create(name='Inventory Load Up')

ROLLBACK, _ = QuantityAdjustmentReason.objects.get_or_create(name='Inventory Rollback')

USER = User.objects.get(email='vince@doggyloot.com')


def load_inventory(cutoff, filename):
    roll_date = cutoff - timedelta(seconds=1)

    ##
    # get qas
    qas = QuantityAdjustment.objects.filter(created__gt=cutoff).order_by('-created')

    ##
    # rollback qas
    for qa in qas:
        sku = Sku.objects.get(id=qa.sku.id)
        rollback = QuantityAdjustment(
            sku=sku,
            new=qa.old,
            who=USER,
            reason=ROLLBACK,
            detail='rollback quantity adjustment <a href="%s">%s</a>' % (qa.get_absolute_url(), str(qa))
        )
        rollback.save()
        rollback.created = roll_date  # overwrite date
        rollback.save()

    ##
    # load up csv
    with codecs.open(filename, 'r', encoding='utf8') as fh:
        reader = csv.reader(fh)
        for skuid, qty, location in reader:
            sku = Sku.objects.get(id=skuid)
            sku.location = location
            sku.save()

            qa = QuantityAdjustment(
                sku=sku,
                new=qty,
                who=USER,
                reason=QAR,
                detail='inventory count'
            )
            qa.save()
            qa.created = cutoff  # overwrite date
            qa.save()

    ##
    # apply qas
    for qa in qas:
        delta = qa.new - qa.old
        sku = Sku.objects.get(id=qa.sku.id)
        if qa.reason.name == 'Spot Count':
            new = qa.new
        else:
            new = sku.quantity_on_hand + delta
        qa.sku = sku
        qa.new = new
        qa.old = sku.quantity_on_hand
        qa.save()

    ##
    # fix location
    for sku in Sku.objects.filter(quantity_on_hand__gt=0, location__in=[None, '']):
        sku.location = sku.last_location
        sku.save()


if __name__ == '__main__':
    cutoff = sys.argv[1]
    filename = sys.argv[2]

    year, month, day = cutoff.split('-')
    cutoff = datetime(int(year), int(month), int(day), 23, 59, 59)

    load_inventory(cutoff, filename)
