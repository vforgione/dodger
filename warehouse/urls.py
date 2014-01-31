from django.conf.urls import patterns, url


urlpatterns = patterns(
    'warehouse.views',

    # shipments
    url(r'^shipments(?:/(?P<pk>\d+))?/$', 'shipment_view', name='shipment-view'),
    url(r'^shipments/receive/$', 'shipment_create', name='shipment-create'),
)
