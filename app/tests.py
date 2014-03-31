import json
from unittest import expectedFailure

from django.contrib.auth.models import User
from django.test import TestCase
from tastypie.models import ApiKey
from tastypie.test import ResourceTestCase

from forms import SkuForm
from models import *


# ===============================================
#               SKU MODEL TESTS
# -----------------------------------------------
#   test update
#   test update with illegal qty change
#   test update with illegal cost change
#   test attributes property
#   test description property
#   test cost adjustment
#   test quantity adjustment
#   test location swap
# -----------------------------------------------
class SkuModelTests(TestCase):

    def setUp(self):
        """also satisfies creating a new sku"""
        self.brand = Brand(name='Tyson')
        self.brand.save()

        self.category = Category(name='Chew')
        self.category.save()

        self.user = User(username='NickPhillips', email='nphillips@doggyloot.com', is_active=True)
        self.user.save()

        self.supplier = Supplier(name='Tyson Pet')
        self.supplier.save()

        self.attr1 = Attribute(name='Size')
        self.attr1.save()
        self.attr2 = Attribute(name='Expiration Date')
        self.attr2.save()

        self.cost_reason = CostAdjustmentReason(name='Supplier Adjustment')
        self.cost_reason.save()

        self.qty_reason = QuantityAdjustmentReason(name='Spot Count')
        self.qty_reason.save()

        # hack to get skus in -- system assumes initial sku population from synced doc
        previous_sku = Sku(
            id=10160,
            name='True Chews Lil\'s Bully Sticks',
            brand=self.brand,
            quantity_on_hand=23,
            owner=self.user,
            supplier=self.supplier
        )
        previous_sku.save(gdocs=True)

        self.sku = Sku()
        self.sku.name = 'test sku'
        self.sku.brand = self.brand
        self.sku.quantity_on_hand = 0
        self.sku.owner = self.user
        self.sku.supplier = self.supplier
        self.sku.cost = 8.32

        self.sku.save()

    def test_update_ok(self):
        self.sku.name = 'updated test name'
        self.sku.save()
        self.assertEqual(self.sku.name, 'updated test name')

    @expectedFailure
    def test_update_illegal_qty(self):
        self.sku.quantity_on_hand = 50
        self.sku.save()

    @expectedFailure
    def test_update_illegal_cost(self):
        self.cost = 12.98
        self.sku.save()

    def test_attributes_property(self):
        sa1 = SkuAttribute(sku=self.sku, attribute=self.attr1, value='6"')
        sa1.save()
        sa2 = SkuAttribute(sku=self.sku, attribute=self.attr2, value='07/2015')
        sa2.save()
        self.assertEqual(len(self.sku.attributes), 2)

    def test_description_property(self):
        sa1 = SkuAttribute(sku=self.sku, attribute=self.attr1, value='6"')
        sa1.save()
        sa2 = SkuAttribute(sku=self.sku, attribute=self.attr2, value='07/2015')
        sa2.save()
        self.assertEqual(self.sku.description, '[10161] Tyson test sku : (Expiration Date) 07/2015, (Size) 6"')

    def test_cost_adjustment(self):
        cost_adj = CostAdjustment(
            sku=self.sku,
            reason=self.cost_reason,
            who=self.user,
            new=12.98
        )
        old = self.sku.cost
        cost_adj.save()
        self.assertEqual(self.sku.cost, cost_adj.new)
        self.assertEqual(cost_adj.old, old)

    def test_qty_adjustment(self):
        qty_adj = QuantityAdjustment(
            sku=self.sku,
            reason=self.qty_reason,
            who=self.user,
            new=1000
        )
        old = self.sku.quantity_on_hand
        qty_adj.save()
        self.assertEqual(self.sku.quantity_on_hand, qty_adj.new)
        self.assertEqual(qty_adj.old, old)

    def test_location(self):
        self.sku.location = 'some new location'
        self.sku.save()
        self.assertEqual(self.sku.old_location, None)
        self.assertEqual(self.sku.location, 'some new location')
        self.sku.location = 'an even newer location'
        self.sku.save()
        self.assertEqual(self.sku.old_location, 'some new location')
        self.assertEqual(self.sku.location, 'an even newer location')
        print self.sku.location, self.sku.old_location


