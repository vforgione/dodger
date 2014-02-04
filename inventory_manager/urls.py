from django.conf.urls import patterns, url


urlpatterns = patterns(
    'inventory_manager.views',

    # products
    url(r'^products(?:/(?P<sku>\d+))?/$', 'product_view', name='product-view'),
    url(r'^products/create/$', 'product_create', name='product-create'),
    url(r'^products/update(?:/(?P<sku>\d+))?/$', 'product_update', name='product-update'),

    # product qty changes
    url(r'product-qty-changes(?:/(?P<pk>\d+))?/$', 'productqtychange_view', name='pqc-view'),
    url(r'product-qty-changes/create/', 'productqtychange_create', name='pqc-create'),
)
