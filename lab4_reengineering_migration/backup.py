"""Simple sidecar service that periodically backs up the SQLite database."""

import os
import sqlite3
import time
from datetime import datetime, timezone
from pathlib import Path

SOURCE = Path(os.getenv("INVENTORY_DB_PATH", "/app/data/inventory.db"))
DESTINATION_DIR = Path(os.getenv("BACKUP_DIR", "/app/backups"))
INTERVAL_SECONDS = int(os.getenv("BACKUP_INTERVAL_SECONDS", "60"))


def create_backup() -> Path | None:
    """Create a consistent SQLite backup; return None if DB is not ready."""
    if not SOURCE.exists():
        return None
    DESTINATION_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    destination = DESTINATION_DIR / f"inventory-{timestamp}.db"
    with sqlite3.connect(SOURCE) as source_connection:
        with sqlite3.connect(destination) as destination_connection:
            source_connection.backup(destination_connection)
    return destination


def main() -> None:
    """Run the backup sidecar until the container is stopped."""
    print("SQLite backup service started.", flush=True)
    while True:
        backup_file = create_backup()
        if backup_file:
            print(f"Backup created: {backup_file.name}", flush=True)
        else:
            print("Waiting for the inventory database to be created...", flush=True)
        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
