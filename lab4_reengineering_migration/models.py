"""Validated request and response models for the re-engineered inventory API."""

from pydantic import BaseModel, Field, field_validator  # type: ignore[reportMissingImports]


class ItemCreate(BaseModel):
    """Fields accepted when a new inventory item is created."""
    
    item_name: str = Field(min_length=1, max_length=100)
    quantity: int = Field(ge=0)
    price: float = Field(ge=0)

    @field_validator("item_name")
    @classmethod
    def strip_item_name(cls, value: str) -> str:
        """Remove surrounding spaces and reject a name made only of spaces."""
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Item name cannot be blank.")
        return cleaned


class ItemRead(ItemCreate):
    """Item model returned by the API, including its database identifier."""

    id: int


class InventorySummary(BaseModel):
    """Summary values returned by the stock summary endpoint."""

    item_count: int
    total_units: int
    total_stock_value: float
