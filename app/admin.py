from django.contrib import admin

from models import *


# generic admins
class ControlModelAdmin(admin.ModelAdmin):

    search_fields = ('name', )


class AdjustmentAdmin(admin.ModelAdmin):

    search_fields = ('created', 'who__username', 'sku__id', 'sku__name', 'sku__upc')


class PurchaseOrderEndpointAdmin(admin.ModelAdmin):

    search_fields = ('name', 'city', 'state', 'zipcode')


# complex admins
class SkuAttributeInline(admin.TabularInline):

    model = SkuAttribute
    extra = 8


class SkuAdmin(admin.ModelAdmin):

    search_fields = (
        'id', 'name', 'upc', 'brand__name', 'categories__name', 'location', 'owner__username', 'supplier__name'
    )
    inlines = (SkuAttributeInline, )


class PurchaseOrderLineItemInline(admin.TabularInline):

    model = PurchaseOrderLineItem
    extra = 5


class PurchaseOrderAdmin(admin.ModelAdmin):

    search_fields = ('creator__username', 'supplier__name', 'created')
    inlines = (PurchaseOrderLineItemInline, )


class ShipmentLineItemInline(admin.TabularInline):

    model = ShipmentLineItem
    extra = 5


class ShipmentAdmin(admin.ModelAdmin):

    search_fields = ('creator__username', 'purchase_order__id')
    inlines = (ShipmentLineItemInline, )


admin.site.register(Attribute, ControlModelAdmin)
admin.site.register(Brand, ControlModelAdmin)
admin.site.register(Category, ControlModelAdmin)
admin.site.register(ContactLabel, ControlModelAdmin)
admin.site.register(CostAdjustmentReason, ControlModelAdmin)
admin.site.register(QuantityAdjustmentReason, ControlModelAdmin)
admin.site.register(Supplier, ControlModelAdmin)
admin.site.register(Sku, SkuAdmin)
admin.site.register(SkuAttribute)
admin.site.register(CostAdjustment, AdjustmentAdmin)
admin.site.register(QuantityAdjustment, AdjustmentAdmin)
admin.site.register(Contact, PurchaseOrderEndpointAdmin)
admin.site.register(Receiver, PurchaseOrderEndpointAdmin)
admin.site.register(PurchaseOrder, PurchaseOrderAdmin)
admin.site.register(PurchaseOrderLineItem)
admin.site.register(Shipment, ShipmentAdmin)
admin.site.register(ShipmentLineItem)
