from django.contrib.auth.models import User
from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.resources import ModelResource

from models import *


class UserResource(ModelResource):

    class Meta:
        resource_name = 'users'
        queryset = User.objects.all()
        filtering = {
            'id': ALL,
            'username': ALL,
        }
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ['get', ]
        always_return_data = True


class AttributeResource(ModelResource):

    class Meta:
        resource_name = 'attributes'
        queryset = Attribute.objects.all()
        filtering = {
            'id': ALL,
            'name': ALL,
        }
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ['get', ]
        always_return_data = True


class BrandResource(ModelResource):

    class Meta:
        resource_name = 'brands'
        queryset = Brand.objects.all()
        filtering = {
            'id': ALL,
            'name': ALL,
        }
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ['get', ]
        always_return_data = True


class CategoryResource(ModelResource):

    class Meta:
        resource_name = 'categories'
        queryset = Category.objects.all()
        filtering = {
            'id': ALL,
            'name': ALL,
        }
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ['get', ]
        always_return_data = True


class ContactLabelResource(ModelResource):

    class Meta:
        resource_name = 'contact_labels'
        queryset = ContactLabel.objects.all()
        filtering = {
            'id': ALL,
            'name': ALL,
        }
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ['get', ]
        always_return_data = True


class CostAdjustmentReasonResource(ModelResource):

    class Meta:
        resource_name = 'cost_adjustment_reasons'
        queryset = CostAdjustmentReason.objects.all()
        filtering = {
            'id': ALL,
            'name': ALL,
        }
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ['get', ]
        always_return_data = True


class QuantityAdjustmentReasonResource(ModelResource):

    class Meta:
        resource_name = 'quantity_adjustment_reasons'
        queryset = QuantityAdjustmentReason.objects.all()
        filtering = {
            'id': ALL,
            'name': ALL,
        }
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ['get', ]
        always_return_data = True


class SupplierResource(ModelResource):

    class Meta:
        resource_name = 'suppliers'
        queryset = Supplier.objects.all()
        filtering = {
            'id': ALL,
            'name': ALL,
        }
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ['get', ]
        always_return_data = True


class ContactResource(ModelResource):

    represents = fields.ForeignKey(SupplierResource, 'represents')
    label = fields.ForeignKey(ContactLabelResource, 'label')

    class Meta:
        resource_name = 'contacts'
        queryset = Contact.objects.all()
        filtering = {
            'id': ALL,
            'name': ALL,
            'address1': ALL,
            'address2': ALL,
            'address3': ALL,
            'city': ALL,
            'state': ALL,
            'zipcode': ALL,
            'country': ALL,
            'email': ALL,
            'phone': ALL,
            'fax': ALL,
            'represents': ALL_WITH_RELATIONS,
            'label': ALL_WITH_RELATIONS,
        }
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ['get', ]
        always_return_data = True


class ReceiverResource(ModelResource):

    class Meta:
        resource_name = 'receivers'
        queryset = Receiver.objects.all()
        filtering = {
            'id': ALL,
            'name': ALL,
            'address1': ALL,
            'address2': ALL,
            'address3': ALL,
            'city': ALL,
            'state': ALL,
            'zipcode': ALL,
            'country': ALL,
        }
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ['get', ]
        always_return_data = True


class SkuResource(ModelResource):

    brand = fields.ForeignKey(BrandResource, 'brand')
    categories = fields.ManyToManyField(CategoryResource, 'categories')
    owner = fields.ForeignKey(UserResource, 'owner')
    supplier = fields.ForeignKey(SupplierResource, 'supplier')
    description = fields.CharField(attribute='_description', readonly=True)

    class Meta:
        resource_name = 'skus'
        queryset = Sku.objects.all()
        filtering = {
            'id': ALL,
            'name': ALL,
            'upc': ALL,
            'brand': ALL_WITH_RELATIONS,
            'categories': ALL_WITH_RELATIONS,
            'quantity_on_hand': ALL,
            'location': ALL,
            'owner': ALL_WITH_RELATIONS,
            'supplier': ALL_WITH_RELATIONS,
            'lead_time': ALL,
            'minimum_quantity': ALL,
            'notify_at_threshold': ALL,
            'cost': ALL,
            'supplier_sku': ALL,
            'in_live_deal': ALL,
            'is_subscription': ALL,
            'created': ALL,
            'modified': ALL,
        }
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ['get', ]
        always_return_data = True


class SkuAttributeResource(ModelResource):

    sku = fields.ForeignKey(SkuResource, 'sku')
    attribute = fields.ForeignKey(AttributeResource, 'attribute')

    class Meta:
        resource_name = 'sku_attributes'
        queryset = SkuAttribute.objects.all()
        filtering = {
            'id': ALL,
            'sku': ALL_WITH_RELATIONS,
            'attribute': ALL_WITH_RELATIONS,
            'value': ALL,
        }
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ['get', ]
        always_return_data = True


