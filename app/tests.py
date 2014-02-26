from unittest import expectedFailure

from django.contrib.auth.models import User
from django.test import TestCase

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
