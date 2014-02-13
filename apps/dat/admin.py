from django.contrib import admin

from .models import Supplier, ContactLabel, Contact, Receiver, PurchaseOrder, PurchaseOrderProduct


class ContactAdmin(admin.ModelAdmin):
    """simple admin for contacts"""

    search_fields = ('name', 'represents__name', 'label')
    list_filter = ('label', )
    exclude = ('slug', )


class ContactLabelAdmin(admin.ModelAdmin):
    """simple admin for contact labels"""

    exclude = ('slug', )


class ReceiverAdmin(admin.ModelAdmin):
    """simple admin for receivers"""

    exclude = ('slug', )


class PurchaseOrderProductAdmin(admin.ModelAdmin):
    """simple admin for purchase-order-products"""

    exclude = ('slug', )


# complex admins
class ContactInline(admin.StackedInline):
    """inline form for supplier admin - create contact with supplier on same page"""

    model = Contact
    extra = 1
    exclude = ('slug', )


class SupplierAdmin(admin.ModelAdmin):
    """admin for supplier - creates supplier and optionally oen or more contacts for supplier"""

    exclude = ('slug', )
    inlines = (ContactInline, )
    search_fields = ('name', )


class POPInline(admin.TabularInline):
    """inline form for purchase-order-products - create line items with po on same page"""

    model = PurchaseOrderProduct
    extra = 3
    exclude = ('slug', )


class PurchaseOrderAdmin(admin.ModelAdmin):
    """admin for po = create po and optionally three or more line items for po"""

    exclude = ('slug', )
    inlines = (POPInline, )
    list_filter = ('created', 'creator__username')
    search_fields = (
        'name', 'supplier__name', 'contact__name', 'contact__email', 'creator__first_name',
        'creator__last_name', 'creator__email', 'comments'
    )


admin.site.register(Supplier, SupplierAdmin)
admin.site.register(ContactLabel, ContactLabelAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Receiver, ReceiverAdmin)
admin.site.register(PurchaseOrder, PurchaseOrderAdmin)
admin.site.register(PurchaseOrderProduct, PurchaseOrderProductAdmin)
