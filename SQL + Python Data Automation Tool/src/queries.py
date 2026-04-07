"""
queries.py
----------
Central repository for all SQL queries.

Design choices:
- Every query is a plain string constant — easy to test, review, port to other DBs
- Builder functions accept parameters and return (sql, params) tuples
- All dynamic filtering uses bind parameters — NEVER string interpolation
- CTEs used for readability (WITH ... AS)

Goals:
- Window functions (LAG, RANK, running totals)
- CTEs (WITH clause)
- Multi-table JOINs
- Aggregations with HAVING
- Parameterised queries (SQL injection prevention)
"""

# ── Monthly revenue ────────────────────────────────────────────────────────────

MONTHLY_REVENUE = """
    SELECT
        strftime('%Y-%m', o.order_date)          AS month,
        COUNT(DISTINCT o.id)                      AS order_count,
        SUM(oi.quantity * oi.unit_price)          AS revenue,
        COUNT(DISTINCT o.customer_id)             AS unique_customers
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.id
    WHERE o.status = 'completed'
    GROUP BY month
    ORDER BY month
"""

# ── Revenue by product category ───────────────────────────────────────────────

REVENUE_BY_CATEGORY = """
    SELECT
        p.category,
        COUNT(DISTINCT o.id)              AS orders,
        SUM(oi.quantity)                  AS units_sold,
        SUM(oi.quantity * oi.unit_price)  AS revenue,
        AVG(oi.unit_price)                AS avg_unit_price
    FROM order_items oi
    JOIN products    p  ON p.id  = oi.product_id
    JOIN orders      o  ON o.id  = oi.order_id
    WHERE o.status = 'completed'
    GROUP BY p.category
    ORDER BY revenue DESC
"""

# ── Top N products (parameterised) ────────────────────────────────────────────

TOP_PRODUCTS_SQL = """
    SELECT
        p.name                            AS product,
        p.category,
        SUM(oi.quantity)                  AS units_sold,
        SUM(oi.quantity * oi.unit_price)  AS revenue
    FROM order_items oi
    JOIN products p ON p.id = oi.product_id
    JOIN orders   o ON o.id = oi.order_id
    WHERE o.status = 'completed'
    GROUP BY p.id, p.name, p.category
    ORDER BY revenue DESC
    LIMIT ?
"""

def top_products(n: int = 10) -> tuple[str, tuple]:
    return TOP_PRODUCTS_SQL, (n,)


# ── Regional performance ───────────────────────────────────────────────────────

REGIONAL_PERFORMANCE = """
    SELECT
        c.region,
        COUNT(DISTINCT o.id)              AS orders,
        COUNT(DISTINCT o.customer_id)     AS customers,
        SUM(oi.quantity * oi.unit_price)  AS revenue,
        AVG(oi.quantity * oi.unit_price)  AS avg_order_value
    FROM orders      o
    JOIN customers   c  ON c.id = o.customer_id
    JOIN order_items oi ON oi.order_id = o.id
    WHERE o.status = 'completed'
    GROUP BY c.region
    ORDER BY revenue DESC
"""

# ── Sales channel breakdown ────────────────────────────────────────────────────

CHANNEL_BREAKDOWN = """
    SELECT
        o.channel,
        COUNT(DISTINCT o.id)              AS orders,
        SUM(oi.quantity * oi.unit_price)  AS revenue,
        ROUND(
            100.0 * SUM(oi.quantity * oi.unit_price)
            / SUM(SUM(oi.quantity * oi.unit_price)) OVER (),
            2
        )                                 AS revenue_pct
    FROM orders      o
    JOIN order_items oi ON oi.order_id = o.id
    WHERE o.status = 'completed'
    GROUP BY o.channel
    ORDER BY revenue DESC
"""

# ── Customer cohort: repeat vs one-time buyers ────────────────────────────────

CUSTOMER_COHORT = """
    WITH order_counts AS (
        SELECT customer_id, COUNT(*) AS total_orders
        FROM orders
        WHERE status = 'completed'
        GROUP BY customer_id
    )
    SELECT
        CASE
            WHEN total_orders = 1 THEN 'One-time'
            WHEN total_orders BETWEEN 2 AND 4 THEN 'Repeat (2-4)'
            ELSE 'Loyal (5+)'
        END                         AS cohort,
        COUNT(*)                    AS customers,
        SUM(total_orders)           AS total_orders
    FROM order_counts
    GROUP BY cohort
    ORDER BY total_orders DESC
"""

# ── Month-over-month growth (window function) ─────────────────────────────────

MOM_GROWTH = """
    WITH monthly AS (
        SELECT
            strftime('%Y-%m', o.order_date)         AS month,
            SUM(oi.quantity * oi.unit_price)         AS revenue
        FROM orders      o
        JOIN order_items oi ON oi.order_id = o.id
        WHERE o.status = 'completed'
        GROUP BY month
    )
    SELECT
        month,
        revenue,
        LAG(revenue) OVER (ORDER BY month)    AS prev_month_revenue,
        ROUND(
            100.0 * (revenue - LAG(revenue) OVER (ORDER BY month))
            / NULLIF(LAG(revenue) OVER (ORDER BY month), 0),
            2
        )                                      AS mom_growth_pct
    FROM monthly
    ORDER BY month
"""

# ── Order status distribution ─────────────────────────────────────────────────

ORDER_STATUS = """
    SELECT
        status,
        COUNT(*)  AS orders,
        ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS pct
    FROM orders
    GROUP BY status
    ORDER BY orders DESC
"""

# ── Date-filtered revenue (builder) ───────────────────────────────────────────

REVENUE_RANGE_SQL = """
    SELECT
        strftime('%Y-%m', o.order_date)         AS month,
        SUM(oi.quantity * oi.unit_price)         AS revenue
    FROM orders      o
    JOIN order_items oi ON oi.order_id = o.id
    WHERE o.status    = 'completed'
      AND o.order_date BETWEEN ? AND ?
    GROUP BY month
    ORDER BY month
"""

def revenue_in_range(date_from: str, date_to: str) -> tuple[str, tuple]:
    """
    Build a parameterised revenue query for a date range.
    Dates as ISO strings: '2023-01-01', '2023-12-31'
    """
    return REVENUE_RANGE_SQL, (date_from, date_to)
