from django.contrib.auth.models import User
from django.db import models

from inventory_manager.models import ProductQtyChange, QtyChangeReason
from dat.models import PurchaseOrderProduct


class Shipment(models.Model):

    purchase_order = models.ForeignKey('dat.PurchaseOrder')
    received_by = models.ForeignKey(User)
    received_on = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'{} on {}'.format(self.purchase_order.name, self.received_on.strftime('%Y-%m-%d %I:%M%p'))


class ShipmentProduct(models.Model):

    shipment = models.ForeignKey(Shipment)
    product = models.ForeignKey('inventory_manager.Product')
    qty_received = models.IntegerField()

    def __unicode__(self):
        prod = PurchaseOrderProduct.objects.get(purchase_order=self.shipment.purchase_order, product=self.product)
        return u'[{}] {}: {} of {}'.format(self.shipment.purchase_order.name, self.product.sku,
                                           self.qty_received, prod.qty_ordered)

    def save(self, *args, **kwargs):
        pqc = ProductQtyChange()
        pqc.product = self.product
        pqc.new_qty = self.product.qty_on_hand + self.qty_received
        pqc.reason = QtyChangeReason.objects.get(pk='received-shipment')
        pqc.details = 'po "%s"' % self.shipment.purchase_order.name
        pqc.who = self.shipment.received_by
        pqc.save()
        super(ShipmentProduct, self).save(*args, **kwargs)
