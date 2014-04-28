#!/usr/bin/env python
# -*- coding: utf-8 -*-

# path hack
import os
import sys
proj = os.path.abspath(os.path.join(__file__, '..', '..', '..'))
sys.path.insert(0, proj)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dodger.settings.prod')

import json

import requests

from constants import URI_LIVE_SKUS
from app.models import Sku


def get_skus_from_sd():
    res = requests.get(URI_LIVE_SKUS)
    res = json.loads(res.text)
    sku_ids = []
    for skuid in res:
        sku_ids.extend(skuid.split(' '))
    sku_ids = set(sku_ids)
    return sku_ids


def turn_off_not_in_list(sku_ids):
    skus = Sku.objects.filter(in_live_deal=True)
    for sku in skus:
        if sku.id not in sku_ids:
            sku.in_live_deal = False
            sku.save()


def turn_on_skus_in_list(sku_ids):
    skus = Sku.objects.filter(id__in=sku_ids)
    for sku in skus:
        sku.in_live_deal = True
        sku.save()


if __name__ == '__main__':
    sku_ids = get_skus_from_sd()
    turn_off_not_in_list(sku_ids)
    turn_on_skus_in_list(sku_ids)
