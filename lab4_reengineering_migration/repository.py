"""Database operations (repository layer) for inventory items."""

from typing import Any

from database import get_connection


def list_items() -> list[dict[str, Any]]:
    """Fetch all inventory records ordered by their database ID."""
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT id, item_name, quantity, price FROM inventory_items ORDER BY id"
        ).fetchall()
    return [dict(row) for row in rows]


def count_items() -> int:
    """Return the number of records in the inventory table."""
    with get_connection() as connection:
        row = connection.execute("SELECT COUNT(*) AS total FROM inventory_items").fetchone()
    return int(row["total"])


def add_item(item_name: str, quantity: int, price: float) -> dict[str, Any]:
    """Insert a new record and return the inserted row."""
    with get_connection() as connection:
        cursor = connection.execute(
            "INSERT INTO inventory_items (item_name, quantity, price) VALUES (?, ?, ?)",
            (item_name, quantity, price),
        )
        row = connection.execute(
            "SELECT id, item_name, quantity, price FROM inventory_items WHERE id = ?",
            (cursor.lastrowid,),
        ).fetchone()
    return dict(row)


def inventory_totals() -> dict[str, int | float]:
    """Calculate item count, total units, and total stock value in SQLite."""
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT COUNT(*) AS item_count,
                   COALESCE(SUM(quantity), 0) AS total_units,
                   COALESCE(SUM(quantity * price), 0) AS total_stock_value
            FROM inventory_items
            """
        ).fetchone()
    return {
        "item_count": int(row["item_count"]),
        "total_units": int(row["total_units"]),
        "total_stock_value": round(float(row["total_stock_value"]), 2),
    }
