from django.contrib import admin
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from models import (
    Category, Manufacturer, Attribute, Product, ProductAttribute, ProductCostChange,
    ProductPriceChange, ProductQtyChange, Reason
)


# =============
# simple admins
# -------------
class CategoryAdmin(admin.ModelAdmin):

    exclude = ('id', )
    search_fields = ('name', )


class ManufacturerAdmin(admin.ModelAdmin):

    exclude = ('id', )
    search_fields = ('name', )


class AttributeAdmin(admin.ModelAdmin):

    exclude = ('id', )
    search_fields = ('name', )


class ReasonAdmin(admin.ModelAdmin):

    exclude = ('id', )
    search_fields = ('name', )


# ===========================================
# product admin - lots of inlines and filters
# -------------------------------------------
class ProductAttributeInline(admin.TabularInline):

    model = ProductAttribute
    extra = 3


class SupplierListFilter(admin.SimpleListFilter):

    title = _('Supplier name')  # name in filter list
    parameter_name = 'supplier'  # querystring parameter

    def lookups(self, request, model_admin):
        """querystring arguments"""
        return (
            ('0-9', _('Numerical')),
            ('A-D', _('A to D')),
            ('E-H', _('E to H')),
            ('I-L', _('I to L')),
            ('M-P', _('M to P')),
            ('Q-T', _('Q to T')),
            ('U-Z', _('U to Z')),
        )

    def queryset(self, request, queryset):
        """performs the lookup based on the querystring parameters"""
        if self.value() == '0-9':
            return queryset.filter(
                Q(manufacturer__name__startswith='0') | Q(manufacturer__name__startswith='1') |
                Q(manufacturer__name__startswith='2') | Q(manufacturer__name__startswith='3') |
                Q(manufacturer__name__startswith='4') | Q(manufacturer__name__startswith='5') |
                Q(manufacturer__name__startswith='6') | Q(manufacturer__name__startswith='7') |
                Q(manufacturer__name__startswith='8') | Q(manufacturer__name__startswith='9')
            )
        elif self.value() == 'A-D':
            return queryset.filter(
                Q(manufacturer__name__startswith='A') | Q(manufacturer__name__startswith='B') |
                Q(manufacturer__name__startswith='C') | Q(manufacturer__name__startswith='D')
            )
        elif self.value() == 'E-H':
            return queryset.filter(
                Q(manufacturer__name__startswith='E') | Q(manufacturer__name__startswith='F') |
                Q(manufacturer__name__startswith='G') | Q(manufacturer__name__startswith='H')
            )
        elif self.value() == 'I-L':
            return queryset.filter(
                Q(manufacturer__name__startswith='I') | Q(manufacturer__name__startswith='J') |
                Q(manufacturer__name__startswith='K') | Q(manufacturer__name__startswith='L')
            )
        elif self.value() == 'M-P':
            return queryset.filter(
                Q(manufacturer__name__startswith='M') | Q(manufacturer__name__startswith='N') |
                Q(manufacturer__name__startswith='O') | Q(manufacturer__name__startswith='P')
            )
        elif self.value() == 'Q-T':
            return queryset.filter(
                Q(manufacturer__name__startswith='Q') | Q(manufacturer__name__startswith='R') |
                Q(manufacturer__name__startswith='S') | Q(manufacturer__name__startswith='T')
            )
        elif self.value() == 'U-Z':
            return queryset.filter(
                Q(manufacturer__name__startswith='U') | Q(manufacturer__name__startswith='V') |
                Q(manufacturer__name__startswith='W') | Q(manufacturer__name__startswith='X') |
                Q(manufacturer__name__startswith='Y') | Q(manufacturer__name__startswith='Z')
            )


