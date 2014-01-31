from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from tastypie.api import Api


from api import UserResource

from dat.api import SupplierResource, ContactLabelResource, ContactResource, \
    ReceiverResource, PurchaseOrderResource, PurchaseOrderProductResource

from inventory_manager.api import CategoryResource, ManufacturerResource, AttributeResource, \
    ProductResource, ProductAttributeResource, ProductQtyChangeResource, ProductCostChangeResource, \
    ProductPriceChangeResource, ReasonResource

from warehouse.api import ShipmentResource, ShipmentProductResource


api_auth = Api(api_name='auth')
api_auth.register(UserResource())

api_dat = Api(api_name='dat')
api_dat.register(SupplierResource())
api_dat.register(ContactLabelResource())
api_dat.register(ContactResource())
api_dat.register(ReceiverResource())
api_dat.register(PurchaseOrderResource())
api_dat.register(PurchaseOrderProductResource())

api_im = Api(api_name='inventory-manager')
api_im.register(CategoryResource())
api_im.register(ManufacturerResource())
api_im.register(AttributeResource())
api_im.register(ProductResource())
api_im.register(ProductAttributeResource())
api_im.register(ProductQtyChangeResource())
api_im.register(ProductCostChangeResource())
api_im.register(ProductPriceChangeResource())
api_im.register(ReasonResource())

api_wh = Api(api_name='warehouse')
api_wh.register(ShipmentResource())
api_wh.register(ShipmentProductResource())


admin.autodiscover()


urlpatterns = patterns(
    '',

    # admin
    url(r'^admin/docs/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # api
    url(r'^api/', include(api_auth.urls + api_dat.urls + api_im.urls + api_wh.urls)),

    # dat front end
    url(r'^dat/', include('dat.urls', namespace='dat')),

    # warehouse front end
    url(r'^warehouse/', include('warehouse.urls', namespace='warehouse')),

    # home page
    url(r'^$', TemplateView.as_view(template_name='dodger/home.html')),
)
