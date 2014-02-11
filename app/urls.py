from django.conf.urls import patterns, url


urlpatterns = patterns(
    'app.views',

    # sku quantity change trace
    url(r'^sku-quantity-adjustment(?:/(?P<pk>\d+))?/$', 'sku_qty_adj__view', name='sku_qty_adj__view'),
    url(r'^sku-quantity-adjustment/create/$', 'sku_qty_adj__create', name='sku_qty_adj__create'),
)