class ManufacturerListFilter(admin.SimpleListFilter):

    title = _('Manufacturer name')  # name in filter list
    parameter_name = 'manufacturer'  # querystring parameter

    def lookups(self, request, model_admin):
        """querystring arguments"""
        return (
            ('0-9', _('Numerical')),
            ('A-D', _('A to D')),
            ('E-H', _('E to H')),
            ('I-L', _('I to L')),
            ('M-P', _('M to P')),
            ('Q-T', _('Q to T')),
            ('U-Z', _('U to Z')),
        )

    def queryset(self, request, queryset):
        """performs the lookup based on the querystring parameters"""
        if self.value() == '0-9':
            return queryset.filter(
                Q(manufacturer__name__startswith='0') | Q(manufacturer__name__startswith='1') |
                Q(manufacturer__name__startswith='2') | Q(manufacturer__name__startswith='3') |
                Q(manufacturer__name__startswith='4') | Q(manufacturer__name__startswith='5') |
                Q(manufacturer__name__startswith='6') | Q(manufacturer__name__startswith='7') |
                Q(manufacturer__name__startswith='8') | Q(manufacturer__name__startswith='9')
            )
        elif self.value() == 'A-D':
            return queryset.filter(
                Q(manufacturer__name__startswith='A') | Q(manufacturer__name__startswith='B') |
                Q(manufacturer__name__startswith='C') | Q(manufacturer__name__startswith='D')
            )
        elif self.value() == 'E-H':
            return queryset.filter(
                Q(manufacturer__name__startswith='E') | Q(manufacturer__name__startswith='F') |
                Q(manufacturer__name__startswith='G') | Q(manufacturer__name__startswith='H')
            )
        elif self.value() == 'I-L':
            return queryset.filter(
                Q(manufacturer__name__startswith='I') | Q(manufacturer__name__startswith='J') |
                Q(manufacturer__name__startswith='K') | Q(manufacturer__name__startswith='L')
            )
        elif self.value() == 'M-P':
            return queryset.filter(
                Q(manufacturer__name__startswith='M') | Q(manufacturer__name__startswith='N') |
                Q(manufacturer__name__startswith='O') | Q(manufacturer__name__startswith='P')
            )
        elif self.value() == 'Q-T':
            return queryset.filter(
                Q(manufacturer__name__startswith='Q') | Q(manufacturer__name__startswith='R') |
                Q(manufacturer__name__startswith='S') | Q(manufacturer__name__startswith='T')
            )
        elif self.value() == 'U-Z':
            return queryset.filter(
                Q(manufacturer__name__startswith='U') | Q(manufacturer__name__startswith='V') |
                Q(manufacturer__name__startswith='W') | Q(manufacturer__name__startswith='X') |
                Q(manufacturer__name__startswith='Y') | Q(manufacturer__name__startswith='Z')
            )


class ProductAdmin(admin.ModelAdmin):

    exclude = ('sku', 'created', 'modified')
    inlines = (ProductAttributeInline, )
    search_fields = ('sku', 'name', 'categories__name', 'supplier__name', 'manufacturer__name')
    list_filter = (SupplierListFilter, ManufacturerListFilter, 'created', 'modified')
    fieldsets = (
        ('Identification', {
            'fields': ('name', 'categories', 'supplier', 'manufacturer'),
        }),
        ('DAT Responsibilities', {
            'fields': ('owner', 'reorder_threshold', 'do_not_disturb', 'price', 'cost', 'mfr_sku', 'case_qty'),
        }),
        ('Required Attributes', {
            'fields': ('qty_on_hand', 'location'),
        })
    )


# =========================================
# prod qty change admin - roll back feature
# -----------------------------------------
def undo_qty_change(modeladmin, request, queryset):
    for pqc in queryset:
        new_pqc = ProductQtyChange()
        new_pqc.product = pqc.product
        new_pqc.new_qty = pqc.old_qty
        new_pqc.reason = 'rolling back change %s' % pqc.pk
        new_pqc.who = request.user
        new_pqc.save()
undo_qty_change.short_description = 'Rollback Quantity Change'


class ProductQtyChangeAdmin(admin.ModelAdmin):

    exclude = ('old_qty', )
    actions = [undo_qty_change, ]


# ===========================================
# prod price change admin - roll back feature
# -------------------------------------------
def undo_price_change(modeladmin, request, queryset):
    for ppc in queryset:
        new_ppc = ProductPriceChange()
        new_ppc.product = ppc.product
        new_ppc.new_price = ppc.old_price
        new_ppc.reason = 'rolling back change %s' % ppc.pk
        new_ppc.who = request.user
        new_ppc.save()
undo_price_change.short_description = 'Rollback Price Change'


class ProductPriceChangeAdmin(admin.ModelAdmin):

    exclude = ('old_price', )
    actions = [undo_price_change, ]


# ==========================================
# prod cost change admin - roll back feature
# ------------------------------------------
def undo_cost_change(modeladmin, request, queryset):
    for pcc in queryset:
        new_pcc = ProductCostChange()
        new_pcc.product = pcc.product
        new_pcc.new_cost = pcc.old_cost
        new_pcc.reason = 'rolling back change %s' % pcc.pk
        new_pcc.who = request.user
        new_pcc.save()
undo_cost_change.short_description = 'Rollback Cost Change'


class ProductCostChangeAdmin(admin.ModelAdmin):

    exclude = ('old_cost', )
    actions = [undo_cost_change, ]


# register admins
admin.site.register(Category, CategoryAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductAttribute)
admin.site.register(ProductCostChange, ProductCostChangeAdmin)
admin.site.register(ProductPriceChange, ProductPriceChangeAdmin)
admin.site.register(ProductQtyChange, ProductQtyChangeAdmin)
admin.site.register(Reason, ReasonAdmin)
