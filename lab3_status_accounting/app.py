"""Inventory application used for Lab 3 configuration status accounting."""

from inventory import inventory
from utils.helpers import (
    format_naira,
    highest_stock_item,
    lowest_stock_item,
    total_stock_value,
)


def main() -> None:
    """Display inventory records and calculate their total stock value."""
    print("=" * 68)
    print("                    INVENTORY STOCK REPORT")
    print("=" * 68)
    print(f"{'ITEM':<22}{'QUANTITY':>12}{'UNIT PRICE':>17}{'STOCK VALUE':>17}")
    print("-" * 68)

    for item in inventory:
        line_value = item["quantity"] * item["price"]
        print(
            f"{item['item_name']:<22}{item['quantity']:>12,}"
            f"{format_naira(item['price']):>17}{format_naira(line_value):>17}"
        )

    print("-" * 68)
    print(f"TOTAL STOCK VALUE: {format_naira(total_stock_value(inventory))}")
    top = highest_stock_item(inventory)
    bottom = lowest_stock_item(inventory)
    if top and bottom:
        print(f"Highest quantity : {top['item_name']} ({top['quantity']} units)")
        print(f"Lowest quantity  : {bottom['item_name']} ({bottom['quantity']} units)")
    else:
        print("Inventory is empty.")
    print("=" * 68)


if __name__ == "__main__":
    main()
