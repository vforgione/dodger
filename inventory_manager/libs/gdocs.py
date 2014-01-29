#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dodger.settings')

import sys
sys.path.append('/home/deploy/dodger-env/dodger')  # normally i hate this, but it's necessary

from inventory_manager.models import Product, Category, Manufacturer, Attribute, ProductAttribute, \
    Reason, ProductQtyChange
from dat.models import Supplier
from django.contrib.auth.models import User


from collections import Counter
from datetime import datetime
import logging
import re

from django.template.defaultfilters import slugify
import gspread
import pytz


logger = logging.getLogger('gdocs')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gdocs.log'))
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


def read_doc(username, password, docname, sheetname):
    """pulls down gspread as list of dicts"""
    logger.info('logging into gdocs')
    try:
        client = gspread.login(username, password)
    except Exception, e:
        logger.critical(e)
        sys.exit(1)

    logger.info('retrieving document')
    try:
        workbook = client.open(docname)
    except Exception, e:
        logger.critical(e)
        sys.exit(1)

    logger.info('getting spreadsheet')
    try:
        sheet = workbook.worksheet(sheetname)
    except Exception, e:
        logger.critical(e)
        sys.exit(1)

    logger.info('parsing spreadsheet')
    try:
        raw_rows = sheet.get_all_values()
        header = raw_rows[0]
        dict_rows = [dict(zip(header, row)) for row in raw_rows[1:]]
    except Exception, e:
        logger.critical(e)
        sys.exit(1)

    logger.info('parsed %d rows from sheet' % len(dict_rows))
    return dict_rows


