from __future__ import annotations
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class NomenclatureBase(BaseModel):
    name: str
    quantity: int = Field(ge=0, description="Количество должно быть >= 0")
    price: Decimal = Field(ge=0, decimal_places=2, description="Цена должна быть >= 0")


class NomenclatureCreate(NomenclatureBase):
    category_id: Optional[int] = None
    top_category_id: Optional[int] = None


class NomenclatureUpdate(BaseModel):
    name: Optional[str] = None
    quantity: Optional[int] = Field(None, ge=0)
    price: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    category_id: Optional[int] = None
    top_category_id: Optional[int] = None


class Nomenclature(NomenclatureBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    category_id: Optional[int] = None
    top_category_id: Optional[int] = None
