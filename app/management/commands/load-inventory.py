import codecs
import csv
from datetime import datetime
import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from app.models import QuantityAdjustment, QuantityAdjustmentReason, Sku


QAR, _ = QuantityAdjustmentReason.objects.get_or_create(name='Inventory Load Up')

ROLLBACK, _ = QuantityAdjustmentReason.objects.get_or_create(name='Inventory Rollback')

USER = User.objects.get(email='vince@doggyloot.com')


class Command(BaseCommand):

    def handle(self, *args, **options):
        # get cutoff date
        try:
            cutoff = datetime.strptime(args[0], '%Y-%m-%d')
        except Exception, e:
            raise CommandError(e)

        # get filename
        filename = args[1]
        if not os.path.isfile(filename):
            raise CommandError('%s is not a recognized file' % str(filename))

        # roll back quantity adjustments made on/after cutoff
        adjs = QuantityAdjustment.objects.filter(created__gte=cutoff)
        for adj in adjs:
            sku = adj.sku
            rollback = QuantityAdjustment(
                sku=sku,
                new=adj.old,
                who=USER,
                reason=ROLLBACK,
                detail='rollback quantity adjustment <a href="%s">%s</a>' % (adj.get_absolute_url(), str(adj))
            )
            rollback.save()
            rollback.created = cutoff  # overwrite date
            rollback.save()

        # load adjustments from file
        skus_not_found = []
        with codecs.open(filename, 'r', encoding='utf8') as fh:
            reader = csv.reader(fh)
            for _id, qty, location in reader:
                qty = qty or 0  # replace `None` values
                try:
                    sku = Sku.objects.get(id=_id)
                except Sku.DoesNotExist:
                    skus_not_found.append(_id)
                if location not in (None, ''):
                    sku.location = location
                    sku.save()
                adj = QuantityAdjustment(
                    sku=sku,
                    new=qty,
                    who=USER,
                    reason=QAR,
                    detail='inventory count - %s' % cutoff.strftime('%x')
                )
                adj.save()
                adj.created = cutoff
                adj.save()

        # alert superfluous skus
        if len(skus_not_found):
            self.stderr.write('the following skus were not found in the database and their adjustments '
                              'were not applied: %s' % str(skus_not_found))

        # apply rolled back adjustments
        for adj in adjs:
            delta = adj.new - adj.old
            sku = Sku.objects.get(id=adj.sku.id)
            if adj.reason.name == 'Spot Count':
                new = adj.new
            else:
                new = sku.quantity_on_hand + delta
            adj.sku = sku
            adj.new = new
            adj.old = sku.quantity_on_hand
            adj.save()
