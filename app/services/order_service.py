from __future__ import annotations
from decimal import Decimal
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.nomenclature import Nomenclature
from app.models.orders import Order, OrderItem


async def add_item_to_order(
    db: AsyncSession,
    order_id: int,
    nomenclature_id: int,
    quantity: int
) -> OrderItem:
    """Добавляет товар в заказ или увеличивает количество существующего."""
    if quantity <= 0:
        raise HTTPException(
            status_code=400, detail="Количество должно быть больше 0"
        )

    order_result = await db.execute(select(Order).where(Order.id == order_id))
    order = order_result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")

    nomenclature_result = await db.execute(
        select(Nomenclature).where(Nomenclature.id == nomenclature_id)
    )
    nomenclature = nomenclature_result.scalar_one_or_none()
    if not nomenclature:
        raise HTTPException(status_code=404, detail="Товар не найден")

    if nomenclature.quantity < quantity:
        raise HTTPException(
            status_code=400,
            detail=f"Недостаточно товара на складе. "
                   f"Доступно: {nomenclature.quantity}, запрошено: {quantity}"
        )

    existing_item_result = await db.execute(
        select(OrderItem).where(
            OrderItem.order_id == order_id,
            OrderItem.nomenclature_id == nomenclature_id
        )
    )
    existing_item = existing_item_result.scalar_one_or_none()
    if existing_item:

        existing_item.quantity += quantity
        existing_item.total_price = (
            Decimal(str(existing_item.price)) * existing_item.quantity
        )
        order_item = existing_item
    else:

        total_price = Decimal(str(nomenclature.price)) * quantity
        order_item = OrderItem(
            order_id=order_id,
            nomenclature_id=nomenclature_id,
            quantity=quantity,
            price=nomenclature.price,
            total_price=total_price
        )
        db.add(order_item)

    nomenclature.quantity -= quantity

    await update_order_total(db, order)

    await db.commit()
    await db.refresh(order_item)

    return order_item


async def remove_item_from_order(
    db: AsyncSession,
    order_id: int,
    item_id: int
) -> bool:
    """Удаляет позицию из заказа и возвращает товар на склад."""

    order_result = await db.execute(select(Order).where(Order.id == order_id))
    order = order_result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")

    item_result = await db.execute(
        select(OrderItem).where(
            OrderItem.id == item_id,
            OrderItem.order_id == order_id
        )
    )
    order_item = item_result.scalar_one_or_none()
    if not order_item:
        raise HTTPException(
            status_code=404, detail="Позиция заказа не найдена"
        )

    nomenclature_result = await db.execute(
        select(Nomenclature).where(
            Nomenclature.id == order_item.nomenclature_id
        )
    )
    nomenclature = nomenclature_result.scalar_one_or_none()
    if nomenclature:
        nomenclature.quantity += order_item.quantity


    await db.delete(order_item)


    await update_order_total(db, order)

    await db.commit()
    return True


async def update_order_total(db: AsyncSession, order: Order) -> None:
    """Пересчитывает общую сумму заказа на основе позиций."""
    items_result = await db.execute(
        select(OrderItem).where(OrderItem.order_id == order.id)
    )
    items = items_result.scalars().all()

    total_amount = sum(
        Decimal(str(item.total_price)) for item in items
    )
    order.total_amount = total_amount
