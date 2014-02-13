from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify


# choices for state fields
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
    """model for product suppliers/vendors"""

    slug = models.SlugField(max_length=255, unique=True)
    name = models.CharField(max_length=255, unique=True)
    ships_products = models.BooleanField(default=False)
    terms = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        """slugifies the name and saves"""
        self.slug = slugify(self.name)
        super(Supplier, self).save(*args, **kwargs)


class ContactLabel(models.Model):
    """control model for labeling contacts"""

    slug = models.SlugField(max_length=255, unique=True)
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        """slugifies the name and saves"""
        self.slug = slugify(self.name)
        super(ContactLabel, self).save(*args, **kwargs)


class Contact(models.Model):
    """model for contacts at suppliers"""

    slug = models.SlugField(max_length=310, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=255)
    fax = models.CharField(max_length=255, blank=True, null=True)
    address1 = models.CharField('Address', max_length=255)
    address2 = models.CharField('Address', max_length=255, blank=True, null=True)
    address3 = models.CharField('Address', max_length=255, blank=True, null=True)
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
        return u'%s @ %s' % (self.name, self.represents.name)

    def save(self, *args, **kwargs):
        """slugifies the name and saves"""
        self.slug = slugify(' '.join([self.name, self.represents.name]))
        super(Contact, self).save(*args, **kwargs)


class Receiver(models.Model):
    """model for shipping destinations, i.e. warehouses, offices"""

    slug = models.SlugField(max_length=255, unique=True)
    name = models.CharField(max_length=255, unique=True)
    address1 = models.CharField('Address', max_length=255)
    address2 = models.CharField('Address', max_length=255, blank=True, null=True)
    address3 = models.CharField('Address', max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2, choices=STATES)
    zipcode = models.CharField(max_length=255)
    country = models.CharField(max_length=255, default='United States')

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        """slugifies the name and saves"""
        self.slug = slugify(self.name)
        super(Receiver, self).save(*args, **kwargs)


class PurchaseOrder(models.Model):
    """model for purchase orders"""

    slug = models.SlugField(max_length=255)
    supplier = models.ForeignKey(Supplier)
    contact = models.ForeignKey(Contact)
    ship_to = models.ForeignKey(Receiver)
    creator = models.ForeignKey(User)
    comments = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s on %s' % (self.slug, self.created.strftime('%Y-%m-%d'))

    def save(self, *args, **kwargs):
        """slugifies the id and username, then commits the slug change"""
        super(PurchaseOrder, self).save(*args, **kwargs)
        self.slug = slugify(' '.join([str(self.id), self.creator.username.strip('@doggyloot.com')]))
        super(PurchaseOrder, self).save(*args, **kwargs)

    def has_been_received(self):
        """checks if id in list of ids associated with received shipments"""
        from apps.warehouse.models import Shipment
        shipments = Shipment.objects.values_list('purchase_order__id')
        return self.id in shipments[0]


class PurchaseOrderProduct(models.Model):
    """model for purchase order line items"""

    slug = models.SlugField(max_length=255)
    purchase_order = models.ForeignKey(PurchaseOrder)
    product = models.ForeignKey('inventory_manager.Product')
    disc_dollar = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    disc_percent = models.IntegerField(blank=True, null=True)
    qty_ordered = models.IntegerField()

    def __unicode__(self):
        return u'%d : %d' % (self.product.sku, self.qty_ordered)

    def save(self, *args, **kwargs):
        """slugifies the po id and the product sku, and then saves"""
        self.slug = slugify(' '.join([str(self.purchase_order.id), str(self.product.sku)]))
        super(PurchaseOrderProduct, self).save(*args, **kwargs)
