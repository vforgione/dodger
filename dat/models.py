from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify


STATES = (
    ('AL', 'Alabama'),
    ('AK', 'Alaska'),
    ('AZ', 'Arizona'),
    ('AR', 'Arkansas'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DE', 'Delaware'),
    ('DC', 'District of Columbia'),
    ('FL', 'Florida'),
    ('GA', 'Georgia'),
    ('HI', 'Hawaii'),
    ('ID', 'Idaho'),
    ('IL', 'Illinois'),
    ('IN', 'Indiana'),
    ('IA', 'Iowa'),
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('ME', 'Maine'),
    ('MT', 'Montana'),
    ('NE', 'Nebraska'),
    ('NV', 'Nevada'),
    ('NH', 'New Hampshire'),
    ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),
    ('NY', 'New York'),
    ('NC', 'North Carolina'),
    ('ND', 'North Dakota'),
    ('OH', 'Ohio'),
    ('OK', 'Oklahoma'),
    ('OR', 'Oregon'),
    ('MD', 'Maryland'),
    ('MA', 'Massachusetts'),
    ('MI', 'Michigan'),
    ('MN', 'Minnesota'),
    ('MS', 'Mississippi'),
    ('MO', 'Missouri'),
    ('PA', 'Pennsylvania'),
    ('RI', 'Rhode Island'),
    ('SC', 'South Carolina'),
    ('SD', 'South Dakota'),
    ('TN', 'Tennessee'),
    ('TX', 'Texas'),
    ('UT', 'Utah'),
    ('VT', 'Vermont'),
    ('VA', 'Virginia'),
    ('WA', 'Washington'),
    ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'),
    ('WY', 'Wyoming'),
)


class Supplier(models.Model):

    id = models.SlugField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    ships_products = models.BooleanField(default=False)
    terms = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = slugify(self.name)
        super(Supplier, self).save(*args, **kwargs)


class ContactLabel(models.Model):

    id = models.SlugField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = slugify(self.name)
        super(ContactLabel, self).save(*args, **kwargs)


class Contact(models.Model):

    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=255)
    fax = models.CharField(max_length=255, blank=True, null=True)
    address0 = models.CharField('Address', max_length=255)
    address1 = models.CharField('Address 2', max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2, choices=STATES)
    zipcode = models.CharField(max_length=255)
    country = models.CharField(max_length=255, default='United States')
    label = models.ForeignKey(ContactLabel)
    represents = models.ForeignKey(Supplier)

    class Meta:
        unique_together = (
            ('name', 'represents'),
        )

    def __unicode__(self):
        return u'{} @ {}'.format(self.name, self.represents.name)


class Receiver(models.Model):

    name = models.CharField(max_length=255, unique=True)
    address0 = models.CharField('Address', max_length=255)
    address1 = models.CharField('Address 2', max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2, choices=STATES)
    zipcode = models.CharField(max_length=255)
    country = models.CharField(max_length=255, default='United States')

    def __unicode__(self):
        return self.name


class PurchaseOrder(models.Model):

    supplier = models.ForeignKey(Supplier)
    contact = models.ForeignKey(Contact)
    ship_to = models.ForeignKey(Receiver)
    dat_member = models.ForeignKey(User)
    comments = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return u'{} @ {}'.format(self.name, self.created.strftime('%Y-%m-%d'))

    def save(self, *args, **kwargs):
        super(PurchaseOrder, self).save(*args, **kwargs)
        self.name = '%d-%s' % (self.id, self.dat_member.last_name)
        super(PurchaseOrder, self).save(*args, **kwargs)

    def has_been_received(self):
        from warehouse.models import Shipment
        shipments = Shipment.objects.values_list('purchase_order__id')
        return self.id in shipments


class PurchaseOrderProduct(models.Model):

    purchase_order = models.ForeignKey(PurchaseOrder)
    product = models.ForeignKey('inventory_manager.Product')
    disc_dollar = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    disc_percent = models.IntegerField(blank=True, null=True)
    qty_ordered = models.IntegerField()

    def __unicode__(self):
        return u'[{}] {} - Qty: {}'.format(self.purchase_order.name, str(self.product), self.qty_ordered)
