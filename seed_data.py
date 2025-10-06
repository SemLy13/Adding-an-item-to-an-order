#!/usr/bin/env python3
"""
Скрипт для заполнения базы данных тестовыми данными
"""
import asyncio
from decimal import Decimal
from datetime import datetime, timezone

from sqlalchemy import text
from app.db.database import AsyncSessionLocal
from app.models import Category, Nomenclature, Client, Order, OrderItem


async def create_test_data():
    """Создает тестовые данные для всех таблиц"""
    async with AsyncSessionLocal() as session:
        try:
            # 1. Создание категорий
            print("Создание категорий...")
            
            # Категории первого уровня
            electronics = Category(name="Электроника")
            clothing = Category(name="Одежда")
            books = Category(name="Книги")
            
            session.add_all([electronics, clothing, books])
            await session.flush()  # Получаем ID
            
            # Подкатегории
            phones = Category(name="Телефоны", parent_id=electronics.id)
            laptops = Category(name="Ноутбуки", parent_id=electronics.id)
            shirts = Category(name="Рубашки", parent_id=clothing.id)
            pants = Category(name="Брюки", parent_id=clothing.id)
            fiction = Category(name="Художественная литература", parent_id=books.id)
            tech_books = Category(name="Техническая литература", parent_id=books.id)
            
            session.add_all([phones, laptops, shirts, pants, fiction, tech_books])
            await session.flush()
            
            # 2. Создание товаров
            print("Создание товаров...")
            
            nomenclature_items = [
                # Электроника
                Nomenclature(
                    name="iPhone 15",
                    quantity=10,
                    price=Decimal("999.99"),
                    category_id=phones.id,
                    top_category_id=electronics.id
                ),
                Nomenclature(
                    name="Samsung Galaxy S24",
                    quantity=15,
                    price=Decimal("899.99"),
                    category_id=phones.id,
                    top_category_id=electronics.id
                ),
                Nomenclature(
                    name="MacBook Pro M3",
                    quantity=5,
                    price=Decimal("2499.99"),
                    category_id=laptops.id,
                    top_category_id=electronics.id
                ),
                Nomenclature(
                    name="Dell XPS 13",
                    quantity=8,
                    price=Decimal("1299.99"),
                    category_id=laptops.id,
                    top_category_id=electronics.id
                ),
                
                # Одежда
                Nomenclature(
                    name="Белая рубашка",
                    quantity=25,
                    price=Decimal("49.99"),
                    category_id=shirts.id,
                    top_category_id=clothing.id
                ),
                Nomenclature(
                    name="Синие джинсы",
                    quantity=20,
                    price=Decimal("79.99"),
                    category_id=pants.id,
                    top_category_id=clothing.id
                ),
                
                # Книги
                Nomenclature(
                    name="1984 - Джордж Оруэлл",
                    quantity=30,
                    price=Decimal("12.99"),
                    category_id=fiction.id,
                    top_category_id=books.id
                ),
                Nomenclature(
                    name="Python для начинающих",
                    quantity=40,
                    price=Decimal("29.99"),
                    category_id=tech_books.id,
                    top_category_id=books.id
                ),
            ]
            
            session.add_all(nomenclature_items)
            await session.flush()
            
            # 3. Создание клиентов
            print("Создание клиентов...")
            
            clients = [
                Client(name="Иван Петров", address="ул. Ленина, 10, Москва"),
                Client(name="Мария Сидорова", address="пр. Победы, 25, СПб"),
                Client(name="Алексей Козлов", address="ул. Мира, 5, Казань"),
                Client(name="Елена Волкова", address="ул. Садовая, 15, Екатеринбург"),
                Client(name="Дмитрий Соколов", address="пр. Гагарина, 30, Новосибирск"),
            ]
            
            session.add_all(clients)
            await session.flush()
            
            # 4. Создание заказов
            print("Создание заказов...")
            
            now = datetime.now(timezone.utc)
            
            orders = [
                Order(
                    client_id=clients[0].id,
                    total_amount=Decimal("0.00"),
                    created_at=now
                ),
                Order(
                    client_id=clients[1].id,
                    total_amount=Decimal("0.00"),
                    created_at=now
                ),
                Order(
                    client_id=clients[2].id,
                    total_amount=Decimal("0.00"),
                    created_at=now
                ),
            ]
            
            session.add_all(orders)
            await session.flush()
            
            # 5. Создание позиций заказов
            print("Создание позиций заказов...")
            
            order_items = [
                # Заказ 1 - Иван Петров
                OrderItem(
                    order_id=orders[0].id,
                    nomenclature_id=nomenclature_items[0].id,  # iPhone 15
                    quantity=1,
                    price=Decimal("999.99"),
                    total_price=Decimal("999.99")
                ),
                OrderItem(
                    order_id=orders[0].id,
                    nomenclature_id=nomenclature_items[4].id,  # Белая рубашка
                    quantity=2,
                    price=Decimal("49.99"),
                    total_price=Decimal("99.98")
                ),
                
                # Заказ 2 - Мария Сидорова
                OrderItem(
                    order_id=orders[1].id,
                    nomenclature_id=nomenclature_items[2].id,  # MacBook Pro
                    quantity=1,
                    price=Decimal("2499.99"),
                    total_price=Decimal("2499.99")
                ),
                OrderItem(
                    order_id=orders[1].id,
                    nomenclature_id=nomenclature_items[6].id,  # 1984
                    quantity=3,
                    price=Decimal("12.99"),
                    total_price=Decimal("38.97")
                ),
                
                # Заказ 3 - Алексей Козлов
                OrderItem(
                    order_id=orders[2].id,
                    nomenclature_id=nomenclature_items[1].id,  # Samsung Galaxy
                    quantity=1,
                    price=Decimal("899.99"),
                    total_price=Decimal("899.99")
                ),
                OrderItem(
                    order_id=orders[2].id,
                    nomenclature_id=nomenclature_items[5].id,  # Джинсы
                    quantity=1,
                    price=Decimal("79.99"),
                    total_price=Decimal("79.99")
                ),
                OrderItem(
                    order_id=orders[2].id,
                    nomenclature_id=nomenclature_items[7].id,  # Python книга
                    quantity=2,
                    price=Decimal("29.99"),
                    total_price=Decimal("59.98")
                ),
            ]
            
            session.add_all(order_items)
            
            # Обновляем суммы заказов
            for order in orders:
                order_items_for_order = [item for item in order_items if item.order_id == order.id]
                order.total_amount = sum(item.total_price for item in order_items_for_order)
            
            # Обновляем остатки товаров
            for item in order_items:
                nomenclature = next(n for n in nomenclature_items if n.id == item.nomenclature_id)
                nomenclature.quantity -= item.quantity
            
            await session.commit()
            print("✅ Тестовые данные успешно созданы!")
            
            # Выводим статистику
            print("\n📊 Статистика созданных данных:")
            categories_count = await session.scalar(
                text('SELECT COUNT(*) FROM categories')
            )
            nomenclature_count = await session.scalar(
                text('SELECT COUNT(*) FROM nomenclature')
            )
            clients_count = await session.scalar(
                text('SELECT COUNT(*) FROM clients')
            )
            orders_count = await session.scalar(
                text('SELECT COUNT(*) FROM orders')
            )
            order_items_count = await session.scalar(
                text('SELECT COUNT(*) FROM order_items')
            )
            
            print(f"Категорий: {categories_count}")
            print(f"Товаров: {nomenclature_count}")
            print(f"Клиентов: {clients_count}")
            print(f"Заказов: {orders_count}")
            print(f"Позиций заказов: {order_items_count}")
            
        except Exception as e:
            print(f"❌ Ошибка при создании тестовых данных: {e}")
            await session.rollback()
            raise


async def main():
    """Главная функция"""
    print("🌱 Запуск заполнения базы данных тестовыми данными...")
    await create_test_data()
    print("🎉 Заполнение завершено!")


if __name__ == "__main__":
    asyncio.run(main())
