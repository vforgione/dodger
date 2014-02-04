from django.conf.urls import patterns, url


urlpatterns = patterns(
    'dat.views',

    # purchase orders
    url(r'^purchase-orders/create/$', 'purchaseorder_create', name='purchaseorder-create'),
    url(r'^purchase-orders(?:/(?P<pk>[a-zA-Z\-\d]+))?/$', 'purchaseorder_view', name='purchaseorder-view'),

    # suppliers - ids are slugs, so the view has to go last as a fall through
    url(r'^suppliers/create/$', 'supplier_create', name='supplier-create'),
    url(r'^suppliers/update(?:/(?P<pk>[a-zA-Z\-]+))?/$', 'supplier_update', name='supplier-update'),
    url(r'^suppliers(?:/(?P<pk>[a-zA-Z\-]+))?/$', 'supplier_view', name='supplier-view'),

    # contacts
    url(r'^contacts(?:/(?P<pk>\d+))?/$', 'contact_view', name='contact-view'),
    url(r'^contacts/create/$', 'contact_create', name='contact-create'),
    url(r'^contacts/update(?:/(?P<pk>\d+))?/$', 'contact_update', name='contact-update'),

    # receivers
    url(r'^receivers(?:/(?P<pk>\d+))?/$', 'receiver_view', name='receiver-view'),
    url(r'^receivers/create/$', 'receiver_create', name='receiver-create'),
    url(r'^receivers/update(?:/(?P<pk>\d+))?/$', 'receiver_update', name='receiver-update'),

    # contact labels - ids are slugs, so the view has to go last as a fall through
    url(r'^contact-labels/create/$', 'contactlabel_create', name='contactlabel-create'),
    url(r'^contact-labels(?:/(?P<pk>[a-zA-Z\-]+))?/$', 'contactlabel_view', name='contactlabel-view'),
)
