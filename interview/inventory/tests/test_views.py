from datetime import datetime, timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APIClient

from interview.inventory.models import (
    Inventory,
    InventoryType,
    InventoryLanguage,
    InventoryTag,
)


class InventoryAfterDateTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.inventory_type = InventoryType.objects.create(name="Type1")
        self.inventory_language = InventoryLanguage.objects.create(name="Language1")
        self.inventory_tag = InventoryTag.objects.create(name="Tag1")

        # Create two Inventory items, one before and one after the specified date
        self.date = timezone.now().date()
        item_before = Inventory.objects.create(
            name="Item Before",
            type=self.inventory_type,
            language=self.inventory_language,
            metadata={},
        )
        # Manually set created_at for item_before to simulate it being created earlier
        Inventory.objects.filter(id=item_before.id).update(
            created_at=self.date - timedelta(days=1)
        )

        self.item_after = Inventory.objects.create(
            name="Item After",
            type=self.inventory_type,
            language=self.inventory_language,
            metadata={},
        )
        # Manually set created_at for item_after to simulate it being created just after the specified date
        Inventory.objects.filter(id=self.item_after.id).update(
            created_at=self.date + timedelta(days=1)
        )

        # Refresh the objects from the database to get the updated created_at values
        item_before.refresh_from_db()
        self.item_after.refresh_from_db()

    def test_get_inventory_after_date(self):
        response = self.client.get(
            reverse("inventory-after-date"), {"date": self.date.strftime("%Y-%m-%d")}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        import pdb

        pdb.set_trace()
        self.assertEqual(
            len(response.data), 1
        )  # Only the "Item After" should be returned
        self.assertEqual(response.data[0]["name"], self.item_after.name)

    def test_get_inventory_invalid_date_format(self):
        response = self.client.get(
            reverse("inventory-after-date"), {"date": "invalid-date-format"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_inventory_serialization(self):
        response = self.client.get(
            reverse("inventory-after-date"), {"date": self.date.strftime("%Y-%m-%d")}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        inventory_item = response.data[0]
        self.assertIn("id", inventory_item)
        self.assertIn("name", inventory_item)
        self.assertIn("type", inventory_item)
        self.assertIn("language", inventory_item)
        self.assertIn("tags", inventory_item)
        self.assertIn("metadata", inventory_item)
        self.assertIn("created_at", inventory_item)
