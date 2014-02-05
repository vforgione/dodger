from django.conf.urls import patterns, url


urlpatterns = patterns(
    'apps.dat.views',

    # purchase orders
    url(r'^purchase-orders(?:/(?P<pk>\d+))?/$',     'purchaseorder_view',   name='purchaseorder-view'),
    url(r'^purchase-orders/create/$',               'purchaseorder_create', name='purchaseorder-create'),

    # suppliers
    url(r'^suppliers(?:/(?P<pk>\d+))?/$',           'supplier_view',        name='supplier-view'),
    url(r'^suppliers/create/$',                     'supplier_create',      name='supplier-create'),
    url(r'^suppliers/update(?:/(?P<pk>\d+))?/$',    'supplier_update',      name='supplier-update'),

    # contacts
    url(r'^contacts(?:/(?P<pk>\d+))?/$',            'contact_view',         name='contact-view'),
    url(r'^contacts/create/$',                      'contact_create',       name='contact-create'),
    url(r'^contacts/update(?:/(?P<pk>\d+))?/$',     'contact_update',       name='contact-update'),

    # receivers
    url(r'^receivers(?:/(?P<pk>\d+))?/$',           'receiver_view',        name='receiver-view'),
    url(r'^receivers/create/$',                     'receiver_create',      name='receiver-create'),
    url(r'^receivers/update(?:/(?P<pk>\d+))?/$',    'receiver_update',      name='receiver-update'),

    # contact labels
    url(r'^contact-labels(?:/(?P<pk>\d+))?/$',      'contactlabel_view',    name='contactlabel-view'),
    url(r'^contact-labels/create/$',                'contactlabel_create',  name='contactlabel-create'),
)
