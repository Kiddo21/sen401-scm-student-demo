"""FastAPI application for the re-engineered inventory system."""

from contextlib import asynccontextmanager
import sqlite3
from typing import AsyncIterator

# pyright: reportMissingImports=false
from fastapi import FastAPI, HTTPException, status

from database import initialize_database
from migrate import migrate_csv_to_sqlite
from models import InventorySummary, ItemCreate, ItemRead
from repository import list_items
from services import create_inventory_item, get_inventory_report


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Prepare the SQLite schema and migrate the legacy CSV on startup."""
    initialize_database()
    migrate_csv_to_sqlite()
    yield


app = FastAPI(
    title="SEN 401 Inventory Management API",
    description="A modular inventory service backed by SQLite.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/", tags=["Health"])
def health_check() -> dict[str, str]:
    """Confirm that the API process is responding."""
    return {"status": "running", "service": "inventory-api"}


@app.get("/items", response_model=list[ItemRead], tags=["Inventory"])
def get_items() -> list[dict]:
    """Return all items currently stored in SQLite."""
    return list_items()


@app.get("/summary", response_model=InventorySummary, tags=["Inventory"])
def get_summary() -> dict:
    """Return item count, total units, and total stock value."""
    return get_inventory_report()["summary"]


@app.post("/items", response_model=ItemRead, status_code=status.HTTP_201_CREATED, tags=["Inventory"])
def create_item(item: ItemCreate) -> dict:
    """Validate and save a new inventory item."""
    try:
        return create_inventory_item(item.item_name, item.quantity, item.price)
    except sqlite3.IntegrityError as error:
        # A duplicate item name violates the database UNIQUE constraint.
        raise HTTPException(status_code=409, detail="Item name already exists.") from error