# ===============================================
#               PO MODEL TESTS
# -----------------------------------------------
#   test is fully received method
# -----------------------------------------------
class PurchaseOrderModelTests(TestCase):

    def setUp(self):
        self.brand = Brand(name='test brand')
        self.brand.save()

        self.category = Category(name='test category')
        self.category.save()

        self.user = User(username='test user', email='name@place.com', is_staff=True)
        self.user.save()

        self.supplier = Supplier(name='test supplier')
        self.supplier.save()

        self.label = ContactLabel(name='test label')
        self.label.save()

        self.contact = Contact(
            name='test contact',
            email='name@place.com',
            work_phone='312 555 0123',
            address1='123 Fake St',
            city='Anytown',
            state='OH',
            zipcode='12345',
            represents=self.supplier
        )
        self.contact.save()

        self.receiver = Receiver(
            name='test receiver',
            address1='321 Fake St',
            city='Anytown',
            state='OH',
            zipcode='12345',
        )
        self.receiver.save()

        self.qty_reason = QuantityAdjustmentReason(name='Received Shipment')
        self.qty_reason.save()

        cost_reason = CostAdjustmentReason(name='Supplier Adjustment')
        cost_reason.save()

        # hack to get skus in -- system assumes initial sku population from synced doc
        self.sku1 = Sku(
            id=123,
            name='test sku 1',
            brand=self.brand,
            quantity_on_hand=174,
            owner=self.user,
            supplier=self.supplier,
            cost=0
        )
        self.sku1.save(gdocs=True)

        self.sku2 = Sku(
            name='test sku 2',
            brand=self.brand,
            quantity_on_hand=0,
            owner=self.user,
            supplier=self.supplier,
            cost=0
        )
        self.sku2.save()

        self.po = PurchaseOrder(
            creator=self.user,
            supplier=self.supplier,
            contact=self.contact,
            receiver=self.receiver,
            terms='NET 1000'
        )
        self.po.save()

        self.po_li1 = PurchaseOrderLineItem(
            purchase_order=self.po,
            sku=self.sku1,
            quantity_ordered=50,
            unit_cost=10
        )
        self.po_li1.save()

        self.po_li2 = PurchaseOrderLineItem(
            purchase_order=self.po,
            sku=self.sku2,
            quantity_ordered=50,
            unit_cost=10
        )
        self.po_li2.save()

    def test_is_fully_received(self):
        self.assertFalse(self.po.is_fully_received())
        shipment1 = Shipment(
            creator=self.user,
            purchase_order=self.po
        )
        shipment1.save()
        s1_li1 = ShipmentLineItem(
            shipment=shipment1,
            sku=self.sku1,
            quantity_received=50
        )
        s1_li1.save()
        self.assertFalse(self.po.is_fully_received())
        shipment2 = Shipment(
            creator=self.user,
            purchase_order=self.po
        )
        shipment2.save()
        s2_li1 = ShipmentLineItem(
            shipment=shipment1,
            sku=self.sku2,
            quantity_received=50
        )
        s2_li1.save()
        self.assertTrue(self.po.is_fully_received())


