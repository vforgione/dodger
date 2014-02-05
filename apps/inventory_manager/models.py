from datetime import datetime, timedelta
import pytz

from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify


class Category(models.Model):
    """model for category control"""

    slug = models.SlugField(max_length=255, unique=True)
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        """slugifies name and saves"""
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class Manufacturer(models.Model):
    """model for manufacturer control"""

    slug = models.SlugField(max_length=255, unique=True)
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        """slugifies name and saves"""
        self.slug = slugify(self.name)
        super(Manufacturer, self).save(*args, **kwargs)


class Attribute(models.Model):
    """model for attribute control"""

    slug = models.SlugField(max_length=255, unique=True)
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        """slugifies name and saves"""
        self.slug = slugify(self.name)
        super(Attribute, self).save(*args, **kwargs)


class Product(models.Model):
    """model for products - kinda complicated so look for inline comments"""

    # id
    sku = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    # classification
    categories = models.ManyToManyField(Category)
    supplier = models.ForeignKey('dat.Supplier')
    manufacturer = models.ForeignKey(Manufacturer)
    # responsibility
    owner = models.ForeignKey(User)
    reorder_threshold = models.IntegerField(default=0)
    notify_at_threshold = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    mfr_sku = models.CharField(max_length=255, blank=True, null=True)
    case_qty = models.IntegerField()
    # required attributes
    location = models.CharField(max_length=255)
    qty_on_hand = models.IntegerField()
    # time stamps
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'%d' % self.sku

    def save(self, *args, **kwargs):
        """if new, creates sku; else, performs checks for controlled updates and will save only if safe changes found"""
        if not self.sku:  # new product
            sku_max = Product.objects.all().aggregate(models.Max('sku'))
            self.sku = sku_max['sku__max'] + 1
        else:  # existing product - check if change model was used
            try:
                prod = Product.objects.get(sku=self.sku)
            except Product.DoesNotExist:
                super(Product, self).save(*args, **kwargs)
                return
            qty = prod.qty_on_hand
            price = prod.price
            cost = prod.cost
            utc = pytz.UTC
            now = datetime.now(tz=utc)
            # note: `if mod is None` will happen if there is no previous change object
            if self.qty_on_hand != qty:
                change = ProductQtyChange.objects.all().filter(product__sku=self.sku).aggregate(models.Max('modified'))
                mod = change['modified__max']
                if mod is None or (now - mod) > timedelta(seconds=1):
                    raise Exception('illegal qty change from prod form')
            elif self.price != price:
                change = ProductPriceChange.objects.all().filter(product__sku=self.sku)\
                    .aggregate(models.Max('modified'))
                mod = change['modified__max']
                if mod is None or (now - mod) > timedelta(seconds=1):
                    raise Exception('illegal price change from prod form')
            elif self.cost != cost:
                change = ProductCostChange.objects.all().filter(product__sku=self.sku).aggregate(models.Max('modified'))
                mod = change['modified__max']
                if mod is None or (now - mod) > timedelta(seconds=1):
                    raise Exception('illegal cost change from prod form')
        super(Product, self).save(*args, **kwargs)

    def get_attributes(self):
        """returns a list of attribute values"""
        attributes = []
        qs = ProductAttribute.objects.all().filter(product=self)
        for row in qs:
            if row.attribute.name.lower().endswith('bulk'):
                attributes.append('Bulk')
            else:
                attributes.append(row.value)
        return attributes

    def _description(self):
        """pretty output"""
        attributes = self.get_attributes()
        if len(attributes):
            return u'[%d] %s : %s' % (self.sku, self.name, u', '.join(attributes))
        return u'[%d] %s' % (self.sku, self.name)

    description = property(_description)


class ProductAttribute(models.Model):
    """model for storing values of attributes for a product"""

    slug = models.SlugField(max_length=255)
    product = models.ForeignKey(Product)
    attribute = models.ForeignKey(Attribute)
    value = models.CharField(max_length=255)

    def __unicode__(self):
        return u'%s@%s : %s' % (self.product.name, self.attribute.name, self.value)

    def save(self, *args, **kwargs):
        """slugifies product sku, attribute name and value, then saves"""
        self.slug = slugify(' '.join([str(self.product.sku), self.attribute.name, self.value]))
        super(ProductAttribute, self).save(*args, **kwargs)


