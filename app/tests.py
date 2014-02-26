from unittest import expectedFailure

from django.contrib.auth.models import User
from django.test import TestCase

from forms import SkuForm
from models import *


class SkuModelTests(TestCase):

    def setUp(self):
        """also satisfies creating a new sku"""
        self.brand = Brand(name='test brand')
        self.brand.save()

        self.category = Category(name='test category')
        self.category.save()

        self.user = User(username='test user', email='name@place.com', is_staff=True)
        self.user.save()

        self.supplier = Supplier(name='test supplier')
        self.supplier.save()

        self.attr1 = Attribute(name='test attr 1')
        self.attr1.save()
        self.attr2 = Attribute(name='test attr 2')
        self.attr2.save()

        self.cost_reason = CostAdjustmentReason(name='test cost adjustment')
        self.cost_reason.save()

        self.qty_reason = QuantityAdjustmentReason(name='test qty adjustment')
        self.qty_reason.save()

        # hack to get skus in -- system assumes initial sku population from synced doc
        previous_sku = Sku(
            id=123,
            name='previous sku',
            brand=self.brand,
            quantity_on_hand=174,
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

    @expectedFailure
    def test_update_illegal_qty(self):
        self.sku.quantity_on_hand = 50
        self.sku.save()

    @expectedFailure
    def test_update_illegal_cost(self):
        self.cost = 12.98
        self.sku.save()

    def test_attributes_property(self):
        sa1 = SkuAttribute(sku=self.sku, attribute=self.attr1, value='hola')
        sa1.save()
        sa2 = SkuAttribute(sku=self.sku, attribute=self.attr2, value='howdy')
        sa2.save()
        self.assertEqual(len(self.sku.attributes), 2)

    def test_description_property(self):
        sa1 = SkuAttribute(sku=self.sku, attribute=self.attr1, value='hola')
        sa1.save()
        sa2 = SkuAttribute(sku=self.sku, attribute=self.attr2, value='howdy')
        sa2.save()
        self.assertEqual(self.sku.description, '[124] test brand test sku : hola, howdy')

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
            phone='312 555 0123',
            address1='123 Fake St',
            city='Anytown',
            state='OH',
            zipcode='12345',
            represents=self.supplier,
            label=self.label
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

        # hack to get skus in -- system assumes initial sku population from synced doc
        self.sku1 = Sku(
            id=123,
            name='test sku 1',
            brand=self.brand,
            quantity_on_hand=174,
            owner=self.user,
            supplier=self.supplier
        )
        self.sku1.save(gdocs=True)

        self.sku2 = Sku(
            name='test sku 2',
            brand=self.brand,
            quantity_on_hand=0,
            owner=self.user,
            supplier=self.supplier
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

        self.cost_reason = CostAdjustmentReason(name='test')
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
            phone='312 555 0123',
            address1='123 Fake St',
            city='Anytown',
            state='OH',
            zipcode='12345',
            represents=self.supplier,
            label=self.label
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

    @expectedFailure
    def test_cost_adjustment_url(self):
        """not in url conf"""
        self.assertEqual(
            self.cost_adj.get_absolute_url(),
            '/cost_adjustments/1/'
        )

    @expectedFailure
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
