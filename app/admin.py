from django.contrib import admin

from .models import *


class PurchaseOrderLineItemInline(admin.TabularInline):
    """inline for adding line items directly to PO"""

    model = PurchaseOrderLineItem
    extra = 5


class PurchaseOrderAdmin(admin.ModelAdmin):
    """admin for creating POs"""

    inlines = (PurchaseOrderLineItemInline, )


class SkuAttributeInline(admin.TabularInline):
    """inline for adding attributes to skus"""

    model = SkuAttribute
    extra = 5


class SkuAdmin(admin.ModelAdmin):
    """admin for creating new skus"""

    inlines = (SkuAttributeInline, )
    exclude = ('created', 'modified')


def undo_quantity_change(modeladmin, request, queryset):
    """custom admin action to undo qty change"""
    for obj in queryset:
        rollback = SkuQuantityAdjustment()
        rollback.sku = obj.sku
        rollback.new = obj.old
        rollback.reason = QuantityAdjustmentReason.objects.get(name='Admin Rollback')
        rollback.who = request.user
        rollback.save()
undo_quantity_change.short_description = 'Undo Quantity Change'


class QuantityAdjustmentReasonAdmin(admin.ModelAdmin):
    """admin for creating a quantity change"""

    exclude = ('old', 'when')
    actions = [undo_quantity_change, ]


class ShipmentLineItemInline(admin.TabularInline):
    """inline form adding line items to shipments"""

    model = ShipmentLineItem
    extra = 5


class ShipmentAdmin(admin.ModelAdmin):

    inlines = (ShipmentLineItemInline, )


admin.site.register(Supplier)

admin.site.register(Category)

admin.site.register(Brand)

admin.site.register(Attribute)

admin.site.register(Sku, SkuAdmin)

admin.site.register(SkuAttribute)

admin.site.register(QuantityAdjustmentReason, QuantityAdjustmentReasonAdmin)

admin.site.register(SkuQuantityAdjustment)

admin.site.register(ContactLabel)

admin.site.register(Contact)

admin.site.register(Receiver)

admin.site.register(PurchaseOrder, PurchaseOrderAdmin)

admin.site.register(PurchaseOrderLineItem)

admin.site.register(Shipment, ShipmentAdmin)

admin.site.register(ShipmentLineItem)
