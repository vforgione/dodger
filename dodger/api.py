from django.contrib.auth.models import User

from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource
from tastypie.http import HttpConflict, HttpBadRequest


from inventory_manager.models import Category, Manufacturer, Attribute, Product, ProductAttribute, \
    ProductQtyChange, ProductCostChange, ProductPriceChange

from dat.models import Supplier, ContactLabel, Contact, Receiver, PurchaseOrder, PurchaseOrderProduct

from warehouse.models import Shipment, ShipmentProduct


class UserResource(ModelResource):
    """a resource for Users"""

    class Meta:
        # how to call resource
        resource_name = 'users'
        queryset = User.objects.all()
        # limit fields
        excludes = ('email', 'password', 'is_superuser')
        # available methods - limit to get, all other work should be done in admin
        list_allowed_methods = ('get', )
        detail_allowed_methods = ('get', )
        # auth
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        # always return data
        always_return_data = True


class CategoryResource(ModelResource):
    """a resource for the Category model"""

    class Meta:
        # how to call resource
        resource_name = 'categories'
        queryset = Category.objects.all()
        # available methods - disallow patch
        list_allowed_methods = ('get', 'post', 'delete')
        detail_allowed_methods = ('get', 'delete')
        # auth
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        # always return data
        always_return_data = True


class ManufacturerResource(ModelResource):
    """a resource for the Manufacturer model"""

    class Meta:
        # how to call resource
        resource_name = 'manufacturers'
        queryset = Manufacturer.objects.all()
        # available methods - disallow patch
        list_allowed_methods = ('get', 'post', 'delete')
        detail_allowed_methods = ('get', 'delete')
        # auth
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        # always return data
        always_return_data = True


class AttributeResource(ModelResource):
    """a resource for the Attribute model"""

    class Meta:
        # how to call resource
        resource_name = 'attributes'
        queryset = Attribute.objects.all()
        # available methods - disallow patch
        list_allowed_methods = ('get', 'post', 'delete')
        detail_allowed_methods = ('get', 'delete')
        # auth
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        # always return data
        always_return_data = True


class SupplierResource(ModelResource):
    """a resource for the Supplier model"""

    class Meta:
        # how to call
        resource_name = 'suppliers'
        queryset = Supplier.objects.all()
        # available methods
        list_allowed_methods = ('get', 'post', 'delete')
        detail_allowed_methods = ('get', 'patch', 'delete')
        # auth
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        # always return data
        always_return_data = True

    def patch_detail(self, request, **kwargs):
        body = self.deserialize(request, request.body)
        if 'name' in body or 'id' in body:
            return HttpBadRequest(
                "`id` and `name` not allowed as keys - they will create a new object. "
                "use POST instead, it's more explicit.")
        else:
            return super(SupplierResource, self).patch_detail(request, **kwargs)


class ContactLabelResource(ModelResource):
    """a resource for the SupplierLabel model"""

    class Meta:
        # how to call
        resource_name = 'contact-labels'
        queryset = ContactLabel.objects.all()
        # available methods - disallow patch
        list_allowed_methods = ('get', 'post', 'delete')
        detail_allowed_methods = ('get', 'delete')
        # auth
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        # always return data
        always_return_data = True


class ContactResource(ModelResource):
    """a resource for the Contact model"""

    # foreign keys
    label = fields.ForeignKey(ContactLabelResource, 'label')
    represents = fields.ForeignKey(SupplierResource, 'represents')

    class Meta:
        # how to call
        resource_name = 'contacts'
        queryset = Contact.objects.all()
        # available methods
        list_allowed_methods = ('get', 'post', 'delete')
        detail_allowed_methods = ('get', 'patch', 'delete')
        # auth
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        # always return data
        always_return_data = True

    def patch_detail(self, request, **kwargs):
        body = self.deserialize(request, request.body)
        if 'name' in body or 'id' in body:
            return HttpBadRequest(
                "`id` is allowed as a key - it will create a new object. "
                "use POST instead, it's more explicit.")
        else:
            return super(ContactResource, self).patch_detail(request, **kwargs)


class ReceiverResource(ModelResource):
    """a resource for the Receiver model"""

    class Meta:
        # how to call
        resource_name = 'receivers'
        queryset = Receiver.objects.all()
        # available methods
        list_allowed_methods = ('get', 'post', 'delete')
        detail_allowed_methods = ('get', 'patch', 'delete')
        # auth
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        # always return data
        always_return_data = True

    def patch_detail(self, request, **kwargs):
        body = self.deserialize(request, request.body)
        if 'name' in body or 'id' in body:
            return HttpBadRequest(
                "`id` is allowed as a key - it will create a new object. "
                "use POST instead, it's more explicit.")
        else:
            return super(ReceiverResource, self).patch_detail(request, **kwargs)


class ProductResource(ModelResource):
    """a resource for the Product model"""

    # foreign keys
    categories = fields.ManyToManyField(CategoryResource, 'categories')
    supplier = fields.ForeignKey(SupplierResource, 'supplier')
    manufacturer = fields.ForeignKey(ManufacturerResource, 'manufacturer')
    owner = fields.ForeignKey(UserResource, 'owner')

    class Meta:
        # how to call resource
        resource_name = 'products'
        queryset = Product.objects.all()
        # available methods
        list_allowed_methods = ('get', 'post', 'delete')
        detail_allowed_methods = ('get', 'patch', 'delete')
        # auth
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        # always return data
        always_return_data = True


