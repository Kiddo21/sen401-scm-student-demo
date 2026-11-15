"""SQLite database setup and connection management."""

import os
import sqlite3
from pathlib import Path

DEFAULT_DATABASE_PATH = Path(__file__).parent / "data" / "inventory.db"


def database_path() -> Path:
    """Read the database location from the environment or use a local default."""
    return Path(os.getenv("INVENTORY_DB_PATH", str(DEFAULT_DATABASE_PATH)))


def get_connection() -> sqlite3.Connection:
    """Create a SQLite connection and return rows by column name."""
    path = database_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path, timeout=30)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database() -> None:
    """Create the inventory table if it does not already exist."""
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS inventory_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT NOT NULL UNIQUE,
                quantity INTEGER NOT NULL CHECK (quantity >= 0),
                price NUMERIC NOT NULL CHECK (price >= 0)
            )
            """
        )
