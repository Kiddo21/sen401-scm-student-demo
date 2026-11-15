"""Unit tests for inventory calculations."""

import unittest
from decimal import Decimal

from utils.helpers import highest_stock_item, total_stock_value


class InventoryTests(unittest.TestCase):
    def test_total_stock_value(self):
        items = [
            {"item_name": "Pen", "quantity": 2, "price": Decimal("100.00")},
            {"item_name": "Book", "quantity": 3, "price": Decimal("250.00")},
        ]
        self.assertEqual(total_stock_value(items), Decimal("950.00"))

    def test_empty_inventory_total_is_zero(self):
        self.assertEqual(total_stock_value([]), Decimal("0.00"))

    def test_highest_quantity_item(self):
        items = [
            {"item_name": "Pen", "quantity": 2, "price": Decimal("100.00")},
            {"item_name": "Book", "quantity": 3, "price": Decimal("250.00")},
        ]
        self.assertEqual(highest_stock_item(items)["item_name"], "Book")

    def test_negative_quantity_is_rejected(self):
        with self.assertRaises(ValueError):
            total_stock_value([
                {"item_name": "Pen", "quantity": -1, "price": Decimal("100.00")}
            ])


if __name__ == "__main__":
    unittest.main()
