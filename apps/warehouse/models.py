from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify


class Shipment(models.Model):
    """model for holding shipment data - tied to purchase orders"""

    slug = models.SlugField(max_length=255)
    purchase_order = models.ForeignKey('dat.PurchaseOrder')
    received_by = models.ForeignKey(User)
    received_on = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s on %s' % (self.slug, self.received_on.strftime('%Y-%m-%d'))

    def save(self, *args, **kwargs):
        """slugifies the id and username, then commits the slug change"""
        super(Shipment, self).save(*args, **kwargs)
        self.slug = slugify(' '.join([str(self.id), self.received_by.username.strip('@doggyloot.com')]))
        super(Shipment, self).save(*args, **kwargs)


class ShipmentProduct(models.Model):
    """model for shipment line items"""

    slug = models.SlugField(max_length=255)
    shipment = models.ForeignKey(Shipment)
    product = models.ForeignKey('inventory_manager.Product')
    qty_received = models.IntegerField()

    def __unicode__(self):
        return u'%d : %d' % (self.product.sku, self.qty_received)

    def save(self, *args, **kwargs):
        """performs a qty change for product and then saves line item"""
        from apps.inventory_manager.models import ProductQtyChange, QtyChangeReason
        pqc = ProductQtyChange()
        pqc.product = self.product
        pqc.new_qty = self.product.qty_on_hand + self.qty_received
        pqc.reason = QtyChangeReason.objects.get(pk='received-shipment')
        pqc.details = 'po "%s"' % self.shipment.purchase_order.slug
        pqc.who = self.shipment.received_by
        pqc.save()
        self.slug = slugify(' '.join([str(self.shipment.id), str(self.product.sku)]))
        super(ShipmentProduct, self).save(*args, **kwargs)
