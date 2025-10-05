from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.orders import OrderItem, OrderItemCreate, Order
from app.services.order_service import (
    add_item_to_order,
    remove_item_from_order,
    update_order_total
)
from app.models.orders import Order as OrderModel
from sqlalchemy import select

router = APIRouter()


@router.post("/{order_id}/items", response_model=OrderItem)
async def add_item_to_order_endpoint(
    order_id: int,
    item: OrderItemCreate,
    db: AsyncSession = Depends(get_db)
):
    """Добавляет товар в заказ или увеличивает количество существующего."""
    return await add_item_to_order(
        db, order_id, item.nomenclature_id, item.quantity
    )


@router.delete("/{order_id}/items/{item_id}")
async def remove_item_from_order_endpoint(
    order_id: int,
    item_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Удаляет позицию из заказа и возвращает товар на склад."""
    success = await remove_item_from_order(db, order_id, item_id)
    return {"success": success, "message": "Позиция удалена"}


@router.get("/{order_id}", response_model=Order)
async def get_order(
    order_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Получает заказ с позициями."""
    order_result = await db.execute(
        select(OrderModel).where(OrderModel.id == order_id)
    )
    order = order_result.scalar_one_or_none()

    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")

    return order
