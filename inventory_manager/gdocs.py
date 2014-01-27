#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import Counter
from datetime import datetime
import logging
import json
import re

from django.template.defaultfilters import slugify
import gspread
import requests


logger = logging.getLogger('gdocs')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('gdocs.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


def read_doc(username, password, docname, sheetname):
    logger.info('logging into gdocs')
    client = gspread.login(username, password)
    logger.debug('retrieving workbook')
    workbook = client.open(docname)
    spreadsheet = workbook.worksheet(sheetname)
    logger.debug('parsing spreadsheet')
    raw_rows = spreadsheet.get_all_values()
    header = raw_rows[0]
    dict_rows = [dict(zip(header, row)) for row in raw_rows[1:]]
    logger.info('parsed %d rows from sheet' % len(dict_rows))
    return dict_rows


def rip_doc(doc, list_uri, detail_uri, api_key):

    # =========================================================================================================
    # helpers
    def get_supporting_resources(uri, headers):
        logger.debug('getting resources from %s' % uri)
        resources = {}
        resp = requests.get(uri, headers=headers)
        resp = json.loads(resp.text)
        for obj in resp['objects']:
            resources[obj['id']] = obj['resource_uri']
        logger.debug('got %d resources from %s' % (len(resources), uri))
        return resources

    # ---------------------------------------------------------------------------------------------------------
    def generate_skus_and_rows(doc):
        logger.info('getting unique skus')
        skus = set([
            row['SKU'] for row in doc
            if len(row['SKU']) and not row['SKU'].lower().endswith('n/a')
        ])
        logger.debug('got %d unique skus' % len(skus))
        for sku in skus:
            logger.info('working with sku %s' % sku)
            rows = filter(lambda r: r['SKU'] == sku, doc)
            logger.info('found %d rows corresponding to sku %s' % (len(rows), sku))
            yield sku, rows

    # ---------------------------------------------------------------------------------------------------------
    def is_fresher_and_is_new(uri, headers, doc_mod):
        logger.debug('determining if doc info is fresher than db for sku %s' % sku)
        resp = requests.get(uri, headers=headers)
        if resp.status_code == 404:
            return True, True
        resp = json.loads(resp.text)
        db_mod = datetime.strptime(resp['modified'], '%Y-%m-%dT%H:%M:%S.%f')
        if db_mod > doc_mod:
            logger.debug('db is fresher, skipping parse for sku %s' % sku)
            return False, False
        logger.info('doc is fresher for sku %s' % sku)
        return True, False

    # ---------------------------------------------------------------------------------------------------------
    def popularity(rows, col, default):
        freqs = Counter([
            r[col] for r in rows
            if len(r[col])
        ])
        try:
            return sorted(freqs.items(), key=lambda r: r[1], reverse=True)[0][0]
        except IndexError:
            logger.error('couldn\'t get good data for col %s. using default value %s' % (col, default))
            return default

    # ---------------------------------------------------------------------------------------------------------
    def latest(rows, comp_col, out_col, default):
        try:
            value = max(rows, key=lambda r:
                datetime.strptime(r[comp_col], '%m/%d/%Y')
                if re.match(r'\d{1,2}/\d{1,2}/\d{4}', r[comp_col])
                else datetime(1985, 8, 3)
            )[out_col]
            if len(value):
                return value
            return default
        except (ValueError, IndexError, KeyError):
            logger.error('couldn\'t get good data for col %s. using default value %s' % (out_col, default))
            return default

    # ---------------------------------------------------------------------------------------------------------
    def slug_popularity(rows, col, default, lookup, uri, key, headers):
        winner = popularity(rows, col, default)
        if winner is None:
            return winner
        slug = slugify(winner)
        if slug in lookup:
            return lookup[slug]
        logger.debug('creating new resource for %s: %s' % (col, winner))
        resp = requests.post(uri, data=json.dumps({key: winner}), headers=headers)
        resp = json.loads(resp.text)
        lookup[slug] = resp['resource_uri']
        return resp['resource_uri']

    # ---------------------------------------------------------------------------------------------------------
    def split_and_use_all(rows, delimiters, col, lookup, uri, key, headers):
        values = []
        for r in rows:
            values.extend(re.split(delimiters, r[col]))
        values = set([value for value in values if len(value)])
        for value in values:
            slug = slugify(value)
            if slug in lookup:
                yield lookup[slug]
            else:
                logger.debug('creating new resource for %s: %s' % (col, value))
                resp = requests.post(uri, data=json.dumps({key: value}), headers=headers)
                resp = json.loads(resp.text)
                lookup[slug] = resp['resource_uri']
                yield resp['resource_uri']

    # ---------------------------------------------------------------------------------------------------------
    def get_attribute(rows, col, attr, lookup, res_uri, uri, headers):
        try:
            value = sorted(
                Counter([r[col] for r in rows if len(r[col]) and r[col] != '0' and r[col] != '-']),
                key=lambda x: x[1], reverse=True
            )[0]
            payload = {
                'product': res_uri,
                'attribute': lookup[attr],
                'value': value
            }
            logger.info('built payload %s' % payload)
            resp = requests.post(uri, data=json.dumps(payload), headers=headers)
            logger.info('attribute response code %s' % resp.status_code)
            resp = json.loads(resp.text)
            print resp['resource_uri']
        except (ValueError, IndexError):
            logger.debug('no attribute to be had for %s' % col)
            pass
    # ===========================================================================================================


    # make headers
    headers = {'Authorization': 'ApiKey %s' % api_key, 'Content-Type': 'application/json'}

    # get resources
    logger.info('getting support resources')
    categories = get_supporting_resources(list_uri % ('inventory-manager', 'categories') + '?limit=0', headers)
    attributes = get_supporting_resources(list_uri % ('inventory-manager', 'attributes') + '?limit=0', headers)
    manufacturers = get_supporting_resources(list_uri % ('inventory-manager', 'manufacturers') + '?limit=0', headers)
    suppliers = get_supporting_resources(list_uri % ('dat', 'suppliers') + '?limit=0', headers)

    # get skus; iterate
    for sku, rows in generate_skus_and_rows(doc):
        # clear out N/A values
        for row in rows:
            for key, value in row.iteritems():
                if value.lower().endswith('n/a'):
                    row[key] = ''

        # determine freshness and newness
        logger.info('getting doc mod date')
        try:
            doc_mod = max([
                datetime.strptime(r['Date Received / Updated'], '%m/%d/%Y') for r in rows
                if re.match('\d{2}/\d{2}/\d{4}', r['Date Received / Updated'])
            ])
            is_fresher, is_new_product = is_fresher_and_is_new(
                detail_uri % ('inventory-manager', 'products', sku), headers, doc_mod)
        except ValueError:
            logger.error('no dates found. skipping sku')
            is_fresher, is_new_product = False, False
        if not is_fresher:
            continue

        ## build out product information
        # name
        name = popularity(rows, 'Product', '(unknown)')

        # qty
        qty = latest(rows, 'Date Received / Updated', 'Total SKU Quantity', 0)
        try:
            int(float(qty))
        except ValueError:
            qty = 0

        # location
        location = latest(rows, 'Date Received / Updated', 'Location', '(unknown)')

        # mfr
        manufacturer = slug_popularity(
            rows, 'Manufacturer', None, manufacturers, list_uri % ('inventory-manager', 'manufacturers'),
            'name', headers)
        if manufacturer is None:
            manufacturer = '/api/inventory-manager/manufacturers/unknown/'

        # supp
        supplier = slug_popularity(
            rows, 'Supplier', None, suppliers, list_uri % ('dat', 'suppliers'), 'name', headers)
        if supplier is None:
            supplier = '/api/dat/suppliers/unknown/'

        # cat
        cats = [cat for cat in split_and_use_all(
            rows, r'/|-', 'Type (Toy/ Treat/ Chew/  More)', categories, list_uri % ('inventory-manager', 'categories'),
            'name', headers)]
        if not len(cats):
            cats = ['/api/inventory-manager/categories/more/', ]

        # filler
        owner = '/api/auth/users/1/'  # dat account = 10
        reorder = 0
        price = 0
        cost = 0
        mfr_sku = '(unknown)'
        case = 0

        # make product
        product = {
            'sku': sku, 'name': name, 'qty_on_hand': qty, 'location': location, 'manufacturer': manufacturer,
            'supplier': supplier, 'categories': cats, 'owner': owner, 'reorder_threshold': reorder,
            'price': price, 'cost': cost, 'mfr_sku': mfr_sku, 'case_qty': case
        }
        logger.info('build payload: %s' % product)
        if is_new_product:
            resp = requests.post(
                list_uri % ('inventory-manager', 'products'), data=json.dumps(product), headers=headers)
        else:
            del product['sku']
            resp = requests.patch(
                detail_uri % ('inventory-manager', 'products', sku), data=json.dumps(product), headers=headers)
        logger.info('response code %s' % resp.status_code)
        resp = json.loads(resp.text)
        prod = resp['resource_uri']

        print prod

        # get attributes
        logger.info('working with attributes')
        get_attribute(
            rows, 'size (ounces for treats)', 'weight', attributes, prod,
            list_uri % ('inventory-manager', 'product-attributes'), headers)

        get_attribute(
            rows, 'Size', 'style', attributes, prod, list_uri % ('inventory-manager', 'product-attributes'),
            headers)

        get_attribute(
            rows, 'Style', 'size', attributes, prod, list_uri % ('inventory-manager', 'product-attributes'),
            headers)

        get_attribute(
            rows, 'Color', 'color', attributes, prod, list_uri % ('inventory-manager', 'product-attributes'),
            headers)

        get_attribute(
            rows, 'Flavor', 'flavor', attributes, prod, list_uri % ('inventory-manager', 'product-attributes'),
            headers)

        get_attribute(
            rows, 'Bulk?', 'is-bulk', attributes, prod, list_uri % ('inventory-manager', 'product-attributes'),
            headers)

        get_attribute(
            rows, 'Expiration', 'expiration-date', attributes, prod,
            list_uri % ('inventory-manager', 'product-attributes'), headers)

        get_attribute(
            rows, 'Made In', 'country-of-origin', attributes, prod,
            list_uri % ('inventory-manager', 'product-attributes'), headers)