def rip_doc(doc):
    """rips the document and updates the db"""

    def get_supporting_resource(model):
        """gets objs from db"""
        logger.info('getting data for %s' % model.__name__)
        try:
            objs = model.objects.all()
            resources = dict((obj.id, obj) for obj in objs)
            logger.debug('%d resources pulled in %s' % (len(resources), model.__name__))
            return resources
        except Exception, e:
            logger.critical(e)
            sys.exit(1)


    def generate_skus_and_rows(doc):
        """gets unique skus and pairs corresponding rows"""
        logger.info('generating skus and rows')
        try:
            skus = set([
                row['SKU'] for row in doc
                if len(row['SKU']) and not row['SKU'].lower().endswith('n/a')
            ])
        except Exception, e:
            logger.critical(e)
            sys.exit(1)
        logger.debug('%d unique skus found' % len(skus))
        for sku in skus:
            rows = filter(lambda r: r['SKU'] == sku, doc)
            logger.info('sku %s, %d rows corresponding' % (sku, len(rows)))
            yield sku, rows

    def nix_na_values(rows):
        """replaces 'N/A' values in rows with '' """
        for row in rows:
            for key, value in row.iteritems():
                if value.lower().endswith('n/a'):
                    row[key] = ''
        return rows

    def is_new_product(sku):
        """determines if the product from the doc is new"""
        try:
            Product.objects.get(sku=sku)
            return False
        except Product.DoesNotExist:
            return True
        except Exception, e:
            logger.critical('is_new_product: %s' % e)
            sys.exit(1)

    def doc_last_mod(rows):
        """gets the latest mod time for rows"""
        try:
            doc_mod = max([
                datetime.strptime(r['Date Received / Updated'], '%m/%d/%Y') for r in rows
                if re.match('\d{2}/\d{2}/\d{4}', r['Date Received / Updated'])
            ])
            doc_mod = doc_mod.replace(tzinfo=pytz.timezone('US/Central'))
            return doc_mod
        except ValueError:
            return None
        except Exception, e:
            logger.critical('doc_latest_mod: %s' % e)
            sys.exit(1)

    def is_doc_fresher(sku, doc_mod):
        """determines if the doc is fresher"""
        if doc_mod is None:
            return False
        try:
            prod = Product.objects.get(sku=sku)
            return doc_mod > prod.modified
        except Product.DoesNotExist:
            return True
        except Exception, e:
            logger.critical('is_doc_fresher: %s' % e)
            sys.exit(1)

    def popularity(rows, col, default):
        """gets the most popular value"""
        try:
            freqs = Counter([
                r[col] for r in rows
                if len(r[col])
            ])
            return sorted(freqs.items(), key=lambda r: r[1], reverse=True)[0][0]
        except (ValueError, IndexError):
            return default
        except Exception, e:
            logger.critical('popularity critical error: %s' % e)
            sys.exit(1)

    def latest(rows, col, default):
        """gets the value of col based on the latest mod time"""
        try:
            value = max(
                rows,
                key=lambda r:
                    datetime.strptime(r['Date Received / Updated'], '%m/%d/%Y')
                    if re.match('\d{2}/\d{2}/\d{4}', r['Date Received / Updated'])
                    else datetime(1985, 8, 3)
            )[col]
            if len(value):
                return value
            return default
        except (ValueError, IndexError):
            return default
        except Exception, e:
            logger.critical('latest: %s' % e)
            sys.exit(1)

    def slug_popularity(rows, col, default, lookup, model):
        """uses or creates object for model"""
        winner = popularity(rows, col, default)
        if winner is None:
            return winner
        slug = slugify(winner)
        if slug in lookup:
            return lookup[slug]
        logger.info('creating new object for %s: %s' % (model.__name__, winner))
        try:
            obj = model()
            obj.name = winner
            obj = obj.save()
            lookup[obj.id] = obj.name
            return obj
        except Exception, e:
            logger.critical(e)
            sys.exit(1)

    def split_and_use_all(rows, delimiters, col, lookup, model):
        """splits the values of col for all rows and yields values"""
        values = []
        for r in rows:
            values.extend(re.split(delimiters, r[col]))
        values = set([val for val in values if len(val)])
        for value in values:
            slug = slugify(value)
            if slug in lookup:
                yield lookup[slug]
            else:
                logger.info('creating new object for %s: %s' % (model.__name__, value))
                try:
                    obj = model()
                    obj.name = value
                    obj = obj.save()
                    lookup[obj.id] = obj.name
                    yield obj
                except Exception, e:
                    logger.critical(e)
                    sys.exit(1)

    def get_attribute(sku, attr, rows, col):
        """if new prod-attr creates new object"""
        try:
            ProductAttribute.objects.get(product__sku=sku, attribute__id=attr)
            return
        except ProductAttribute.DoesNotExist:
            pass
        try:
            value = sorted(
                Counter([r[col] for r in rows if len(r[col]) and r[col] != '0' and r[col] != '-']),
                key=lambda x: x[1], reverse=True
            )[0]
        except (ValueError, IndexError):
            return
        except Exception, e:
            logger.critical('getting value for new prod-attr: %s' % e)
            sys.exit(1)
        try:
            pa = ProductAttribute()
            pa.product = Product.objects.get(sku=sku)
            pa.attribute = Attribute.objects.get(id=attr)
            pa.value = value
            pa.save()
            logger.info('created new ProductAttribute %s@%s=%s' % (sku, attr, value))
        except Exception, e:
            logger.critical('creating new prod-attr: %s' % e)
            sys.exit(1)

    # -------------------------------------------------------------------------------------------
    # get supporting resources
    logger.info('getting support resources')
    attributes = get_supporting_resource(Attribute)
    categories = get_supporting_resource(Category)
    manufacturers = get_supporting_resource(Manufacturer)
    suppliers = get_supporting_resource(Supplier)

    # get skus, rows and iterate
    for sku, rows in generate_skus_and_rows(doc):
        rows = nix_na_values(rows)

        # get mod time
        doc_mod = doc_last_mod(rows)
        if not is_doc_fresher(sku, doc_mod):
            logger.info('doc is stale for %s. skipping' % sku)
            continue

        # is new product - could trigger product qty change
        pqc = False
        if not is_new_product(sku):
            prod = Product.objects.get(sku=sku)

            # compare qty - need to make change obj if different
            default = 'barf'
            qty = latest(rows, 'Total SKU Quantity', default)
            if qty == default:
                qty = 0
            else:
                try:
                    ProductQtyChange(
                        product=prod,
                        old_qty=prod.qty_on_hand,
                        new_qty=qty,
                        reason=Reason.objects.get(name='gdocs sync'),
                        who=User.objects.get(username='dat@doggyloot.com')
                    ).save()
                    pqc = True
                except Exception, e:
                    logger.critical('create PQC failed: %s' % e)
                    sys.exit(1)
        else:
            qty = latest(rows, 'Total SKU Quantity', 0)

        # name
        name = popularity(rows, 'Product', '(unknown)')

        # location
        location = latest(rows, 'Location', '(unknown)')

        # mfr
        manufacturer = slug_popularity(rows, 'Manufacturer', None, manufacturers, Manufacturer)
        if manufacturer is None:
            manufacturer = manufacturers['unknown']

        # supp
        supplier = slug_popularity(rows, 'Supplier', None, suppliers, Supplier)
        if supplier is None:
            supplier = suppliers['unknown']

        # cat
        cats = [cat for cat in
                split_and_use_all(rows, r'/|-', 'Type (Toy/ Treat/ Chew/  More)', categories, Category)]
        if not len(cats):
            cats = [categories['more'], ]

        # filler
        owner = User.objects.get(username='dat@doggyloot.com')
        reorder = 0
        price = 0
        cost = 0
        mfr_sku = '(unknown)'
        case = 0

        product = {
            'sku': sku, 'name': name, 'location': location, 'manufacturer': manufacturer,
            'supplier': supplier, 'owner': owner, 'reorder_threshold': reorder,
            'price': price, 'cost': cost, 'mfr_sku': mfr_sku, 'case_qty': case
        }
        if not pqc:
            product['qty_on_hand'] = qty
            try:
                prod = Product.objects.create(**product)
                for cat in cats:
                    prod.categories.add(cat)
                prod = prod.save()
                logger.info('product save: %s' % prod)
            except Exception, e:
                logger.critical('product save: %s' % e)
                sys.exit(1)
        else:
            try:
                prod = Product.objects.filter(sku=sku).update(**product)
                for cat in cats:
                    prod.categories.add(cat)
                prod = prod.save()
                logger.info('product save: %s' % prod)
            except Exception, e:
                logger.critical('product save: %s' % e)
                sys.exit(1)

        # attributes
        get_attribute(sku, 'weight', rows, 'size (ounces for treats)')
        get_attribute(sku, 'style', rows, 'Style')
        get_attribute(sku, 'size', rows, 'Size')
        get_attribute(sku, 'color', rows, 'Color')
        get_attribute(sku, 'flavor', rows, 'Flavor')
        get_attribute(sku, 'is-bulk', rows, 'Bulk?')
        get_attribute(sku, 'expiration-date', rows, 'Expiration')
        get_attribute(sku, 'country-of-origin', rows, 'Made In')



# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
#
# from collections import Counter
# from datetime import datetime
# import logging
# import json
# import os
# import re
#
# from django.template.defaultfilters import slugify
# import gspread
# import requests
#
#
# logger = logging.getLogger('gdocs')
# logger.setLevel(logging.DEBUG)
# fh = logging.FileHandler(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gdocs.log'))
# fh.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s')
# fh.setFormatter(formatter)
# logger.addHandler(fh)
#
#
# def read_doc(username, password, docname, sheetname):
#     logger.info('logging into gdocs')
#     client = gspread.login(username, password)
#     logger.debug('retrieving workbook')
#     workbook = client.open(docname)
#     spreadsheet = workbook.worksheet(sheetname)
#     logger.debug('parsing spreadsheet')
#     raw_rows = spreadsheet.get_all_values()
#     header = raw_rows[0]
#     dict_rows = [dict(zip(header, row)) for row in raw_rows[1:]]
#     logger.info('parsed %d rows from sheet' % len(dict_rows))
#     return dict_rows
#
#
# def rip_doc(doc, list_uri, detail_uri, api_key):
#
#     # =========================================================================================================
#     # helpers
#     def get_supporting_resources(uri, headers):
#         logger.debug('getting resources from %s' % uri)
#         resources = {}
#         resp = requests.get(uri, headers=headers, verify=False)
#         resp = json.loads(resp.text)
#         for obj in resp['objects']:
#             resources[obj['id']] = obj['resource_uri']
#         logger.debug('got %d resources from %s' % (len(resources), uri))
#         return resources
#
#     # ---------------------------------------------------------------------------------------------------------
#     def generate_skus_and_rows(doc):
#         logger.info('getting unique skus')
#         skus = set([
#             row['SKU'] for row in doc
#             if len(row['SKU']) and not row['SKU'].lower().endswith('n/a')
#         ])
#         logger.debug('got %d unique skus' % len(skus))
#         for sku in skus:
#             logger.info('working with sku %s' % sku)
#             rows = filter(lambda r: r['SKU'] == sku, doc)
#             logger.info('found %d rows corresponding to sku %s' % (len(rows), sku))
#             yield sku, rows
#
#     # ---------------------------------------------------------------------------------------------------------
#     def is_fresher_and_is_new(uri, headers, doc_mod):
#         logger.debug('determining if doc info is fresher than db for sku %s' % sku)
#         resp = requests.get(uri, headers=headers, verify=False)
#         if resp.status_code == 404:
#             return True, True
#         resp = json.loads(resp.text)
#         db_mod = datetime.strptime(resp['modified'], '%Y-%m-%dT%H:%M:%S.%f')
#         if db_mod > doc_mod:
#             logger.debug('db is fresher, skipping parse for sku %s' % sku)
#             return False, False
#         logger.info('doc is fresher for sku %s' % sku)
#         return True, False
#
#     # ---------------------------------------------------------------------------------------------------------
#     def popularity(rows, col, default):
#         freqs = Counter([
#             r[col] for r in rows
#             if len(r[col])
#         ])
#         try:
#             return sorted(freqs.items(), key=lambda r: r[1], reverse=True)[0][0]
#         except IndexError:
#             logger.error('couldn\'t get good data for col %s. using default value %s' % (col, default))
#             return default
#
#     # ---------------------------------------------------------------------------------------------------------
#     def latest(rows, comp_col, out_col, default):
#         try:
#             value = max(rows, key=lambda r:
#                 datetime.strptime(r[comp_col], '%m/%d/%Y')
#                 if re.match(r'\d{1,2}/\d{1,2}/\d{4}', r[comp_col])
#                 else datetime(1985, 8, 3)
#             )[out_col]
#             if len(value):
#                 return value
#             return default
#         except (ValueError, IndexError, KeyError):
#             logger.error('couldn\'t get good data for col %s. using default value %s' % (out_col, default))
#             return default
#
#     # ---------------------------------------------------------------------------------------------------------
#     def slug_popularity(rows, col, default, lookup, uri, key, headers):
#         winner = popularity(rows, col, default)
#         if winner is None:
#             return winner
#         slug = slugify(winner)
#         if slug in lookup:
#             return lookup[slug]
#         logger.debug('creating new resource for %s: %s' % (col, winner))
#         resp = requests.post(uri, data=json.dumps({key: winner}), headers=headers, verify=False)
#         resp = json.loads(resp.text)
#         lookup[slug] = resp['resource_uri']
#         return resp['resource_uri']
#
#     # ---------------------------------------------------------------------------------------------------------
#     def split_and_use_all(rows, delimiters, col, lookup, uri, key, headers):
#         values = []
#         for r in rows:
#             values.extend(re.split(delimiters, r[col]))
#         values = set([value for value in values if len(value)])
#         for value in values:
#             slug = slugify(value)
#             if slug in lookup:
#                 yield lookup[slug]
#             else:
#                 logger.debug('creating new resource for %s: %s' % (col, value))
#                 resp = requests.post(uri, data=json.dumps({key: value}), headers=headers, verify=False)
#                 resp = json.loads(resp.text)
#                 lookup[slug] = resp['resource_uri']
#                 yield resp['resource_uri']
#
#     # ---------------------------------------------------------------------------------------------------------
#     def get_attribute(rows, col, attr, lookup, res_uri, uri, headers):
#         try:
#             value = sorted(
#                 Counter([r[col] for r in rows if len(r[col]) and r[col] != '0' and r[col] != '-']),
#                 key=lambda x: x[1], reverse=True
#             )[0]
#             payload = {
#                 'product': res_uri,
#                 'attribute': lookup[attr],
#                 'value': value
#             }
#             logger.info('built payload %s' % payload)
#             resp = requests.post(uri, data=json.dumps(payload), headers=headers, verify=False)
#             logger.info('attribute response code %s' % resp.status_code)
#             resp = json.loads(resp.text)
#         except (ValueError, IndexError):
#             logger.debug('no attribute to be had for %s' % col)
#             pass
#     # ===========================================================================================================
#
#
#     # make headers
#     headers = {'Authorization': 'ApiKey %s' % api_key, 'Content-Type': 'application/json'}
#
#     # get resources
#     logger.info('getting support resources')
#     categories = get_supporting_resources(list_uri % ('inventory-manager', 'categories') + '?limit=0', headers)
#     attributes = get_supporting_resources(list_uri % ('inventory-manager', 'attributes') + '?limit=0', headers)
#     manufacturers = get_supporting_resources(list_uri % ('inventory-manager', 'manufacturers') + '?limit=0', headers)
#     suppliers = get_supporting_resources(list_uri % ('dat', 'suppliers') + '?limit=0', headers)
#
#     # get skus; iterate
#     for sku, rows in generate_skus_and_rows(doc):
#         # clear out N/A values
#         for row in rows:
#             for key, value in row.iteritems():
#                 if value.lower().endswith('n/a'):
#                     row[key] = ''
#
#         # determine freshness and newness
#         logger.info('getting doc mod date')
#         try:
#             doc_mod = max([
#                 datetime.strptime(r['Date Received / Updated'], '%m/%d/%Y') for r in rows
#                 if re.match('\d{2}/\d{2}/\d{4}', r['Date Received / Updated'])
#             ])
#             is_fresher, is_new_product = is_fresher_and_is_new(
#                 detail_uri % ('inventory-manager', 'products', sku), headers, doc_mod)
#         except ValueError:
#             logger.error('no dates found. skipping sku')
#             is_fresher, is_new_product = False, False
#         if not is_fresher:
#             continue
#
#         ## build out product information
#         # name
#         name = popularity(rows, 'Product', '(unknown)')
#
#         # qty
#         qty = latest(rows, 'Date Received / Updated', 'Total SKU Quantity', 0)
#         try:
#             int(float(qty))
#         except ValueError:
#             qty = 0
#
#         # location
#         location = latest(rows, 'Date Received / Updated', 'Location', '(unknown)')
#
#         # mfr
#         manufacturer = slug_popularity(
#             rows, 'Manufacturer', None, manufacturers, list_uri % ('inventory-manager', 'manufacturers'),
#             'name', headers)
#         if manufacturer is None:
#             manufacturer = '/api/inventory-manager/manufacturers/unknown/'
#
#         # supp
#         supplier = slug_popularity(
#             rows, 'Supplier', None, suppliers, list_uri % ('dat', 'suppliers'), 'name', headers)
#         if supplier is None:
#             supplier = '/api/dat/suppliers/unknown/'
#
#         # cat
#         cats = [cat for cat in split_and_use_all(
#             rows, r'/|-', 'Type (Toy/ Treat/ Chew/  More)', categories, list_uri % ('inventory-manager', 'categories'),
#             'name', headers)]
#         if not len(cats):
#             cats = ['/api/inventory-manager/categories/more/', ]
#
#         # filler
#         owner = '/api/auth/users/3/'  # dat account = 3
#         reorder = 0
#         price = 0
#         cost = 0
#         mfr_sku = '(unknown)'
#         case = 0
#
#         # make product
#         product = {
#             'sku': sku, 'name': name, 'qty_on_hand': qty, 'location': location, 'manufacturer': manufacturer,
#             'supplier': supplier, 'categories': cats, 'owner': owner, 'reorder_threshold': reorder,
#             'price': price, 'cost': cost, 'mfr_sku': mfr_sku, 'case_qty': case
#         }
#         logger.info('build payload: %s' % product)
#         if is_new_product:
#             resp = requests.post(
#                 list_uri % ('inventory-manager', 'products'), data=json.dumps(product), headers=headers, verify=False)
#         else:
#             del product['sku']
#             resp = requests.patch(
#                 detail_uri % ('inventory-manager', 'products', sku), data=json.dumps(product), headers=headers, verify=False)
#         logger.info('response code %s' % resp.status_code)
#         resp = json.loads(resp.text)
#         prod = resp['resource_uri']
#
#         # get attributes
#         logger.info('working with attributes')
#         get_attribute(
#             rows, 'size (ounces for treats)', 'weight', attributes, prod,
#             list_uri % ('inventory-manager', 'product-attributes'), headers)
#
#         get_attribute(
#             rows, 'Size', 'style', attributes, prod, list_uri % ('inventory-manager', 'product-attributes'),
#             headers)
#
#         get_attribute(
#             rows, 'Style', 'size', attributes, prod, list_uri % ('inventory-manager', 'product-attributes'),
#             headers)
#
#         get_attribute(
#             rows, 'Color', 'color', attributes, prod, list_uri % ('inventory-manager', 'product-attributes'),
#             headers)
#
#         get_attribute(
#             rows, 'Flavor', 'flavor', attributes, prod, list_uri % ('inventory-manager', 'product-attributes'),
#             headers)
#
#         get_attribute(
#             rows, 'Bulk?', 'is-bulk', attributes, prod, list_uri % ('inventory-manager', 'product-attributes'),
#             headers)
#
#         get_attribute(
#             rows, 'Expiration', 'expiration-date', attributes, prod,
#             list_uri % ('inventory-manager', 'product-attributes'), headers)
#
#         get_attribute(
#             rows, 'Made In', 'country-of-origin', attributes, prod,
#             list_uri % ('inventory-manager', 'product-attributes'), headers)
