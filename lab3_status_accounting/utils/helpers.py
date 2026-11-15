"""Reusable calculations and validation for inventory records."""

from decimal import Decimal, InvalidOperation
from typing import TypedDict


class InventoryItem(TypedDict):
    item_name: str
    quantity: int
    price: Decimal


def validate_inventory(items: list[InventoryItem]) -> None:
    """Validate each item and prevent invalid quantities/prices."""
    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            raise TypeError(f"Inventory record {index} must be a dictionary.")
        name = item.get("item_name")
        quantity = item.get("quantity")
        price = item.get("price")
        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"Inventory record {index} has an invalid item name.")
        if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity < 0:
            raise ValueError(f"Quantity for {name} must be a non-negative integer.")
        try:
            price_value = price if isinstance(price, Decimal) else Decimal(str(price))
        except (InvalidOperation, TypeError, ValueError) as error:
            raise ValueError(f"Price for {name} must be numeric.") from error
        if price_value < 0:
            raise ValueError(f"Price for {name} cannot be negative.")


def total_stock_value(items: list[InventoryItem]) -> Decimal:
    """Return the value of all stock (quantity multiplied by unit price)."""
    validate_inventory(items)
    return sum(
        (Decimal(item["quantity"]) * Decimal(str(item["price"])) for item in items),
        start=Decimal("0.00"),
    )


def highest_stock_item(items: list[InventoryItem]) -> InventoryItem | None:
    """Return the item with the greatest quantity, if any."""
    validate_inventory(items)
    return max(items, key=lambda item: item["quantity"], default=None)


def lowest_stock_item(items: list[InventoryItem]) -> InventoryItem | None:
    """Return the item with the smallest quantity, if any."""
    validate_inventory(items)
    return min(items, key=lambda item: item["quantity"], default=None)


def format_naira(amount: Decimal) -> str:
    """Format an amount in Nigerian naira with two decimal places."""
    return f"₦{amount:,.2f}"
