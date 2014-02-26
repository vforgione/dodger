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
