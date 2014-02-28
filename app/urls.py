from django.conf.urls import patterns, url


urlpatterns = patterns(
    'app.views',

    ##
    # search
    url(r'^search/$', 'search', name='search'),

    ## adjustments
    # cost adjustments
    url(r'^cost_adjustments(?:/(?P<pk>\d+))?/$', 'cost_adjustment__view', name='cost_adjustment__view'),
    url(r'^cost_adjustments/create/$', 'cost_adjustment__create', name='cost_adjustment__create'),
    url(r'^cost_adjustments/table/$', 'cost_adjustment__table', name='cost_adjustment__table'),
    url(r'^cost_adjustments/export/$', 'cost_adjustment__export', name='cost_adjustment__export'),

    # quantity adjustments
    url(r'^quantity_adjustments(?:/(?P<pk>\d+))?/$', 'quantity_adjustment__view', name='quantity_adjustment__view'),
    url(r'^quantity_adjustments/create/$', 'quantity_adjustment__create', name='quantity_adjustment__create'),
    url(r'^quantity_adjustments/table/$', 'quantity_adjustment__table', name='quantity_adjustment__table'),
    url(r'^quantity_adjustments/export/$', 'quantity_adjustment__export', name='quantity_adjustment__export'),

    ##
    # skus
    url(r'^skus(?:/(?P<pk>\d+))?/$', 'sku__view', name='sku__view'),
    url(r'^skus/create/$', 'sku__create', name='sku__create'),
    url(r'^skus/update(?:/(?P<pk>\d+))?/$', 'sku__update', name='sku__update'),
    url(r'^skus/table/$', 'sku__table', name='sku__table'),
    url(r'^skus/export/$', 'sku__export', name='sku__export'),

    ##
    # purchase orders
    url(r'^purchase_orders(?:/(?P<pk>\d+))?/$', 'purchase_order__view', name='purchase_order__view'),
    url(r'^purchase_orders/create/$', 'purchase_order__create', name='purchase_order__create'),
    url(r'^purchase_orders/update(?:/(?P<pk>\d+))?/$', 'purchase_order__update', name='purchase_order__update'),
    url(r'^purchase_orders/table/$', 'purchase_order__table', name='purchase_order__table'),
    url(r'^purchase_orders/export/$', 'purchase_order__export', name='purchase_order__export'),

    ##
    # purchase order line items
    url(r'^purchase_order_line_items/table/$', 'purchase_order_line_item__table', name='purchase_order_line_item__table'),
    url(r'^purchase_order_line_items/export/$', 'purchase_order_line_item__export', name='purchase_order_line_item__export'),

    ##
    # shipments
    url(r'^shipments(?:/(?P<pk>\d+))?/$', 'shipment__view', name='shipment__view'),
    url(r'^shipments/create/$', 'shipment__create', name='shipment__create'),
    url(r'^shipments/update(?:/(?P<pk>\d+))?/$', 'shipment__update', name='shipment__update'),
    url(r'^shipments/table/$', 'shipment__table', name='shipment__table'),
    url(r'^shipments/export/$', 'shipment__export', name='shipment__export'),

    ##
    # shipment line items
    url(r'^shipment_line_items/table/$', 'shipment_line_item__table', name='shipment_line_item__table'),
    url(r'^shipment_line_items/export/$', 'shipment_line_item__export', name='shipment_line_item__export'),

    ## controls
    # attributes
    url(r'^attributes(?:/(?P<pk>\d+))?/$', 'attribute__view', name='attribute__view'),
    url(r'^attributes/create/$', 'attribute__create', name='attribute__create'),
    url(r'^attributes/update(?:/(?P<pk>\d+))?/$', 'attribute__update', name='attribute__update'),

    # brands
    url(r'^brands(?:/(?P<pk>\d+))?/$', 'brand__view', name='brand__view'),
    url(r'^brands/create/$', 'brand__create', name='brand__create'),
    url(r'^brands/update(?:/(?P<pk>\d+))?/$', 'brand__update', name='brand__update'),

    # categories
    url(r'^categories(?:/(?P<pk>\d+))?/$', 'category__view', name='category__view'),
    url(r'^categories/create/$', 'category__create', name='category__create'),
    url(r'^categories/update(?:/(?P<pk>\d+))?/$', 'category__update', name='category__update'),

    # contact labels
    url(r'^contact_labels(?:/(?P<pk>\d+))?/$', 'contact_label__view', name='contact_label__view'),
    url(r'^contact_labels/create/$', 'contact_label__create', name='contact_label__create'),
    url(r'^contact_labels/update(?:/(?P<pk>\d+))?/$', 'contact_label__update', name='contact_label__update'),

    # cost adj reasons
    url(r'^cost_adjustment_reasons(?:/(?P<pk>\d+))?/$', 'cost_adjustment_reason__view', name='cost_adjustment_reason__view'),
    url(r'^cost_adjustment_reasons/create/$', 'cost_adjustment_reason__create', name='cost_adjustment_reason__create'),
    url(r'^cost_adjustment_reasons/update(?:/(?P<pk>\d+))?/$', 'cost_adjustment_reason__update', name='cost_adjustment_reason__update'),

    # quantity adj reasons
    url(r'^quantity_adjustment_reasons(?:/(?P<pk>\d+))?/$', 'quantity_adjustment_reason__view', name='quantity_adjustment_reason__view'),
    url(r'^quantity_adjustment_reasons/create/$', 'quantity_adjustment_reason__create', name='quantity_adjustment_reason__create'),
    url(r'^quantity_adjustment_reasons/update(?:/(?P<pk>\d+))?/$', 'quantity_adjustment_reason__update', name='quantity_adjustment_reason__update'),

    # suppliers
    url(r'^suppliers(?:/(?P<pk>\d+))?/$', 'supplier__view', name='supplier__view'),
    url(r'^suppliers/create/$', 'supplier__create', name='supplier__create'),
    url(r'^suppliers/update(?:/(?P<pk>\d+))?/$', 'supplier__update', name='supplier__update'),

    ## po endpoints
    # contacts
    url(r'^contacts(?:/(?P<pk>\d+))?/$', 'contact__view', name='contact__view'),
    url(r'^contacts/create/$', 'contact__create', name='contact__create'),
    url(r'^contacts/update(?:/(?P<pk>\d+))?/$', 'contact__update', name='contact__update'),

    # receivers
    url(r'^receivers(?:/(?P<pk>\d+))?/$', 'receiver__view', name='receiver__view'),
    url(r'^receivers/create/$', 'receiver__create', name='receiver__create'),
    url(r'^receivers/update(?:/(?P<pk>\d+))?/$', 'receiver__update', name='receiver__update'),
)
