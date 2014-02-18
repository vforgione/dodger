from django.conf.urls import patterns, url


urlpatterns = patterns(
    'app.views',

    # sku quantity change trace
    url(r'^sku-quantity-adjustment(?:/(?P<pk>\d+))?/$', 'warehouse.sku_qty_adj__view', name='sku_qty_adj__view'),
    url(r'^sku-quantity-adjustment/create/$', 'warehouse.sku_qty_adj__create', name='sku_qty_adj__create'),

    # purchase orders
    url(r'^purchase-order(?:/(?P<pk>\d+))?/$', 'dat.po__view', name='po__view'),
    url(r'^purchase-order/create/$', 'dat.po__create', name='po__create'),
    # reporting
    url(r'purchase-order/export/$', 'reporting.po__export', name='po__export'),
    url(r'purchase-order/csv/(?P<start>\d{4}\-\d{2}\-\d{2})/(?P<end>\d{4}\-\d{2}\-\d{2})/$',
        'reporting.po__csv', name='po__csv'),

    # shipments
    url(r'^shipment(?:/(?P<pk>\d+))?/$', 'warehouse.shipment__view', name='shipment__view'),
    url(r'^shipment/create/$', 'warehouse.shipment__create', name='shipment__create'),

    # skus
    url(r'^sku(?:/(?P<pk>\d+))?/$', 'skus.sku__view', name='sku__view'),
    url(r'^sku/create/$', 'skus.sku__create', name='sku__create'),
    url(r'^sku/update(?:/(?P<pk>\d+))?/$', 'skus.sku__update', name='sku__update'),
)
