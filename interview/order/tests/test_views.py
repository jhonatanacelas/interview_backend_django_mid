from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from interview.order.models import Order
from interview.inventory.models import InventoryType, InventoryLanguage, InventoryTag, Inventory
from datetime import date

class OrdersBetweenDatesTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.inventory_type = InventoryType.objects.create(name="Type1")
        self.inventory_language = InventoryLanguage.objects.create(name="Language1")
        self.inventory_tag = InventoryTag.objects.create(name="Tag1")
        self.inventory = Inventory.objects.create(
            name="Test Inventory", type=self.inventory_type, 
            language=self.inventory_language, metadata={})
        
        # Create orders with different start and embargo dates
        Order.objects.create(
            inventory=self.inventory,
            start_date=date(2022, 1, 1),
            embargo_date=date(2022, 1, 10),
            is_active=True
        )
        Order.objects.create(
            inventory=self.inventory,
            start_date=date(2022, 1, 11),
            embargo_date=date(2022, 1, 20),
            is_active=True
        )

    def test_orders_within_date_range(self):
        response = self.client.get(
            reverse("orders-between-dates"),
            {'start_date': '2022-01-01', 'embargo_date': '2022-01-20'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Both orders should be returned

    def test_no_orders_outside_date_range(self):
        response = self.client.get(
            reverse("orders-between-dates"),
            {'start_date': '2022-01-21', 'embargo_date': '2022-01-30'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # No orders should be returned
