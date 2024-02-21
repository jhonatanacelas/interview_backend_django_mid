from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from interview.order.models import Order, OrderTag
from interview.inventory.models import InventoryType, InventoryLanguage, InventoryTag, Inventory
from datetime import date

class DeactivateOrderViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.inventory_type = InventoryType.objects.create(name="Type1")
        self.inventory_language = InventoryLanguage.objects.create(name="Language1")
        self.inventory_tag = InventoryTag.objects.create(name="Tag1")
        self.inventory = Inventory.objects.create(
            name="Test Inventory", metadata= {}, 
            type=self.inventory_type, language=self.inventory_language,)

        # Create two orders, both initially active
        self.order1 = Order.objects.create(
            inventory=self.inventory,
            start_date=date.today(),
            embargo_date=date.today(),
            is_active=True
        )
        self.order2 = Order.objects.create(
            inventory=self.inventory,
            start_date=date.today(),
            embargo_date=date.today(),
            is_active=True
        )

    def test_deactivate_order_only_affects_targeted_order(self):
        # Deactivate the first order
        url = reverse('deactivate-order', args=[self.order1.id])
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh from DB to get updated values
        self.order1.refresh_from_db()
        self.order2.refresh_from_db()

        # Check that the first order is deactivated
        self.assertFalse(self.order1.is_active)

        # Check that the second order remains active
        self.assertTrue(self.order2.is_active)

    def test_deactivate_already_deactivated_order(self):
        # Deactivate the first order
        self.order1.is_active = False
        self.order1.save()

        # Attempt to deactivate the first order again
        url = reverse('deactivate-order', args=[self.order1.id])
        response = self.client.patch(url)
        
        # Check for a successful response even though no change was made
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order1.refresh_from_db()  # Refresh to get the latest state

        # Ensure the order remains deactivated
        self.assertFalse(self.order1.is_active)

    def test_deactivate_order_with_invalid_id(self):
        # Try to deactivate an order with a non-existent ID
        non_existent_id = max(self.order1.id, self.order2.id) + 1  # Assumes auto-incrementing IDs
        url = reverse('deactivate-order', args=[non_existent_id])
        response = self.client.patch(url)

        # Expect a 404 Not Found response since the order does not exist
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
