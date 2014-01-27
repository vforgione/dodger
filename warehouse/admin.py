from django.contrib import admin

from models import Shipment, ShipmentProduct


class ShipmentProductInline(admin.TabularInline):

    model = ShipmentProduct
    extra = 3


class ShipmentAdmin(admin.ModelAdmin):

    inlines = (ShipmentProductInline, )


admin.site.register(Shipment, ShipmentAdmin)
admin.site.register(ShipmentProduct)