class QtyChangeReason(models.Model):
    """model for qty change control"""

    slug = models.SlugField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        """slugifies name and saves"""
        self.slug = slugify(self.name)
        super(QtyChangeReason, self).save(*args, **kwargs)


class ProductQtyChange(models.Model):
    """model to track and account for qty changes"""

    slug = models.SlugField(max_length=255)
    product = models.ForeignKey(Product)
    old_qty = models.IntegerField()
    new_qty = models.IntegerField()
    reason = models.ForeignKey(QtyChangeReason)
    details = models.TextField(blank=True, null=True)
    who = models.ForeignKey(User)
    modified = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'[%d] %d to %d on %s because "%s" by %s' % (
            self.product.sku, self.old_qty, self.new_qty, self.modified.strftime('%Y-%m-%d %I:%M%p'),
            self.reason.name, self.who.username)

    def save(self, *args, **kwargs):
        """performs error checks, saves self, saves product"""
        self.old_qty = self.product.qty_on_hand
        self.product.qty_on_hand = self.new_qty
        super(ProductQtyChange, self).save(*args, **kwargs)
        self.slug = slugify(self.modified.strftime('%Y %m %d %H %M'))
        super(ProductQtyChange, self).save(*args, **kwargs)
        self.product.save()


class PriceChangeReason(models.Model):
    """model for price change control"""

    slug = models.SlugField(max_length=255, unique=True)
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        """slugifies name and saves"""
        self.slug = slugify(self.name)
        super(PriceChangeReason, self).save(*args, **kwargs)


class ProductPriceChange(models.Model):
    """model to track and account for price changes"""

    slug = models.SlugField(max_length=255)
    product = models.ForeignKey(Product)
    old_price = models.DecimalField(max_digits=10, decimal_places=2)
    new_price = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.ForeignKey(PriceChangeReason)
    details = models.TextField(blank=True, null=True)
    who = models.ForeignKey(User)
    modified = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'[%d] $%f to $%f on %s because "%s" by %s' % (
            self.product.sku, self.old_price, self.new_price, self.modified.strftime('%Y-%m-%d %I:%M%p'),
            self.reason.name, self.who.username)

    def save(self, *args, **kwargs):
        """performs error checks, saves self, saves product"""
        self.old_price = self.product.price
        self.product.price = self.new_price
        super(ProductPriceChange, self).save(*args, **kwargs)
        self.slug = slugify(self.modified.strftime('%Y %m %d %H %M'))
        super(ProductPriceChange, self).save(*args, **kwargs)
        self.product.save()


class CostChangeReason(models.Model):
    """model for cost change control"""

    slug = models.SlugField(max_length=255, unique=True)
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        """slugifies name and saves"""
        self.slug = slugify(self.name)
        super(CostChangeReason, self).save(*args, **kwargs)


class ProductCostChange(models.Model):
    """model to track and account for cost changes"""

    slug = models.SlugField(max_length=255)
    product = models.ForeignKey(Product)
    old_cost = models.DecimalField(max_digits=10, decimal_places=2)
    new_cost = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.ForeignKey(CostChangeReason)
    details = models.TextField(blank=True, null=True)
    who = models.ForeignKey(User)
    modified = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'[%d] $%f to $%f on %s because "%s" by %s' % (
            self.product.sku, self.old_cost, self.new_cost, self.modified.strftime('%Y-%m-%d %I:%M%p'),
            self.reason.name, self.who.username)

    def save(self, *args, **kwargs):
        """performs error checks, saves self, saves product"""
        self.old_cost = self.product.cost
        self.product.cost = self.new_cost
        super(ProductCostChange, self).save(*args, **kwargs)
        self.slug = slugify(self.modified.strftime('%Y %m %d %H %M'))
        super(ProductCostChange, self).save(*args, **kwargs)
        self.product.save()
