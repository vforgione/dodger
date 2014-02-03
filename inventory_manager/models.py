from datetime import datetime, timedelta
import pytz

from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify


class Category(models.Model):

    id = models.SlugField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class Manufacturer(models.Model):

    id = models.SlugField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = slugify(self.name)
        super(Manufacturer, self).save(*args, **kwargs)


class Attribute(models.Model):

    id = models.SlugField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = slugify(self.name)
        super(Attribute, self).save(*args, **kwargs)


class Reason(models.Model):

    id = models.SlugField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = 'Product change reason'

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = slugify(self.name)
        super(Reason, self).save(*args, **kwargs)


class Product(models.Model):

    # id
    sku = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    # classification
    categories = models.ManyToManyField(Category)
    supplier = models.ForeignKey('dat.Supplier')
    manufacturer = models.ForeignKey(Manufacturer)
    # responsibility
    owner = models.ForeignKey(User)
    reorder_threshold = models.IntegerField()
    do_not_disturb = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    mfr_sku = models.CharField(max_length=255)
    case_qty = models.CharField(max_length=255)
    # required attributes
    location = models.CharField(max_length=255)
    qty_on_hand = models.IntegerField()
    # time stamps
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        attributes = self.get_attributes()
        if len(attributes):
            return u'[{}] {} : {}'.format(self.sku, self.name, u', '.join(attributes))
        return u'[{}] {}'.format(self.sku, self.name)

    def _description(self):
        return self.__unicode__()

    description = property(_description)

    def save(self, *args, **kwargs):
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
        attributes = []
        qs = ProductAttribute.objects.all().filter(product=self.sku)
        for row in qs:
            if row.attribute.name.lower().endswith('bulk'):
                attributes.append('Bulk')
            else:
                attributes.append(row.value)
        return attributes


class ProductAttribute(models.Model):

    product = models.ForeignKey(Product)
    attribute = models.ForeignKey(Attribute)
    value = models.CharField(max_length=255)

    def __unicode__(self):
        return u'{}@{} : {}'.format(self.product.name, self.attribute.name, self.value)


class ProductQtyChange(models.Model):

    product = models.ForeignKey(Product)
    old_qty = models.IntegerField()
    new_qty = models.IntegerField()
    reason = models.ForeignKey(Reason)
    who = models.ForeignKey(User)
    modified = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'[{}] {} to {} on {} because "{}" by {}'.format(
            self.product.sku, self.old_qty, self.new_qty, self.modified.strftime('%Y-%m-%d %I:%M%p'), self.reason.name,
            self.who.get_full_name()
        )

    def save(self, *args, **kwargs):
        self.old_qty = self.product.qty_on_hand
        self.product.qty_on_hand = self.new_qty
        super(ProductQtyChange, self).save(*args, **kwargs)
        self.product.save()


class ProductPriceChange(models.Model):

    product = models.ForeignKey(Product)
    old_price = models.DecimalField(max_digits=10, decimal_places=2)
    new_price = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.ForeignKey(Reason)
    who = models.ForeignKey(User)
    modified = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'[{}] ${} to ${} on {} because "{}" by {}'.format(
            self.product.sku, self.old_price, self.new_price, self.modified.strftime('%Y-%m-%d %I:%M%p'),
            self.reason.name, self.who.get_full_name()
        )

    def save(self, *args, **kwargs):
        self.old_price = self.product.price
        self.product.price = self.new_price
        super(ProductPriceChange, self).save(*args, **kwargs)
        self.product.save()


class ProductCostChange(models.Model):

    product = models.ForeignKey(Product)
    old_cost = models.DecimalField(max_digits=10, decimal_places=2)
    new_cost = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.ForeignKey(Reason)
    who = models.ForeignKey(User)
    modified = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'[{}] ${} to ${} on {} because "{}" by {}'.format(
            self.product.sku, self.old_cost, self.new_cost, self.modified.strftime('%Y-%m-%d %I:%M%p'),
            self.reason.name, self.who.get_full_name()
        )

    def save(self, *args, **kwargs):
        self.old_cost = self.product.cost
        self.product.cost = self.new_cost
        super(ProductCostChange, self).save(*args, **kwargs)
        self.product.save()