# ===============================================
#           ABSOLUTE URL METHOD TESTS
# -----------------------------------------------
#   test attribute - expect failure
#   test brand - expect failure
#   test category - expect failure
#   test contact label - expect failure
#   test cost adjustment reason - expect failure
#   test quantity adjustment reason - expect failure
#   test supplier - expect failure
#   test sku
#   test sku attribute - expect failure
#   test cost adjustment
#   test quantity adjustment
#   test contact - expect failure
#   test receiver - expect failure
#   test purchase order
#   test po line item - expect failure
#   test shipment
#   test shipment line item - expect failure
# -----------------------------------------------
class AbsoluteUrlTests(TestCase):

    def setUp(self):
        self.user = User(username='test user', email='name@place.com', is_staff=True)
        self.user.save()

        self.attribute = Attribute(name='test')
        self.attribute.save()

        self.brand = Brand(name='test')
        self.brand.save()

        self.category = Category(name='test')
        self.category.save()

        self.label = ContactLabel(name='test')
        self.label.save()

        self.cost_reason = CostAdjustmentReason(name='Supplier Adjustment')  # explicitly needed later
        self.cost_reason.save()

        self.qty_reason = QuantityAdjustmentReason(name='Received Shipment')  # explicitly needed later for shipment
        self.qty_reason.save()

        self.supplier = Supplier(name='test')
        self.supplier.save()

        self.sku = Sku(
            id=123,
            name='test',
            brand=self.brand,
            quantity_on_hand=0,
            owner=self.user,
            supplier=self.supplier,
            cost=12.22
        )
        self.sku.save(gdocs=True)

        self.sku_attr = SkuAttribute(sku=self.sku, attribute=self.attribute, value='hola')
        self.sku_attr.save()

        self.cost_adj = CostAdjustment(
            sku=self.sku,
            reason=self.cost_reason,
            who=self.user,
            new=12.98
        )
        self.cost_adj.save()

        self.qty_adj = QuantityAdjustment(
            sku=self.sku,
            reason=self.qty_reason,
            who=self.user,
            new=1000
        )
        self.qty_adj.save()

        self.contact = Contact(
            name='test contact',
            email='name@place.com',
            work_phone='312 555 0123',
            address1='123 Fake St',
            city='Anytown',
            state='OH',
            zipcode='12345',
            represents=self.supplier
        )
        self.contact.save()

        self.receiver = Receiver(
            name='test receiver',
            address1='321 Fake St',
            city='Anytown',
            state='OH',
            zipcode='12345',
        )
        self.receiver.save()

        self.po = PurchaseOrder(
            creator=self.user,
            supplier=self.supplier,
            contact=self.contact,
            receiver=self.receiver,
            terms='NET 1000'
        )
        self.po.save()

        self.po_li = PurchaseOrderLineItem(
            purchase_order=self.po,
            sku=self.sku,
            quantity_ordered=50,
            unit_cost=10
        )
        self.po_li.save()

        self.shipment = Shipment(
            creator=self.user,
            purchase_order=self.po
        )
        self.shipment.save()

        self.ship_li = ShipmentLineItem(
            shipment=self.shipment,
            sku=self.sku,
            quantity_received=50
        )
        self.ship_li.save()

    @expectedFailure
    def test_attribute_url(self):
        """not in url conf"""
        self.assertEqual(
            self.attribute.get_absolute_url(),
            '/attributes/1/'
        )

    @expectedFailure
    def test_brand_url(self):
        """not in url conf"""
        self.assertEqual(
            self.brand.get_absolute_url(),
            '/brands/1/'
        )

    @expectedFailure
    def test_category_url(self):
        """not in url conf"""
        self.assertEqual(
            self.category.get_absolute_url(),
            '/categories/1/'
        )

    @expectedFailure
    def test_contact_label_url(self):
        """not in url conf"""
        self.assertEqual(
            self.label.get_absolute_url(),
            '/contact_labels/1/'
        )

    @expectedFailure
    def test_cost_adjustment_reason_url(self):
        """not in url conf"""
        self.assertEqual(
            self.cost_reason.get_absolute_url(),
            '/cost_adjustment_reasons/1/'
        )

    @expectedFailure
    def test_quantity_adjustment_reason_url(self):
        """not in url conf"""
        self.assertEqual(
            self.qty_reason.get_absolute_url(),
            '/quantity_adjustment_reasons/1/'
        )

    @expectedFailure
    def test_supplier_url(self):
        """not in url conf"""
        self.assertEqual(
            self.supplier.get_absolute_url(),
            '/suppliers/1/'
        )

    def test_sku_url(self):
        self.assertEqual(
            self.sku.get_absolute_url(),
            '/skus/123/'  # from above - note the id field is explicitly set
        )

    @expectedFailure
    def test_sku_attr_url(self):
        """not in url conf"""
        self.assertEqual(
            self.sku_attr.get_absolute_url(),
            '/sku_attributes/1/'
        )

    def test_cost_adjustment_url(self):
        """not in url conf"""
        self.assertEqual(
            self.cost_adj.get_absolute_url(),
            '/cost_adjustments/1/'
        )

    def test_quantity_adjustment_url(self):
        """not in url conf"""
        self.assertEqual(
            self.qty_adj.get_absolute_url(),
            '/quantity_adjustments/1/'
        )

    @expectedFailure
    def test_contact_url(self):
        """not in url conf"""
        self.assertEqual(
            self.contact.get_absolute_url(),
            '/contacts/1/'
        )

    @expectedFailure
    def test_receiver_url(self):
        """not in url conf"""
        self.assertEqual(
            self.receiver.get_absolute_url(),
            '/receivers/1/'
        )

    def test_purchase_order_url(self):
        """not in url conf"""
        self.assertEqual(
            self.po.get_absolute_url(),
            '/purchase_orders/1/'
        )

    @expectedFailure
    def test_purchase_order_line_item_url(self):
        """not in url conf"""
        self.assertEqual(
            self.po_li.get_absolute_url(),
            '/purchase_order_line_items/1/'
        )

    def test_shipment_url(self):
        """not in url conf"""
        self.assertEqual(
            self.shipment.get_absolute_url(),
            '/shipments/1/'
        )

    @expectedFailure
    def test_shipment_line_item_url(self):
        """not in url conf"""
        self.assertEqual(
            self.ship_li.get_absolute_url(),
            '/shipment_line_items/1/'
        )


