from django.conf.urls import patterns, url


urlpatterns = patterns(
    'inventory_manager.views',

    # products
    url(r'^products(?:/(?P<pk>\d+))?/$', 'product_view', name='product-view'),
    url(r'^products/create/$', 'product_create', name='product-create'),
    url(r'^products/update(?:/(?P<pk>\d+))?/$', 'product_update', name='product-update'),

    # product qty changes
    url(r'product-qty-changes(?:/(?P<pk>\d+))?/$', 'productqtychange_view', name='pqc-view'),
    url(r'product-qty-changes/create/$', 'productqtychange_create', name='pqc-create'),

    # product cost changes
    url(r'product-cost-changes(?:/(?P<pk>\d+))?/$', 'productcostchange_view', name='pcc-view'),
    url(r'product-cost-changes/create/$', 'productcostchange_create', name='pcc-create'),

    # product price changes
    url(r'product-price-changes(?:/(?P<pk>\d+))?/$', 'productpricechange_view', name='ppc-view'),
    url(r'product-price-changes/create/$', 'productpricechange_create', name='ppc-create'),

    # categories
    url(r'categories/create/$', 'category_create', name='category-create'),
    url(r'categories(?:/(?P<pk>[a-zA-Z\-]+))?/$', 'category_view', name='category-view'),

    # manufacturers
    url(r'manufacturers/create/$', 'manufacturer_create', name='manufacturer-create'),
    url(r'manufacturers(?:/(?P<pk>[a-zA-Z\-]+))?/$', 'manufacturer_view', name='manufacturer-view'),

    # attributes
    url(r'attributes/create/$', 'attribute_create', name='attribute-create'),
    url(r'attributes(?:/(?P<pk>[a-zA-Z\-]+))?/$', 'attribute_view', name='attribute-view'),
)
