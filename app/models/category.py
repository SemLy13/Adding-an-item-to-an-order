from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base

if TYPE_CHECKING:
    from .nomenclature import Nomenclature


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    parent_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("categories.id"), nullable=True
    )

    # relations
    parent: Mapped[Optional["Category"]] = relationship(
        "Category", remote_side=[id], back_populates="children"
    )
    children: Mapped[List["Category"]] = relationship(
        "Category",
        back_populates="parent",
        cascade="all, delete-orphan",
        single_parent=True,
    )
    nomenclatures: Mapped[List["Nomenclature"]] = relationship(
        "Nomenclature",
        back_populates="category",
        foreign_keys="Nomenclature.category_id"
    )

    __table_args__ = (
        Index("ix_categories_parent_id", "parent_id"),
        Index("ix_categories_name", "name"),
    )
