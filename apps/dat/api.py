from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.resources import ModelResource
from tastypie.http import HttpBadRequest

from models import Supplier, ContactLabel, Contact, Receiver, PurchaseOrder, PurchaseOrderProduct


class SupplierResource(ModelResource):
    """a resource for the Supplier model"""

    class Meta:
        # how to call
        resource_name = 'suppliers'
        queryset = Supplier.objects.all()
        # available methods
        list_allowed_methods = ('get', 'post', 'delete')
        detail_allowed_methods = ('get', 'patch', 'delete')
        # field filters (querystring)
        filtering = {
            'id': ALL,
            'name': ALL,
            'ships_products': ALL,
            'terms': ALL,
        }
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
        # field filters (querystring)
        filtering = {
            'name': ALL,
            'email': ALL,
            'phone': ALL,
            'fax': ALL,
            'address0': ALL,
            'address1': ALL,
            'city': ALL,
            'state': ALL,
            'zipcode': ALL,
            'country': ALL,
            'label': ALL_WITH_RELATIONS,
            'represents': ALL_WITH_RELATIONS,
        }
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
        # field filters (querystring)
        filtering = {
            'name': ALL,
            'email': ALL,
            'phone': ALL,
            'fax': ALL,
            'address0': ALL,
            'address1': ALL,
            'city': ALL,
            'state': ALL,
            'zipcode': ALL,
            'country': ALL,
        }
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


class PurchaseOrderResource(ModelResource):
    """a resource for the PurchaseOrder model"""

    # foreign keys
    supplier = fields.ForeignKey(SupplierResource, 'supplier')
    contact = fields.ForeignKey(ContactResource, 'contact')
    ship_to = fields.ForeignKey(ReceiverResource, 'ship_to')
    dat_member = fields.ForeignKey('dodger.api.UserResource', 'creator')

    class Meta:
        # how to call
        resource_name = 'purchase-orders'
        queryset = PurchaseOrder.objects.all()
        # available methods
        list_allowed_methods = ('get', 'post', 'delete')
        detail_allowed_methods = ('get', 'patch', 'delete')
        # field filters (querystring)
        filtering = {
            'supplier': ALL_WITH_RELATIONS,
            'contact': ALL_WITH_RELATIONS,
            'ship_to': ALL_WITH_RELATIONS,
            'creator': ALL_WITH_RELATIONS,
            'comments': ALL,
            'created': ALL,
            'name': ALL,
            'id': ALL,
        }
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
    product = fields.ForeignKey('apps.inventory_manager.api.ProductResource', 'product')

    class Meta:
        # how to call
        resource_name = 'purchase-order-products'
        queryset = PurchaseOrderProduct.objects.all()
        # available methods - limit to get and post
        list_allowed_methods = ('get', 'post')
        detail_allowed_methods = ('get', )
        # field filters (querystring)
        filtering = {
            'purchase_order': ALL_WITH_RELATIONS,
            'product': ALL_WITH_RELATIONS,
            'disc_dollar': ALL,
            'disc_percent': ALL,
            'qty_ordered': ALL,
        }
        # auth
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        # always return data
        always_return_data = True
