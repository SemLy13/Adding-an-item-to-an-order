from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base

if TYPE_CHECKING:
    from .category import Category
    from .orders import OrderItem


class Nomenclature(Base):
    __tablename__ = "nomenclature"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False, default=0)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categories.id"))
    top_category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categories.id"), nullable=True)

    # relations
    category: Mapped[Optional["Category"]] = relationship(
        "Category", back_populates="nomenclatures", foreign_keys=[category_id]
    )
    top_category: Mapped[Optional["Category"]] = relationship(
        "Category", foreign_keys=[top_category_id]
    )
    order_items: Mapped[List["OrderItem"]] = relationship(
        "OrderItem", back_populates="nomenclature"
    )

    __table_args__ = (
        Index("ix_nomenclature_category_id", "category_id"),
        Index("ix_nomenclature_name", "name"),
        Index("ix_nomenclature_price", "price"),
        Index("ix_nomenclature_top_category_id", "top_category_id"),
    )
