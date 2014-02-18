from django.contrib.auth.models import User
from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.resources import ModelResource

from .models import *


class UserResource(ModelResource):

    class Meta:
        # name
        resource_name = 'users'
        queryset = User.objects.all()
        # auth
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        # data
        filtering = {
            'id': ALL,
            'username': ALL,
        }
        always_return_data = True


class SupplierResource(ModelResource):

    class Meta:
        # name
        resource_name = 'suppliers'
        queryset = Supplier.objects.all()
        # auth
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        # data
        filtering = {
            'id': ALL,
            'name': ALL,
        }
        always_return_data = True


class CategoryResource(ModelResource):

    class Meta:
        # name
        resource_name = 'categories'
        queryset = Category.objects.all()
        # auth
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        # data
        filtering = {
            'id': ALL,
            'name': ALL,
        }
        always_return_data = True


class BrandResource(ModelResource):

    class Meta:
        # name
        resource_name = 'brands'
        queryset = Brand.objects.all()
        # auth
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        # data
        filtering = {
            'id': ALL,
            'name': ALL,
        }
        always_return_data = True


class AttributeResource(ModelResource):

    class Meta:
        # name
        resource_name = 'attributes'
        queryset = Attribute.objects.all()
        # auth
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        # data
        filtering = {
            'id': ALL,
            'name': ALL,
        }
        always_return_data = True


class SkuResource(ModelResource):

    # foreign keys
    categories = fields.ManyToManyField(CategoryResource, 'categories')
    supplier = fields.ForeignKey(SupplierResource, 'supplier')
    brand = fields.ForeignKey(BrandResource, 'brand')
    owner = fields.ForeignKey(UserResource, 'owner')
    description = fields.CharField(attribute='_description', readonly=True)

    class Meta:
        # name
        resource_name = 'skus'
        queryset = Sku.objects.all()
        # auth
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        # data
        filtering = {
            'id': ALL,
            'name': ALL,
            'categories': ALL_WITH_RELATIONS,
            'supplier': ALL_WITH_RELATIONS,
            'brand': ALL_WITH_RELATIONS,
            'owner': ALL_WITH_RELATIONS,
            'reorder_threshold': ALL,
            'notify_at_threshold': ALL,
            'cost': ALL,
            'mfr_sku': ALL,
            'case_qty': ALL,
            'location': ALL,
            'qty_on_hand': ALL,
            'created': ALL,
            'modified': ALL,
        }
        always_return_data = True


class SkuAttributeResource(ModelResource):

    # foreign keys
    sku = fields.ForeignKey(SkuResource, 'sku')
    attribute = fields.ForeignKey(AttributeResource, 'attribute')

    class Meta:
        # name
        resource_name = 'sku-attributes'
        queryset = SkuAttribute.objects.all()
        # auth
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        # data
        filtering = {
            'id': ALL,
            'value': ALL,
            'sku': ALL_WITH_RELATIONS,
            'attribute': ALL_WITH_RELATIONS,
        }
        always_return_data = True


class QuantityAdjustmentReasonResource(ModelResource):

    class Meta:
        # name
        resource_name = 'sku-quantity-change-reasons'
        queryset = QuantityAdjustmentReason.objects.all()
        # auth
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        # data
        filtering = {
            'id': ALL,
            'name': ALL,
        }
        always_return_data = True


class SkuQuantityAdjustmentResource(ModelResource):

    # foreign keys
    sku = fields.ForeignKey(SkuResource, 'sku')
    who = fields.ForeignKey(UserResource, 'who')
    reason = fields.ForeignKey(QuantityAdjustmentReasonResource, 'reason')

    class Meta:
        # name
        resource_name = 'sku-quantity-change-traces'
        queryset = SkuQuantityAdjustment.objects.all()
        # auth
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        # data
        filtering = {
            'id': ALL,
            'sku': ALL_WITH_RELATIONS,
            'old': ALL,
            'new': ALL,
            'who': ALL_WITH_RELATIONS,
            'reason': ALL_WITH_RELATIONS,
            'detail': ALL,
            'when': ALL,
        }
        always_return_data = True


class ContactLabelResource(ModelResource):

    class Meta:
        # name
        resource_name = 'contact-labels'
        queryset = ContactLabel.objects.all()
        # auth
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        # data
        filtering = {
            'id': ALL,
            'name': ALL,
        }
        always_return_data = True


