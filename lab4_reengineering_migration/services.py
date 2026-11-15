"""Application service layer for inventory operations."""

from typing import Any

import repository


def get_inventory_report() -> dict[str, Any]:
    """Combine inventory rows and aggregate totals for presentation/API use."""
    return {"items": repository.list_items(), "summary": repository.inventory_totals()}


def create_inventory_item(item_name: str, quantity: int, price: float) -> dict[str, Any]:
    """Create a validated inventory item through the repository layer."""
    return repository.add_item(item_name, quantity, price)
