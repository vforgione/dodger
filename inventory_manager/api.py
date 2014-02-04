from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.resources import ModelResource
from tastypie.http import HttpConflict

from models import Category, Manufacturer, Attribute, Product, ProductAttribute, \
    ProductQtyChange, ProductCostChange, ProductPriceChange, QtyChangeReason, CostChangeReason, PriceChangeReason


class CategoryResource(ModelResource):
    """a resource for the Category model"""

    class Meta:
        # how to call resource
        resource_name = 'categories'
        queryset = Category.objects.all()
        # available methods - disallow patch
        list_allowed_methods = ('get', 'post', 'delete')
        detail_allowed_methods = ('get', 'delete')
        # field filters (querystring)
        filtering = {
            'id': ALL,
            'name': ALL,
        }
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
        # field filters (querystring)
        filtering = {
            'id': ALL,
            'name': ALL,
        }
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
        # field filters (querystring)
        filtering = {
            'id': ALL,
            'name': ALL,
        }
        # auth
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        # always return data
        always_return_data = True


class ProductResource(ModelResource):
    """a resource for the Product model"""

    # foreign keys
    categories = fields.ManyToManyField(CategoryResource, 'categories')
    supplier = fields.ForeignKey('dat.api.SupplierResource', 'supplier')
    manufacturer = fields.ForeignKey(ManufacturerResource, 'manufacturer')
    owner = fields.ForeignKey('dodger.api.UserResource', 'owner')
    description = fields.CharField(attribute='_description', readonly=True)

    class Meta:
        # how to call resource
        resource_name = 'products'
        queryset = Product.objects.all()
        # available methods
        list_allowed_methods = ('get', 'post', 'delete')
        detail_allowed_methods = ('get', 'patch', 'delete')
        # field filters (querystring)
        filtering = {
            'sku': ALL,
            'name': ALL,
            'categories': ALL_WITH_RELATIONS,
            'supplier': ALL_WITH_RELATIONS,
            'manufacturer': ALL_WITH_RELATIONS,
            'owner': ALL_WITH_RELATIONS,
            'reorder_threshold': ALL,
            'do_not_disturb': ALL,
            'price': ALL,
            'cost': ALL,
            'mfr_sku': ALL,
            'case_qty': ALL,
            'location': ALL,
            'qty_on_hand': ALL,
            'created': ALL,
            'modified': ALL,
        }
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
        # field filters (querystring)
        filtering = {
            'product': ALL_WITH_RELATIONS,
            'attribute': ALL_WITH_RELATIONS,
            'value': ALL,
        }
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


class QtyChangeReasonResource(ModelResource):
    """a resource for the QtyChangeReason model"""

    class Meta:
        # how to call
        resource_name = 'qty-change-reasons'
        queryset = QtyChangeReason.objects.all()
        # available methods - limit to get and post
        list_allowed_methods = ('get', 'post')
        detail_allowed_methods = ('get', )
        # field filters (querystring)
        filtering = {
            'id': ALL,
            'name': ALL,
        }
        # auth
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        # always return data
        always_return_data = True


class CostChangeReasonResource(ModelResource):
    """a resource for the QtyChangeReason model"""

    class Meta:
        # how to call
        resource_name = 'cost-change-reasons'
        queryset = CostChangeReason.objects.all()
        # available methods - limit to get and post
        list_allowed_methods = ('get', 'post')
        detail_allowed_methods = ('get', )
        # field filters (querystring)
        filtering = {
            'id': ALL,
            'name': ALL,
        }
        # auth
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        # always return data
        always_return_data = True


class PriceChangeReasonResource(ModelResource):
    """a resource for the QtyChangeReason model"""

    class Meta:
        # how to call
        resource_name = 'price-cahnge-reasons'
        queryset = PriceChangeReason.objects.all()
        # available methods - limit to get and post
        list_allowed_methods = ('get', 'post')
        detail_allowed_methods = ('get', )
        # field filters (querystring)
        filtering = {
            'id': ALL,
            'name': ALL,
        }
        # auth
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        # always return data
        always_return_data = True


class ProductQtyChangeResource(ModelResource):
    """a resource for the ProductQtyChange model"""

    # foreign keys
    product = fields.ForeignKey(ProductResource, 'product')
    reason = fields.ForeignKey(QtyChangeReasonResource, 'reason')
    who = fields.ForeignKey('dodger.api.UserResource', 'who')

    class Meta:
        # how to call
        resource_name = 'product-qty-changes'
        queryset = ProductQtyChange.objects.all()
        # available methods - limit to get and post
        list_allowed_methods = ('get', 'post')
        detail_allowed_methods = ('get', )
        # field filters (querystring)
        filtering = {
            'product': ALL_WITH_RELATIONS,
            'reason': ALL_WITH_RELATIONS,
            'who': ALL_WITH_RELATIONS,
            'old_qty': ALL,
            'new_qty': ALL,
            'modified': ALL,
            'details': ALL,
        }
        # auth
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        # always return data
        always_return_data = True


class ProductCostChangeResource(ModelResource):
    """a resource for the ProductQtyChange model"""

    # foreign keys
    product = fields.ForeignKey(ProductResource, 'product')
    reason = fields.ForeignKey(CostChangeReasonResource, 'reason')
    who = fields.ForeignKey('dodger.api.UserResource', 'who')

    class Meta:
        # how to call
        resource_name = 'product-cost-changes'
        queryset = ProductCostChange.objects.all()
        # available methods - limit to get and post
        list_allowed_methods = ('get', 'post')
        detail_allowed_methods = ('get', )
        # field filters (querystring)
        filtering = {
            'product': ALL_WITH_RELATIONS,
            'reason': ALL_WITH_RELATIONS,
            'who': ALL_WITH_RELATIONS,
            'old_cost': ALL,
            'new_cost': ALL,
            'modified': ALL,
            'details': ALL,
        }
        # auth
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        # always return data
        always_return_data = True


class ProductPriceChangeResource(ModelResource):
    """a resource for the ProductQtyChange model"""

    # foreign keys
    product = fields.ForeignKey(ProductResource, 'product')
    reason = fields.ForeignKey(PriceChangeReasonResource, 'reason')
    who = fields.ForeignKey('dodger.api.UserResource', 'who')

    class Meta:
        # how to call
        resource_name = 'product-price-changes'
        queryset = ProductPriceChange.objects.all()
        # available methods - limit to get and post
        list_allowed_methods = ('get', 'post')
        detail_allowed_methods = ('get', )
        # field filters (querystring)
        filtering = {
            'product': ALL_WITH_RELATIONS,
            'reason': ALL_WITH_RELATIONS,
            'who': ALL_WITH_RELATIONS,
            'old_price': ALL,
            'new_price': ALL,
            'modified': ALL,
            'details': ALL,
        }
        # auth
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        # always return data
        always_return_data = True
