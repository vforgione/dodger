from django.core.management.base import BaseCommand

from app.models import Sku


class Command(BaseCommand):

    def handle(self, *args, **options):
        # get skus with 0 qty
        skus = Sku.objects.filter(quantity_on_hand=0)

        # iterate
        for sku in skus:
            # null out current location
            if sku.location is not None:
                sku.last_location = sku.location
                sku.location = None

            # null out expiration date
            attrs = sku.skuattribute_set.all()
            for attr in attrs:
                if attr.attribute.name.lower == 'expiration date':
                    attr.value = None
                    try:
                        attr.save()
                    except Exception as e:
                        self.stderr.write(str(e))
                    break

            # update sku
            try:
                sku.save()
            except Exception as e:
                self.stderr.write(str(e))
