from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class OrderItemBase(BaseModel):
    nomenclature_id: int
    quantity: int = Field(gt=0, description="Количество должно быть > 0")
    price: Decimal = Field(
        ge=0, decimal_places=2, description="Цена должна быть >= 0"
    )


class OrderItemCreate(OrderItemBase):
    pass


class OrderItem(OrderItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_id: int
    total_price: Decimal = Field(ge=0, decimal_places=2)


class OrderBase(BaseModel):
    client_id: int


class OrderCreate(OrderBase):
    items: List[OrderItemCreate]


class OrderUpdate(BaseModel):
    total_amount: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    created_at: Optional[datetime] = None


class Order(OrderBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    total_amount: Decimal = Field(ge=0, decimal_places=2)
    created_at: datetime
    items: List[OrderItem] = []
