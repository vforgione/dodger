from django.contrib import admin

from models import Shipment, ShipmentProduct


class ShipmentProductAdmin(admin.ModelAdmin):
    """simple admin for shipment line items"""

    exclude = ('slug', )


class ShipmentProductInline(admin.TabularInline):
    """inline form to processes items with shipment accounting"""

    model = ShipmentProduct
    extra = 5
    exclude = ('slug', )


class ShipmentAdmin(admin.ModelAdmin):
    """admin for shipments including inline form for processing line items"""

    exclude = ('slug', )
    inlines = (ShipmentProductInline, )
    list_filter = ('received_on', 'received_by__username')
    search_fields = ('received_on', 'received_by__username', 'received_by__first_name', 'received_by__last_name', )


admin.site.register(Shipment, ShipmentAdmin)
admin.site.register(ShipmentProduct, ShipmentProductAdmin)
