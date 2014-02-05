from django.conf.urls import patterns, url


urlpatterns = patterns(
    'apps.inventory_manager.views',

    # products
    url(r'^products(?:/(?P<pk>\d+))?/$',                'product_view',               name='product-view'),
    url(r'^products/create/$',                          'product_create',             name='product-create'),
    url(r'^products/update(?:/(?P<pk>\d+))?/$',         'product_update',             name='product-update'),

    # product qty changes
    url(r'product-qty-changes(?:/(?P<pk>\d+))?/$',      'productqtychange_view',      name='productqtychange-view'),
    url(r'product-qty-changes/create/$',                'productqtychange_create',    name='productqtychange-create'),

    # product cost changes
    url(r'product-cost-changes(?:/(?P<pk>\d+))?/$',     'productcostchange_view',     name='productcostchange-view'),
    url(r'product-cost-changes/create/$',               'productcostchange_create',   name='productcostchange-create'),

    # product price changes
    url(r'product-price-changes(?:/(?P<pk>\d+))?/$',    'productpricechange_view',    name='productpricechange-view'),
    url(r'product-price-changes/create/$',              'productpricechange_create',  name='productpricechange-create'),

    # categories
    url(r'categories/create/$',                         'category_create',            name='category-create'),
    url(r'categorie(?:/(?P<pk>\d+))?/$',                'category_view',              name='category-view'),

    # manufacturers
    url(r'manufacturers/create/$',                      'manufacturer_create',        name='manufacturer-create'),
    url(r'manufacturers(?:/(?P<pk>\d+))?/$',            'manufacturer_view',          name='manufacturer-view'),

    # attributes
    url(r'attributes/create/$',                         'attribute_create',           name='attribute-create'),
    url(r'attributes(?:/(?P<pk>\d+))?/$',               'attribute_view',             name='attribute-view'),
)