class ContactResource(ModelResource):

    # foreign keys
    represents = fields.ForeignKey(SupplierResource, 'represents')
    label = fields.ForeignKey(ContactLabelResource, 'label')

    class Meta:
        # name
        resource_name = 'contacts'
        queryset = Contact.objects.all()
        # auth
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        # data
        filtering = {
            'id': ALL,
            'name': ALL,
            'email': ALL,
            'phone': ALL,
            'fax': ALL,
            'address1': ALL,
            'address2': ALL,
            'address3': ALL,
            'city': ALL,
            'state': ALL,
            'zipcode': ALL,
            'country': ALL,
            'represents': ALL_WITH_RELATIONS,
            'label': ALL_WITH_RELATIONS,
        }
        always_return_data = True


class ReceiverResource(ModelResource):

    class Meta:
        # name
        resource_name = 'receivers'
        queryset = Receiver.objects.all()
        # auth
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        # data
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
        always_return_data = True


class PurchaseOrderResource(ModelResource):

    # foreign keys
    supplier = fields.ForeignKey(SupplierResource, 'supplier')
    contact = fields.ForeignKey(ContactResource, 'contact')
    receiver = fields.ForeignKey(ReceiverResource, 'receiver')
    creator = fields.ForeignKey(UserResource, 'creator')

    class Meta:
        # name
        resource_name = 'purchase-orders'
        queryset = PurchaseOrder.objects.all()
        # auth
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        # data
        filtering = {
            'id': ALL,
            'supplier': ALL_WITH_RELATIONS,
            'contact': ALL_WITH_RELATIONS,
            'receiver': ALL_WITH_RELATIONS,
            'creator': ALL_WITH_RELATIONS,
            'comments': ALL,
            'created': ALL,
        }
        always_return_data = True


class PurchaseOrderLineItemResource(ModelResource):

    # foreign keys
    purchase_order = fields.ForeignKey(PurchaseOrderResource, 'purchase_order')
    sku = fields.ForeignKey(SkuResource, 'sku')

    class Meta:
        # name
        resource_name = 'purchase-order-line-items'
        queryset = PurchaseOrderLineItem.objects.all()
        # auth
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        # data
        filtering = {
            'id': ALL,
            'purchase_order': ALL_WITH_RELATIONS,
            'sku': ALL_WITH_RELATIONS,
            'disc_dollar': ALL,
            'disc_percent': ALL,
            'qty_ordered': ALL,
            'unit_cost': ALL,
        }
        always_return_data = True


class ShipmentResource(ModelResource):

    # foreign keys
    purchase_order = fields.ForeignKey(PurchaseOrderResource, 'purchase_order')
    received_by = fields.ForeignKey(UserResource, 'received_by')

    class Meta:
        # name
        resource_name = 'shipments'
        queryset = Shipment.objects.all()
        # auth
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        # data
        filtering = {
            'id': ALL,
            'purchase_order': ALL_WITH_RELATIONS,
            'received_by': ALL_WITH_RELATIONS,
            'received_on': ALL,
            'comments': ALL,
            'status': ALL,
        }
        always_return_data = True


class ShipmentLineItemResource(ModelResource):

    # foreign keys
    shipment = fields.ForeignKey(ShipmentResource, 'shipment')
    sku = fields.ForeignKey(SkuResource, 'sku')

    class Meta:
        # name
        resource_name = 'shipment-line-items'
        queryset = ShipmentLineItem.objects.all()
        # auth
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        # data
        filtering = {
            'id': ALL,
            'shipment': ALL_WITH_RELATIONS,
            'sku': ALL_WITH_RELATIONS,
            'qty_received': ALL,
        }
        always_return_data = True


from django.conf.urls import patterns, include, url
from tastypie.api import Api

auth_api = Api(api_name='auth')
auth_api.register(UserResource())

app_api = Api(api_name='sku-service')
app_api.register(SupplierResource())
app_api.register(CategoryResource())
app_api.register(BrandResource())
app_api.register(AttributeResource())
app_api.register(SkuResource())
app_api.register(SkuAttributeResource())
app_api.register(QuantityAdjustmentReasonResource())
app_api.register(SkuQuantityAdjustmentResource())
app_api.register(ContactLabelResource())
app_api.register(ContactResource())
app_api.register(ReceiverResource())
app_api.register(PurchaseOrderResource())
app_api.register(PurchaseOrderLineItemResource())
app_api.register(ShipmentResource())
app_api.register(ShipmentLineItemResource())


urlpatterns = patterns(
    '',

    # api
    url(r'^', include(auth_api.urls + app_api.urls)),
)
