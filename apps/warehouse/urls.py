from django.conf.urls import patterns, url


urlpatterns = patterns(
    'apps.warehouse.views',

    # shipments
    url(r'^shipments(?:/(?P<pk>\d+))?/$',   'shipment_view',    name='shipment-view'),
    url(r'^shipments/receive/$',            'shipment_create',  name='shipment-create'),
)
