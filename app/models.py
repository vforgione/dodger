from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify

from .controls import STATES


class Supplier(models.Model):
    """model for suppliers/vendors control for sku"""

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    """model for the category control for sku"""

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Brand(models.Model):
    """model for the brand control for sku"""

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Attribute(models.Model):
    """model for attribute controls for skus"""

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Sku(models.Model):
    """individual sellable item"""

    # id
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    # categorization
    categories = models.ManyToManyField(Category)
    supplier = models.ForeignKey(Supplier)
    brand = models.ForeignKey(Brand)
    # responsibility
    owner = models.ForeignKey(User)
    reorder_threshold = models.PositiveIntegerField(default=0)
    notify_at_threshold = models.BooleanField(default=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    mfr_sku = models.CharField(max_length=255, blank=True, null=True)
    case_qty = models.PositiveIntegerField()
    # inventory
    location = models.CharField(max_length=255, blank=True, null=True)
    qty_on_hand = models.IntegerField()
    # stamps
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.id:  # new sku
            self.id = Sku.objects.all().aggregate(models.Max('id'))['id__max'] + 1
            super(Sku, self).save(*args, **kwargs)
        else:  # existing sku
            if 'qty_change' in kwargs:  # save triggered by qty change model
                del kwargs['qty_change']
                super(Sku, self).save(*args, **kwargs)
            elif 'gdocs' in kwargs:
                del kwargs['gdocs']
                super(Sku, self).save(*args, **kwargs)
            else:  # change from elsewhere - verify qty is same
                try:
                    existing = Sku.objects.get(pk=self.pk)
                    assert existing.qty_on_hand == self.qty_on_hand
                except Sku.DoesNotExist:
                    pass
                super(Sku, self).save(*args, **kwargs)

    def get_attributes(self):
        attrs = []
        queryset = SkuAttribute.objects.filter(sku=self)
        for obj in queryset:
            if obj.attribute.name.lower().endswith('bulk'):
                attrs.append('Bulk')
            else:
                attrs.append(obj.value)
        return attrs

    def _description(self):
        attrs = self.get_attributes()
        if len(attrs):
            desc = '[%d] %s %s : %s' % (self.id, self.brand.name, self.name, ', '.join(attrs))
        else:
            desc = '[%d] %s %s' % (self.id, self.brand.name, self.name)
        return ''.join([c for c in desc if ord(c) < 128])
    description = property(_description)

    def __str__(self):
        return self.description


class SkuAttribute(models.Model):
    """attribute values for skus"""

    sku = models.ForeignKey(Sku)
    attribute = models.ForeignKey(Attribute)
    value = models.CharField(max_length=255)

    class Meta:
        unique_together = (
            ('sku', 'attribute'),
        )


class ChangeReason(models.Model):
    """abstract for future _change models"""

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class QuantityAdjustmentReason(ChangeReason):
    """model for qty change control for skus"""

    def __init__(self, *args, **kwargs):
        super(QuantityAdjustmentReason, self).__init__(*args, **kwargs)


class SkuQuantityAdjustment(models.Model):
    """model to trace attribute blame for qty changes"""

    sku = models.ForeignKey(Sku)
    old = models.IntegerField()
    new = models.IntegerField()
    who = models.ForeignKey(User)
    reason = models.ForeignKey(QuantityAdjustmentReason)
    detail = models.TextField(blank=True, null=True)
    when = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.old = self.sku.qty_on_hand
        super(SkuQuantityAdjustment, self).save(*args, **kwargs)
        self.sku.qty_on_hand = self.new
        self.sku.save(qty_change=True)

    def __str__(self):
        return 'SKU %d : from %d to %d on %s by %s' % (
            self.sku.id, self.old, self.new, self.when.strftime('%x'), self.who.username
        )


class ContactLabel(models.Model):
    """model for label control for contacts"""

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Contact(models.Model):
    """model for contact info for a supplier - used to build POs"""

    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    fax = models.CharField(max_length=255, blank=True, null=True)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    address3 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255, choices=STATES)
    zipcode = models.CharField(max_length=255)
    country = models.CharField(max_length=255, default='United States')
    represents = models.ForeignKey(Supplier)
    label = models.ForeignKey(ContactLabel)

    def __str__(self):
        return self.name

    def _description(self):
        return '%s @ %s (%s)' % (self.name, self.represents.name, self.label.name)
    description = property(_description)

    class Meta:
        unique_together = (
            ('name', 'represents'),
        )


class Receiver(models.Model):
    """model for a POs destination"""

    name = models.CharField(max_length=255, unique=True)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    address3 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255, choices=STATES)
    zipcode = models.CharField(max_length=255)
    country = models.CharField(max_length=255, default='United States')

    def __str__(self):
        return self.name


class PurchaseOrder(models.Model):
    """model for header information of a po"""

    supplier = models.ForeignKey(Supplier)
    contact = models.ForeignKey(Contact)
    receiver = models.ForeignKey(Receiver)
    creator = models.ForeignKey(User)
    comments = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.friendly_name

    def _has_been_received(self):
        """checks if id in list of ids associated with received shipments"""
        try:
            Shipment.objects.get(purchase_order__id=self.id)
            return True
        except Shipment.DoesNotExist:
            return False
    has_been_received = property(_has_been_received)

    def _friendly_name(self):
        return slugify('%d %s' % (self.id, self.creator.username.strip('@doggyloot.com')))
    friendly_name = property(_friendly_name)


class PurchaseOrderLineItem(models.Model):
    """model for line items (skus) in a PO"""

    purchase_order = models.ForeignKey(PurchaseOrder)
    sku = models.ForeignKey(Sku)
    disc_dollar = models.FloatField(blank=True, null=True)
    disc_percent = models.FloatField(blank=True, null=True)
    qty_ordered = models.PositiveIntegerField()
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)


class Shipment(models.Model):
    """model for a processed shipment (received PO)"""

    purchase_order = models.ForeignKey(PurchaseOrder)
    received_by = models.ForeignKey(User)
    received_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.friendly_name

    def _friendly_name(self):
        return slugify('%d %s' % (self.id, self.received_by.username.strip('@doggyloot.com')))
    friendly_name = property(_friendly_name)


class ShipmentLineItem(models.Model):
    """model for line items (skus) in a shipment"""

    shipment = models.ForeignKey(Shipment)
    sku = models.ForeignKey(Sku)
    qty_received = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        trace = SkuQuantityAdjustment()
        trace.sku = self.sku
        trace.new = trace.sku.qty_on_hand + self.qty_received
        trace.reason = QuantityAdjustmentReason.objects.get(name='Received Shipment')
        trace.detail = 'received %d units on %s - <a href="/purchase-order/%d/">PO %s</a>' % (
            self.qty_received, self.shipment.received_on.strftime('%Y-%m-%d %H:%M:%S'),
            self.shipment.purchase_order.pk, self.shipment.purchase_order.friendly_name
        )
        trace.who = self.shipment.received_by
        trace.save()
        super(ShipmentLineItem, self).save(*args, **kwargs)
