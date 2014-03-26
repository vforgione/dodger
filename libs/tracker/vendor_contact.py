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

from app.models import Supplier, Contact


def import_vendor_contact(filename):
    with codecs.open(filename, 'r', encoding='utf8') as fh:
        reader = csv.DictReader(fh)

        for row in reader:

            for key, value in row.iteritems():
                row[key] = ''.join([c for c in value if ord(c) < 128])
                if not len(value):
                    row[key] = None

            supplier = row['supplier']

            name = row['contact_name']
            addr1 = row['addr1']
            addr2 = row['addr2']
            city_line = row['city']
            phone = row['phone']
            email = '%s@%s.com' % (name.replace(' ', '_'), supplier.replace(' ', '_'))

            if city_line is not None:
                city, state_zip = city_line.split(',')[0], city_line.split(',')[1]
                state_zip = state_zip.strip()
                try:
                    state, zipcode = state_zip.split(' ')
                except ValueError:
                    state = state_zip
                    zipcode = None
            else:
                city, state, zipcode = None, None, None

            if phone is None:
                phone = '-'

            supp, _ = Supplier.objects.get_or_create(name=supplier)
            print supp, _

            cont, _ = Contact.objects.get_or_create(
                name=name,
                email=email,
                work_phone=phone,
                address1=addr1,
                address2=addr2,
                city=city,
                state=state,
                zipcode=zipcode,
                country='USA',
                represents=supp,
            )
            print cont, _




if __name__ == '__main__':
    import sys
    filename = sys.argv[1]
    import_vendor_contact(filename)
