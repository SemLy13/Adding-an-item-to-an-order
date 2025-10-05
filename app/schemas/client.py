from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict


class ClientBase(BaseModel):
    name: str
    address: Optional[str] = None


class ClientCreate(ClientBase):
    pass


class ClientUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None


class Client(ClientBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