# ===============================================
#               SKU FORM TESTS
# -----------------------------------------------
#   test creation form - no readonly
#   test update form - readonly cost and qty
# -----------------------------------------------
class SkuFormTests(TestCase):

    def setUp(self):
        self.user = User(username='test user', email='name@place.com', is_staff=True)
        self.user.save()

        self.brand = Brand(name='test')
        self.brand.save()

        self.supplier = Supplier(name='test')
        self.supplier.save()

        self.sku = Sku(
            id=123,
            name='test',
            brand=self.brand,
            quantity_on_hand=0,
            owner=self.user,
            supplier=self.supplier,
            cost=12.22
        )
        self.sku.save(gdocs=True)

    def test_create_form(self):
        form = SkuForm()
        self.assertNotIn('readonly', form.fields['cost'].widget.attrs)
        self.assertNotIn('readonly', form.fields['quantity_on_hand'].widget.attrs)

    def test_update_form(self):
        form = SkuForm(instance=self.sku)
        self.assertTrue(form.fields['cost'].widget.attrs['readonly'])
        self.assertTrue(form.fields['quantity_on_hand'].widget.attrs['readonly'])


# ===============================================
#                   API TESTS
# -----------------------------------------------
#
# -----------------------------------------------
class ApiResourceTests(ResourceTestCase):
    """abstract class to make resource-specific tests more concise"""

    def setUp(self):
        super(ApiResourceTests, self).setUp()

        self.user = User.objects.create_superuser('test user', 'name@place.com', 'password')
        self.api_key = ApiKey(user=self.user)
        self.api_key.save()

        try:
            obj = self.model(name='test')
            obj.save()

            self.list_uri = '/api/sku_service/%s/' % self.uri_spec
            self.detail_uri = self.list_uri + '1/'
        except Exception:
            pass

        self.payload = json.dumps({'name': 'test'})

    def get_credentials(self):
        return self.create_apikey(self.user.username, self.api_key)

    @expectedFailure
    def test_get_list(self):
        response = self.api_client.get(self.list_uri, authentication=self.get_credentials())
        self.assertHttpOK(response)

    @expectedFailure
    def test_get_list_unauthorized(self):
        response = self.api_client.get(self.list_uri)
        self.assertHttpUnauthorized(response)

    @expectedFailure
    def test_get_detail(self):
        response = self.api_client.get(self.detail_uri, authentication=self.get_credentials())
        self.assertHttpOK(response)

    @expectedFailure
    def test_get_detail_unauthorized(self):
        response = self.api_client.get(self.detail_uri)
        self.assertHttpUnauthorized(response)

    @expectedFailure
    def test_other_methods(self):
        response = self.api_client.delete(self.detail_uri, authentication=self.get_credentials())
        self.assertHttpMethodNotAllowed(response)

        response = self.api_client.patch(self.detail_uri, data=self.payload, authentication=self.get_credentials())
        self.assertHttpMethodNotAllowed(response)

        response = self.api_client.post(self.detail_uri, data=self.payload, authentication=self.get_credentials())
        self.assertHttpMethodNotAllowed(response)

        response = self.api_client.put(self.detail_uri, data=self.payload, authentication=self.get_credentials())
        self.assertHttpMethodNotAllowed(response)


