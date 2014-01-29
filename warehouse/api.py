from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.resources import ModelResource

from models import Shipment, ShipmentProduct


class ShipmentResource(ModelResource):
    """a resource for the Shipment model"""

    # foreign keys
    purchase_order = fields.ForeignKey('dat.api.PurchaseOrderResource', 'purchase_order')
    received_by = fields.ForeignKey('dodger.api.UserResource', 'received_by')

    class Meta:
        # how to call
        resource_name = 'shipments'
        queryset = Shipment.objects.all()
        # available methods - limit to get and post
        list_allowed_methods = ('get', 'post')
        detail_allowed_methods = ('get', )
        # field filters (querystring)
        filtering = {
            'purchase_order': ALL_WITH_RELATIONS,
            'received_by': ALL_WITH_RELATIONS,
            'received_on': ALL,
        }
        # auth
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        # always return data
        always_return_data = True


class ShipmentProductResource(ModelResource):
    """a resource for the ShipmentProduct model"""

    # foreign keys
    shipment = fields.ForeignKey(ShipmentResource, 'shipment')
    product = fields.ForeignKey('dat.api.PurchaseOrderProductResource', 'product')

    class Meta:
        # how to call
        resource_name = 'shipment-products'
        queryset = ShipmentProduct.objects.all()
        # available methods - limit to get and post
        list_allowed_methods = ('get', 'post')
        detail_allowed_methods = ('get', )
        # field filters (querystring)
        filtering = {
            'shipment': ALL_WITH_RELATIONS,
            'product': ALL_WITH_RELATIONS,
            'qty_received': ALL,
        }
        # auth
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        # always return data
        always_return_data = True
