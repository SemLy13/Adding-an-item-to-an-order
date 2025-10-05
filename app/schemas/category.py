from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, ConfigDict


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    parent_id: Optional[int] = None


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    parent_id: Optional[int] = None


class Category(CategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    parent_id: Optional[int] = None
