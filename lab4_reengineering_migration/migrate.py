"""Import the legacy CSV inventory into SQLite."""

import csv
import os
from decimal import Decimal
from pathlib import Path

from database import initialize_database
from repository import add_item, count_items

CSV_PATH = Path(os.getenv("INVENTORY_CSV_PATH", str(Path(__file__).parent / "data" / "inventory.csv")))


def migrate_csv_to_sqlite(csv_path: Path = CSV_PATH) -> int:
    """Import CSV rows only when the target SQLite table is empty.

    Returns the number of records imported. Running the migration again is
    safe: it does not duplicate records if data has already been imported.
    """
    initialize_database()
    if count_items() > 0:
        return 0

    imported = 0
    with csv_path.open("r", newline="", encoding="utf-8") as source:
        reader = csv.DictReader(source)
        for row in reader:
            quantity = int(row["quantity"])
            price = Decimal(row["price"])
            add_item(row["item_name"].strip(), quantity, float(price))
            imported += 1
    return imported


if __name__ == "__main__":
    print(f"Imported {migrate_csv_to_sqlite()} record(s) into SQLite.")
