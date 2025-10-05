-- Сумма заказанных товаров по каждому клиенту (Наименование клиента, сумма)

```sql
SELECT
    c.name AS client_name,
    COALESCE(SUM(oi.total_price), 0) AS total_amount
FROM clients c
LEFT JOIN orders o ON o.client_id = c.id
LEFT JOIN order_items oi ON oi.order_id = o.id
GROUP BY c.id, c.name
ORDER BY c.name;
```

-- Количество дочерних элементов первого уровня для категорий номенклатуры

```sql
SELECT
    parent.name AS category_name,
    COUNT(child.id) AS children_count
FROM categories parent
LEFT JOIN categories child ON child.parent_id = parent.id
GROUP BY parent.id, parent.name
ORDER BY parent.name;
```

-- Топ-5 самых покупаемых товаров за последний месяц (по количеству штук)
-- Предполагается поле orders.created_at (timestamp)

```sql
CREATE OR REPLACE VIEW view_top5_products_last_month AS
SELECT
    n.name AS product_name,
    COALESCE(p.name, c.name) AS top_level_category,
    SUM(oi.quantity) AS total_quantity
FROM order_items oi
JOIN orders o ON o.id = oi.order_id
JOIN nomenclature n ON n.id = oi.nomenclature_id
LEFT JOIN categories c ON c.id = n.category_id
LEFT JOIN categories p ON p.id = c.parent_id
WHERE o.created_at >= NOW() - INTERVAL '1 month'
GROUP BY n.id, n.name, COALESCE(p.name, c.name)
ORDER BY total_quantity DESC
LIMIT 5;
```

-- Рекомендации по оптимизации

-- Индексы
--   CREATE INDEX IF NOT EXISTS idx_orders_created_at ON orders (created_at);
--   CREATE INDEX IF NOT EXISTS idx_order_items_nomenclature_id ON order_items (nomenclature_id);
--   -- опц.: CREATE INDEX IF NOT EXISTS idx_order_items_nomenclature_order ON order_items (nomenclature_id, order_id);

-- Альтернативный запрос с группировкой по id
```sql
WITH product_base AS (
    SELECT
        n.id AS product_id,
        n.name AS product_name,
        COALESCE(c.parent_id, c.id) AS top_category_id,
        oi.quantity
    FROM order_items oi
    JOIN orders o ON o.id = oi.order_id
    JOIN nomenclature n ON n.id = oi.nomenclature_id
    LEFT JOIN categories c ON c.id = n.category_id
    WHERE o.created_at >= NOW() - INTERVAL '1 month'
)
SELECT
    pb.product_name,
    tc.name AS top_level_category,
    SUM(pb.quantity) AS total_quantity
FROM product_base pb
LEFT JOIN categories tc ON tc.id = pb.top_category_id
GROUP BY pb.product_id, pb.product_name, tc.name
ORDER BY total_quantity DESC
LIMIT 5;
```