class ProductAttributeResource(ModelResource):
    """a resource for the ProductAdditionalAttribute model"""

    # foreign keys
    product = fields.ForeignKey(ProductResource, 'product')
    attribute = fields.ForeignKey(AttributeResource, 'attribute')

    class Meta:
        # how to call resource
        resource_name = 'product-attributes'
        queryset = ProductAttribute.objects.all()
        # available methods - disallow patch
        list_allowed_methods = ('get', 'post', 'delete')
        detail_allowed_methods = ('get', 'delete')
        # auth
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        # always return data
        always_return_data = True

    def post_list(self, request, **kwargs):
        body = self.deserialize(request, request.body)
        product = body['product'].split('/')[-2]
        attribute = body['attribute'].split('/')[-2]
        try:
            _ = ProductAttribute.objects.filter(product=product, attribute=attribute)[0]
            return HttpConflict("attribute already exists for this product")
        except (ProductAttribute.DoesNotExist, IndexError):
            super(ProductAttributeResource, self).post_list(request, **kwargs)


class ProductQtyChangeResource(ModelResource):
    """a resource for the ProductQtyChange model"""

    # foreign keys
    product = fields.ForeignKey(ProductResource, 'product')
    who = fields.ForeignKey(UserResource, 'who')

    class Meta:
        # how to call
        resource_name = 'product-qty-changes'
        queryset = ProductQtyChange.objects.all()
        # available methods - limit to get and post
        list_allowed_methods = ('get', 'post')
        detail_allowed_methods = ('get', )
        # auth
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        # always return data
        always_return_data = True


class ProductCostChangeResource(ModelResource):
    """a resource for the ProductQtyChange model"""

    # foreign keys
    product = fields.ForeignKey(ProductResource, 'product')
    who = fields.ForeignKey(UserResource, 'who')

    class Meta:
        # how to call
        resource_name = 'product-cost-changes'
        queryset = ProductCostChange.objects.all()
        # available methods - limit to get and post
        list_allowed_methods = ('get', 'post')
        detail_allowed_methods = ('get', )
        # auth
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        # always return data
        always_return_data = True


class ProductPriceChangeResource(ModelResource):
    """a resource for the ProductQtyChange model"""

    # foreign keys
    product = fields.ForeignKey(ProductResource, 'product')
    who = fields.ForeignKey(UserResource, 'who')

    class Meta:
        # how to call
        resource_name = 'product-price-changes'
        queryset = ProductPriceChange.objects.all()
        # available methods - limit to get and post
        list_allowed_methods = ('get', 'post')
        detail_allowed_methods = ('get', )
        # auth
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        # always return data
        always_return_data = True


class PurchaseOrderResource(ModelResource):
    """a resource for the PurchaseOrder model"""

    # foreign keys
    supplier = fields.ForeignKey(SupplierResource, 'supplier')
    contact = fields.ForeignKey(ContactResource, 'contact')
    ship_to = fields.ForeignKey(ReceiverResource, 'ship_to')
    dat_member = fields.ForeignKey(UserResource, 'dat_member')

    class Meta:
        # how to call
        resource_name = 'purchase-orders'
        queryset = PurchaseOrder.objects.all()
        # available methods
        list_allowed_methods = ('get', 'post', 'delete')
        detail_allowed_methods = ('get', 'patch', 'delete')
        # auth
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        # always return data
        always_return_data = True

    def patch_detail(self, request, **kwargs):
        body = self.deserialize(request, request.body)
        if 'name' in body or 'id' in body:
            return HttpBadRequest(
                "`id` is allowed as a key - it will create a new object. "
                "use POST instead, it's more explicit.")
        else:
            return super(PurchaseOrderResource, self).patch_detail(request, **kwargs)


class PurchaseOrderProductResource(ModelResource):
    """a resource for the PurchaseOrderProduct model"""

    # foreign keys
    purchase_order = fields.ForeignKey(PurchaseOrderResource, 'purchase_order')
    product = fields.ForeignKey(ProductResource, 'product')

    class Meta:
        # how to call
        resource_name = 'purchase-order-products'
        queryset = PurchaseOrderProduct.objects.all()
        # available methods - limit to get and post
        list_allowed_methods = ('get', 'post')
        detail_allowed_methods = ('get', )
        # auth
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        # always return data
        always_return_data = True


class ShipmentResource(ModelResource):
    """a resource for the Shipment model"""

    # foreign keys
    purchase_order = fields.ForeignKey(PurchaseOrderResource, 'purchase_order')
    received_by = fields.ForeignKey(UserResource, 'received_by')

    class Meta:
        # how to call
        resource_name = 'shipments'
        queryset = Shipment.objects.all()
        # available methods - limit to get and post
        list_allowed_methods = ('get', 'post')
        detail_allowed_methods = ('get', )
        # auth
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        # always return data
        always_return_data = True


class ShipmentProductResource(ModelResource):
    """a resource for the ShipmentProduct model"""

    # foreign keys
    shipment = fields.ForeignKey(ShipmentResource, 'shipment')
    product = fields.ForeignKey(PurchaseOrderProductResource, 'product')

    class Meta:
        # how to call
        resource_name = 'shipment-products'
        queryset = ShipmentProduct.objects.all()
        # available methods - limit to get and post
        list_allowed_methods = ('get', 'post')
        detail_allowed_methods = ('get', )
        # auth
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        # always return data
        always_return_data = True
