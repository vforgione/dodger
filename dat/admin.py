from django.contrib import admin

from models import Supplier, ContactLabel, Contact, Receiver, PurchaseOrder, PurchaseOrderProduct


class ContactLabelAdmin(admin.ModelAdmin):

    exclude = ('id', )
    search_fields = ('name', )


class ContactAdmin(admin.ModelAdmin):

    search_fields = ('name', 'represents__name', 'label')
    list_filter = ('label', )


class ContactInline(admin.StackedInline):

    model = Contact
    extra = 1


class SupplierAdmin(admin.ModelAdmin):

    exclude = ('id', )
    inlines = (ContactInline, )
    search_fields = ('name', )


class PurchaseOrderProductInline(admin.TabularInline):

    model = PurchaseOrderProduct
    extra = 3


class PurchaseOrderAdmin(admin.ModelAdmin):

    exclude = ('name', )
    inlines = (PurchaseOrderProductInline, )
    search_fields = (
        'name', 'supplier__name', 'contact__name', 'contact__email', 'dat_member__first_name',
        'dat_member__last_name', 'dat_member__email', 'comments'
    )
    list_filter = ('created', 'dat_member__last_name')


admin.site.register(Supplier, SupplierAdmin)
admin.site.register(ContactLabel, ContactLabelAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Receiver)
admin.site.register(PurchaseOrder, PurchaseOrderAdmin)
admin.site.register(PurchaseOrderProduct)
