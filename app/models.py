from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models

from constants import US_STATES, ACTIONS


# control models
class ControlModel(models.Model):
    """an abstract model that only contains a name - serves as a control for selection options"""

    class Meta:
        abstract = True
        ordering = ('name', )

    name = models.CharField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name


class Attribute(ControlModel):

    def get_absolute_url(self):
        return reverse('app:attribute__view', args=[str(self.pk)])


class Brand(ControlModel):

    def get_absolute_url(self):
        return reverse('app:brand__view', args=[str(self.pk)])


class Category(ControlModel):

    def get_absolute_url(self):
        return reverse('app:category__view', args=[str(self.pk)])


class ContactLabel(ControlModel):

    def get_absolute_url(self):
        return reverse('app:contact_label__view', args=[str(self.pk)])


class CostAdjustmentReason(ControlModel):

    def get_absolute_url(self):
        return reverse('app:cost_adjustment_reason__view', args=[str(self.pk)])


class QuantityAdjustmentReason(ControlModel):

    def get_absolute_url(self):
        return reverse('app:quantity_adjustment_reason__view', args=[str(self.pk)])


class Supplier(ControlModel):

    def get_absolute_url(self):
        return reverse('app:supplier__view', args=[str(self.pk)])


# full models
class Sku(models.Model):

    class Meta:
        ordering = ('id', )

    # id
    id =                    models.IntegerField(primary_key=True)
    name =                  models.CharField(max_length=255, db_index=True)
    upc =                   models.CharField(max_length=255, blank=True, null=True, db_index=True, default=None)
    # categorization
    brand =                 models.ForeignKey(Brand)
    categories =            models.ManyToManyField(Category)
    # inventory
    quantity_on_hand =      models.IntegerField(default=0, db_index=True)
    location =              models.CharField(max_length=255, blank=True, null=True, db_index=True, default=None)
    # dat team
    owner =                 models.ForeignKey(User)
    supplier =              models.ForeignKey(Supplier)
    lead_time =             models.IntegerField(blank=True, null=True, default=None)
    minimum_quantity =      models.IntegerField(default=0)
    notify_at_threshold =   models.BooleanField(default=False)
    cost =                  models.FloatField(blank=True, null=True, default=0)
    supplier_sku =          models.CharField(max_length=255, blank=True, null=True, default=None)
    case_quantity =         models.IntegerField(blank=True, null=True, default=None)
    in_live_deal =          models.BooleanField(default=False, db_index=True)
    is_subscription =       models.BooleanField(default=False, db_index=True)
    notes =                 models.CharField(max_length=255, blank=True, null=True, db_index=True, default=None)
    action =                models.CharField(max_length=255, choices=ACTIONS, blank=True, null=True, db_index=True, default=None)
    action_date =           models.CharField(max_length=255, blank=True, null=True, default=None)
    # stamp
    created =               models.DateTimeField(auto_now_add=True)
    modified =              models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.id:  # new sku
            self.id = Sku.objects.all().aggregate(models.Max('id'))['id__max'] + 1
            super(Sku, self).save(*args, **kwargs)
        else:  # existing sku
            if 'qty_change' in kwargs:
                del kwargs['qty_change']
                super(Sku, self).save(*args, **kwargs)
            elif 'cost_change' in kwargs:
                del kwargs['cost_change']
                super(Sku, self).save(*args, **kwargs)
            elif 'gdocs' in kwargs:
                del kwargs['gdocs']
                super(Sku, self).save(*args, **kwargs)
            else:
                old = Sku.objects.get(pk=self.pk)
                assert old.quantity_on_hand == self.quantity_on_hand
                assert old.cost == self.cost
                super(Sku, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('app:sku__view', args=[str(self.pk)])

    def _attributes(self):
        attrs = []
        # qs = SkuAttribute.objects.filter(sku=self)
        # for obj in qs:
        #     if obj.attribute.name.lower().endswith('bulk'):
        #         attrs.append('Bulk')
        #     elif obj.attribute.name.lower().endswith('date'):
        #         attrs.append('(%s) %s' % (obj.attribute.name.split()[0], obj.value))
        #     else:
        #         attrs.append(obj.value)
        for attr in self.skuattribute_set.all():
            attrs.append((attr.attribute.name, attr.value))
        return attrs
    attributes = property(_attributes)

    def _description(self):
        attrs = self.attributes
        if len(attrs):
            # return '[%d] %s %s : %s' % (self.id, self.brand, self.name, ', '.join(attrs))
            attrs = ', '.join(['(%s) %s' % (attr[0], attr[1]) for attr in attrs])
            return '[%d] %s %s : %s' % (self.id, self.brand, self.name, attrs)
        else:
            return '[%d] %s %s' % (self.id, self.brand, self.name)
    description = property(_description)

    def __str__(self):
        return ''.join([c for c in self.description if ord(c) < 128])


class SkuAttribute(models.Model):

    class Meta:
        ordering = ('sku__id', 'attribute__name')
        unique_together = (
            ('sku', 'attribute'),
        )

    sku = models.ForeignKey(Sku)
    attribute = models.ForeignKey(Attribute)
    value = models.CharField(max_length=255, db_index=True)

    def get_absolute_url(self):
        return reverse('app:sku_attribute__view', args=[str(self.pk)])

    def __str__(self):
        return '%s@%s : %s' % (self.sku.id, self.attribute.name, self.value)


class CostAdjustment(models.Model):

    class Meta:
        ordering = ('-created', )

    sku = models.ForeignKey(Sku)
    old = models.FloatField()
    new = models.FloatField()
    who = models.ForeignKey(User)
    reason = models.ForeignKey(CostAdjustmentReason)
    detail = models.TextField(blank=True, null=True, default=None)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.old = self.sku.cost
        super(CostAdjustment, self).save(*args, **kwargs)
        self.sku.cost = self.new
        self.sku.save(cost_change=True)

    def get_absolute_url(self):
        return reverse('app:cost_adjustment__view', args=[str(self.pk)])

    def __str__(self):
        return '[%s] %s to %s' % (self.sku.id, self.old, self.new)


class QuantityAdjustment(models.Model):

    class Meta:
        ordering = ('-created', )

    sku = models.ForeignKey(Sku)
    old = models.IntegerField()
    new = models.IntegerField()
    who = models.ForeignKey(User)
    reason = models.ForeignKey(QuantityAdjustmentReason)
    detail = models.TextField(blank=True, null=True, default=None)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.old = self.sku.quantity_on_hand
        super(QuantityAdjustment, self).save(*args, **kwargs)
        self.sku.quantity_on_hand = self.new
        self.sku.save(qty_change=True)

    def get_absolute_url(self):
        return reverse('app:quantity_adjustment__view', args=[str(self.pk)])

    def __str__(self):
        return '[%s] %s to %s' % (self.sku.id, self.old, self.new)


class Contact(models.Model):

    class Meta:
        ordering = ('name', 'represents')
        unique_together = (
            ('name', 'represents'),
        )

    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    work_phone = models.CharField(max_length=255)
    cell_phone = models.CharField(max_length=255, blank=True, null=True, default=None)
    fax = models.CharField(max_length=255, blank=True, null=True, default=None)
    address1 = models.CharField(max_length=255, blank=True, null=True, default=None)
    address2 = models.CharField(max_length=255, blank=True, null=True, default=None)
    address3 = models.CharField(max_length=255, blank=True, null=True, default=None)
    city = models.CharField(max_length=255, blank=True, null=True, default=None)
    state = models.CharField(max_length=255, choices=US_STATES, blank=True, null=True, default=None)
    zipcode = models.CharField(max_length=255, blank=True, null=True, default=None)
    country = models.CharField(max_length=255, default='United States', blank=True, null=True)
    represents = models.ForeignKey(Supplier)
    label = models.ManyToManyField(ContactLabel)

    def get_absolute_url(self):
        return reverse('app:contact__view', args=[str(self.pk)])

    def __str__(self):
        return '%s @ %s' % (self.name, self.represents.name)


class Receiver(models.Model):

    class Meta:
        ordering = ('name', )

    name = models.CharField(max_length=255, unique=True)
    address1 = models.CharField(max_length=255, blank=True, null=True, default=None)
    address2 = models.CharField(max_length=255, blank=True, null=True, default=None)
    address3 = models.CharField(max_length=255, blank=True, null=True, default=None)
    city = models.CharField(max_length=255, blank=True, null=True, default=None)
    state = models.CharField(max_length=255, choices=US_STATES, blank=True, null=True, default=None)
    zipcode = models.CharField(max_length=255, blank=True, null=True, default=None)
    country = models.CharField(max_length=255, default='United States', blank=True, null=True)

    def get_absolute_url(self):
        return reverse('app:receiver__view', args=[str(self.pk)])

    def __str__(self):
        return self.name


class PurchaseOrder(models.Model):

    class Meta:
        ordering = ('-created', )

    creator = models.ForeignKey(User)
    supplier = models.ForeignKey(Supplier)
    contact = models.ForeignKey(Contact)
    receiver = models.ForeignKey(Receiver)
    note = models.TextField(blank=True, null=True, default=None)
    created = models.DateTimeField(auto_now_add=True)
    terms = models.CharField(max_length=255)
    tracking_url = models.CharField(max_length=512, blank=True, null=True, default=None)
    shipping_cost = models.FloatField(default=0.0)
    sales_tax = models.FloatField(default=0.0)

    def get_absolute_url(self):
        return reverse('app:purchase_order__view', args=[str(self.pk)])

    def is_fully_received(self):
        po_li = dict(
            (li.sku.id, li.quantity_ordered) for li
            in PurchaseOrderLineItem.objects.filter(purchase_order=self)
        )
        qs = ShipmentLineItem.objects.filter(shipment__purchase_order=self)
        ship_li = {}
        for li in qs:
            ship_li.setdefault(li.sku.id, 0)
            ship_li[li.sku.id] += li.quantity_received
        for sku, qty in po_li.iteritems():
            if sku in ship_li:
                if qty > ship_li[sku]:
                    return False
            else:
                return False
        return True

    def _total_cost(self):
        return sum([li.total_cost for li in self.purchaseorderlineitem_set.all()]) + self.shipping_cost + self.sales_tax
    total_cost = property(_total_cost)

    def __str__(self):
        return '%s-%s' % (self.id, self.creator.username)


class PurchaseOrderLineItem(models.Model):

    class Meta:
        ordering = ('-purchase_order__id', 'sku__id')

    purchase_order = models.ForeignKey(PurchaseOrder)
    sku = models.ForeignKey(Sku)
    quantity_ordered = models.IntegerField()
    unit_cost = models.FloatField()
    discount_percent = models.FloatField(blank=True, null=True)
    discount_dollar = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        super(PurchaseOrderLineItem, self).save(*args, **kwargs)
        if self.unit_cost != self.sku.cost:
            ca = CostAdjustment(
                sku=self.sku,
                new=self.unit_cost,
                who=self.purchase_order.creator,
                reason=CostAdjustmentReason.objects.get(name='Supplier Adjustment'),
                detail='adjustment made during creation of <a href="%s">%s</a>' % (
                    self.purchase_order.get_absolute_url(), str(self.purchase_order))
            )
            ca.save()

    def get_absolute_url(self):
        return reverse('app:purchase_order_line_item__view', args=[str(self.pk)])

    def _adjusted_unit_cost(self):
        dp = self.discount_percent or 0
        dd = self.discount_dollar or 0
        dp /= 100.0
        return (self.unit_cost - (self.unit_cost * dp)) - dd
    adjusted_unit_cost = property(_adjusted_unit_cost)

    def _total_cost(self):
        return self.adjusted_unit_cost * self.quantity_ordered
    total_cost = property(_total_cost)

    def __str__(self):
        return '[%s] %s' % (self.sku.id, self.quantity_ordered)


class Shipment(models.Model):

    class Meta:
        ordering = ('-created', )

    creator = models.ForeignKey(User)
    purchase_order = models.ForeignKey(PurchaseOrder)
    note = models.TextField(blank=True, null=True, default=None)
    created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('app:shipment__view', args=[str(self.pk)])

    def __str__(self):
        return '%s-%s' % (self.id, self.creator.username)


class ShipmentLineItem(models.Model):

    class Meta:
        ordering = ('-shipment__id', 'sku__id')

    shipment = models.ForeignKey(Shipment)
    sku = models.ForeignKey(Sku)
    quantity_received = models.IntegerField()

    def save(self, *args, **kwargs):
        adj = QuantityAdjustment()
        adj.sku = self.sku
        adj.new = self.sku.quantity_on_hand + self.quantity_received
        adj.reason = QuantityAdjustmentReason.objects.get(name='Received Shipment')
        adj.detail = 'received %s units on %s in shipment <a href="%s">%s</a>' % (
            self.quantity_received, self.shipment.created.strftime('%x'), self.shipment.get_absolute_url(),
            str(self.shipment)
        )
        adj.who = self.shipment.creator
        adj.save()
        super(ShipmentLineItem, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('app:shipment_line_item__view', args=[str(self.pk)])

    def __str__(self):
        return '[%s] %s' % (self.sku.id, self.quantity_received)
