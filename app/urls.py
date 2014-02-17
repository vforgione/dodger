from django.conf.urls import patterns, url


urlpatterns = patterns(
    'app.views',

    # sku quantity change trace
    url(r'^sku-quantity-adjustment(?:/(?P<pk>\d+))?/$', 'warehouse.sku_qty_adj__view', name='sku_qty_adj__view'),
    url(r'^sku-quantity-adjustment/create/$', 'warehouse.sku_qty_adj__create', name='sku_qty_adj__create'),

    # purchase orders
    url(r'^purchase-order(?:/(?P<pk>\d+))?/$', 'dat.po__view', name='po__view'),
    url(r'^purchase-order/create/$', 'dat.po__create', name='po__create'),

    # shipments
    url(r'^shipment(?:/(?P<pk>\d+))?/$', 'warehouse.shipment__view', name='shipment__view'),
    url(r'^shipment/create/$', 'warehouse.shipment__create', name='shipment__create'),

    # skus
    url(r'^sku(?:/(?P<pk>\d+))?/$', 'skus.sku__view', name='sku__view'),
)