class PurchaseOrderResource(ModelResource):

    creator = fields.ForeignKey(UserResource, 'creator')
    supplier = fields.ForeignKey(SupplierResource, 'supplier')
    contact = fields.ForeignKey(ContactResource, 'contact')
    receiver = fields.ForeignKey(ReceiverResource, 'receiver')
    total_cost = fields.CharField(attribute='_total_cost', readonly=True)

    class Meta:
        resource_name = 'purchase_orders'
        queryset = PurchaseOrder.objects.all()
        filtering = {
            'id': ALL,
            'creator': ALL_WITH_RELATIONS,
            'supplier': ALL_WITH_RELATIONS,
            'contact': ALL_WITH_RELATIONS,
            'receiver': ALL_WITH_RELATIONS,
            'note': ALL,
            'created': ALL,
            'terms': ALL,
            'total_cost': ALL,
        }
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ['get', ]
        always_return_data = True


class PurchaseOrderLineItemResource(ModelResource):

    purchase_order = fields.ForeignKey(PurchaseOrderResource, 'purchase_order')
    sku = fields.ForeignKey(SkuResource, 'sku')
    adjustted_unit_cost = fields.CharField(attribute='_adjusted_unit_cost', readonly=True)
    total_cost = fields.CharField(attribute='_total_cost', readonly=True)

    class Meta:
        resource_name = 'purchase_order_line_items'
        queryset = PurchaseOrderLineItem.objects.all()
        filtering = {
            'id': ALL,
            'purchase_order': ALL_WITH_RELATIONS,
            'sku': ALL_WITH_RELATIONS,
            'quantity_received': ALL,
            'unit_cost': ALL,
            'discount_percent': ALL,
            'discount_dollar': ALL,
            'adjusted_unit_cost': ALL,
            'total_cost': ALL,
        }
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ['get', ]
        always_return_data = True


class ShipmentResource(ModelResource):

    creator = fields.ForeignKey(UserResource, 'creator')
    purchase_order = fields.ForeignKey(PurchaseOrderResource, 'purchase_order')

    class Meta:
        resource_name = 'shipments'
        queryset = Shipment.objects.all()
        filtering = {
            'id': ALL,
            'creator': ALL_WITH_RELATIONS,
            'purchase_order': ALL_WITH_RELATIONS,
            'note': ALL,
            'created': ALL,
        }
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ['get', ]
        always_return_data = True


class ShipmentLineItemResource(ModelResource):

    shipment = fields.ForeignKey(ShipmentResource, 'shipment')
    sku = fields.ForeignKey(SkuResource, 'sku')

    class Meta:
        resource_name = 'shipment_line_items'
        queryset = ShipmentLineItem.objects.all()
        filtering = {
            'id': ALL,
            'shipment': ALL_WITH_RELATIONS,
            'sku': ALL_WITH_RELATIONS,
            'quantity_received': ALL,
        }
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ['get', ]
        always_return_data = True


class CostAdjustmentResource(ModelResource):

    sku = fields.ForeignKey(SkuResource, 'sku')
    who = fields.ForeignKey(UserResource, 'who')
    reason = fields.ForeignKey(CostAdjustmentReasonResource, 'reason')

    class Meta:
        resource_name = 'cost_adjustments'
        queryset = CostAdjustment.objects.all()
        filtering = {
            'id': ALL,
            'sku': ALL_WITH_RELATIONS,
            'old': ALL,
            'new': ALL,
            'who': ALL_WITH_RELATIONS,
            'reason': ALL_WITH_RELATIONS,
            'detail': ALL,
            'created': ALL,
        }
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ['get', ]
        always_return_data = True


class QuantityAdjustmentResource(ModelResource):

    sku = fields.ForeignKey(SkuResource, 'sku')
    who = fields.ForeignKey(UserResource, 'who')
    reason = fields.ForeignKey(QuantityAdjustmentReasonResource, 'reason')

    class Meta:
        resource_name = 'quantity_adjustments'
        queryset = QuantityAdjustment.objects.all()
        filtering = {
            'id': ALL,
            'sku': ALL_WITH_RELATIONS,
            'old': ALL,
            'new': ALL,
            'who': ALL_WITH_RELATIONS,
            'reason': ALL_WITH_RELATIONS,
            'detail': ALL,
            'created': ALL,
        }
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ['get', ]
        always_return_data = True


# url conf
from django.conf.urls import include, patterns, url
from tastypie.api import Api
from api import *

auth_api = Api(api_name='auth')
auth_api.register(UserResource())

app_api = Api(api_name='sku_service')
app_api.register(AttributeResource())
app_api.register(BrandResource())
app_api.register(CategoryResource())
app_api.register(ContactLabelResource())
app_api.register(CostAdjustmentReasonResource())
app_api.register(QuantityAdjustmentReasonResource())
app_api.register(SupplierResource())
app_api.register(CostAdjustmentResource())
app_api.register(QuantityAdjustmentResource())
app_api.register(ContactResource())
app_api.register(ReceiverResource())
app_api.register(SkuResource())
app_api.register(SkuAttributeResource())
app_api.register(PurchaseOrderResource())
app_api.register(PurchaseOrderLineItemResource())
app_api.register(ShipmentResource())
app_api.register(ShipmentLineItemResource())

urlpatterns = patterns(
    '',
    url(r'^', include(auth_api.urls + app_api.urls)),
)