class AttributeResourceTests(ApiResourceTests):

    def setUp(self):
        self.model = Attribute
        self.uri_spec = 'attributes'
        super(AttributeResourceTests, self).setUp()


class BrandResourceTests(ApiResourceTests):

    def setUp(self):
        self.model = Brand
        self.uri_spec = 'brands'
        super(BrandResourceTests, self).setUp()


class CategoryResourceTests(ApiResourceTests):

    def setUp(self):
        self.model = Category
        self.uri_spec = 'categories'
        super(CategoryResourceTests, self).setUp()


class ContactLabelResourceTests(ApiResourceTests):

    def setUp(self):
        self.model = ContactLabel
        self.uri_spec = 'contact_labels'
        super(ContactLabelResourceTests, self).setUp()


class CostAdjustmentReasonResourceTests(ApiResourceTests):

    def setUp(self):
        self.model = CostAdjustmentReason
        self.uri_spec = 'cost_adjustment_reason'
        super(CostAdjustmentReasonResourceTests, self).setUp()


class QuantityAdjustmentReasonResourceTests(ApiResourceTests):

    def setUp(self):
        self.model = QuantityAdjustmentReason
        self.uri_spec = 'quantity_adjustment_reason'
        super(QuantityAdjustmentReasonResourceTests, self).setUp()


class SupplierResourceTests(ApiResourceTests):

    def setUp(self):
        self.model = Supplier
        self.uri_spec = 'suppliers'
        super(SupplierResourceTests, self).setUp()


class SkuResourceTests(ApiResourceTests):

    def setUp(self):
        self.model = Sku
        self.uri_spec = 'skus'
        super(SkuResourceTests, self).setUp()


class SkuAttributeTests(ApiResourceTests):

    def setUp(self):
        self.model = SkuAttribute
        self.uri_spec = 'sku_attributes'
        super(SkuAttributeTests, self).setUp()


class CostAdjustmentResourceTests(ApiResourceTests):

    def setUp(self):
        self.model = CostAdjustment
        self.uri_spec = 'cost_adjustments'
        super(CostAdjustmentResourceTests, self).setUp()


class QuantityAdjustmentResourceTests(ApiResourceTests):

    def setUp(self):
        self.model = QuantityAdjustment
        self.uri_spec = 'quantity_adjustments'
        super(QuantityAdjustmentResourceTests, self).setUp()


class ContactResourceTests(ApiResourceTests):

    def setUp(self):
        self.model = Contact
        self.uri_spec = 'contacts'
        super(ContactResourceTests, self).setUp()


class ReceiverResourceTests(ApiResourceTests):

    def setUp(self):
        self.model = Receiver
        self.uri_spec = 'receivers'
        super(ReceiverResourceTests, self).setUp()


class PurchaseOrderResourceTests(ApiResourceTests):

    def setUp(self):
        self.model = PurchaseOrder
        self.uri_spec = 'purchase_orders'
        super(PurchaseOrderResourceTests, self).setUp()


class PurchaseOrderLineItemResourceTests(ApiResourceTests):

    def setUp(self):
        self.model = PurchaseOrderLineItem
        self.uri_spec = 'purchase_order_line_items'
        super(PurchaseOrderLineItemResourceTests, self).setUp()


class ShipmentResourceTests(ApiResourceTests):

    def setUp(self):
        self.model = Shipment
        self.uri_spec = 'shipments'
        super(ShipmentResourceTests, self).setUp()


class ShipmentLineItemResourceTests(ApiResourceTests):

    def setUp(self):
        self.model = ShipmentLineItem
        self.uri_spec = 'shipment_line_items'
        super(ShipmentLineItemResourceTests, self).setUp()

