from __future__ import annotations

from typing import List, TYPE_CHECKING

from sqlalchemy import Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base

if TYPE_CHECKING:
    from .orders import Order


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str | None] = mapped_column(Text, nullable=True)

    # relations
    orders: Mapped[List["Order"]] = relationship("Order", back_populates="client")

    __table_args__ = (
        Index("ix_clients_name", "name"),
    )
