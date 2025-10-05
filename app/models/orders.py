from __future__ import annotations

from datetime import datetime
from typing import List, TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Index, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base

if TYPE_CHECKING:
    from .client import Client
    from .nomenclature import Nomenclature


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"), nullable=False)
    total_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    # relations
    client: Mapped["Client"] = relationship("Client", back_populates="orders")
    items: Mapped[List["OrderItem"]] = relationship(
        "OrderItem", back_populates="order", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("ix_orders_client_id", "client_id"),
        Index("ix_orders_created_at", "created_at"),
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
    nomenclature_id: Mapped[int] = mapped_column(ForeignKey("nomenclature.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    total_price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)

    # relations
    order: Mapped["Order"] = relationship("Order", back_populates="items")
    nomenclature: Mapped["Nomenclature"] = relationship(
        "Nomenclature", back_populates="order_items"
    )

    __table_args__ = (
        Index("ix_order_items_order_id", "order_id"),
        Index("ix_order_items_nomenclature_id", "nomenclature_id"),
        Index("ix_order_items_order_nomenclature", "order_id", "nomenclature_id"),
    )
