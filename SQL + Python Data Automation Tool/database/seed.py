"""
seed.py
-------
Creates and populates sample.db with a realistic e-commerce schema.
Run once: python database/seed.py
"""

import sqlite3
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)

DB_PATH = Path(__file__).parent / "sample.db"


PRODUCTS = [
    ("Laptop Pro 15",       "Electronics",    1299.99),
    ("Wireless Mouse",      "Electronics",      29.99),
    ("USB-C Hub",           "Electronics",      49.99),
    ("Standing Desk",       "Furniture",       449.00),
    ("Ergonomic Chair",     "Furniture",       389.00),
    ("Monitor 27\"",        "Electronics",     399.99),
    ("Mechanical Keyboard", "Electronics",     129.99),
    ("Webcam HD",           "Electronics",      89.99),
    ("Desk Lamp",           "Furniture",        39.99),
    ("Notebook Set",        "Stationery",       12.99),
    ("Pen Organizer",       "Stationery",        8.99),
    ("Whiteboard 90x60",    "Stationery",       59.99),
    ("Headphones Pro",      "Electronics",     249.99),
    ("Phone Stand",         "Electronics",      19.99),
    ("Cable Organizer",     "Accessories",      14.99),
]

REGIONS   = ["North", "South", "East", "West", "Central"]
CHANNELS  = ["Online", "Retail", "B2B", "Reseller"]
STATUSES  = ["completed", "completed", "completed", "returned", "pending"]

CUSTOMERS = [
    (f"customer_{i:04d}",
     f"user{i}@example.com",
     random.choice(REGIONS))
    for i in range(1, 301)
]


def build(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()
    cur.executescript("""
    PRAGMA journal_mode=WAL;

    CREATE TABLE IF NOT EXISTS customers (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        name        TEXT    NOT NULL,
        email       TEXT    UNIQUE NOT NULL,
        region      TEXT    NOT NULL,
        created_at  TEXT    NOT NULL DEFAULT (date('now'))
    );

    CREATE TABLE IF NOT EXISTS products (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        name        TEXT    NOT NULL,
        category    TEXT    NOT NULL,
        unit_price  REAL    NOT NULL
    );

    CREATE TABLE IF NOT EXISTS orders (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id  INTEGER NOT NULL REFERENCES customers(id),
        order_date   TEXT    NOT NULL,
        status       TEXT    NOT NULL,
        channel      TEXT    NOT NULL
    );

    CREATE TABLE IF NOT EXISTS order_items (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id    INTEGER NOT NULL REFERENCES orders(id),
        product_id  INTEGER NOT NULL REFERENCES products(id),
        quantity    INTEGER NOT NULL,
        unit_price  REAL    NOT NULL
    );
    """)

    cur.executemany(
        "INSERT INTO customers (name, email, region) VALUES (?,?,?)",
        CUSTOMERS,
    )
    cur.executemany(
        "INSERT INTO products (name, category, unit_price) VALUES (?,?,?)",
        PRODUCTS,
    )
    conn.commit()

    product_ids  = [r[0] for r in cur.execute("SELECT id FROM products").fetchall()]
    customer_ids = [r[0] for r in cur.execute("SELECT id FROM customers").fetchall()]
    start        = datetime(2023, 1, 1)

    orders, items = [], []
    for order_id in range(1, 1201):
        days   = random.randint(0, 729)
        odate  = (start + timedelta(days=days)).strftime("%Y-%m-%d")
        orders.append((
            random.choice(customer_ids),
            odate,
            random.choice(STATUSES),
            random.choice(CHANNELS),
        ))
        n_items = random.randint(1, 4)
        for pid in random.sample(product_ids, k=min(n_items, len(product_ids))):
            price = next(p[2] for p in PRODUCTS if PRODUCTS.index(p) == pid - 1)
            items.append((order_id, pid, random.randint(1, 5), price))

    cur.executemany(
        "INSERT INTO orders (customer_id, order_date, status, channel) VALUES (?,?,?,?)",
        orders,
    )
    cur.executemany(
        "INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (?,?,?,?)",
        items,
    )
    conn.commit()
    print(f"Seeded {len(orders):,} orders, {len(items):,} items → {DB_PATH}")


if __name__ == "__main__":
    if DB_PATH.exists():
        DB_PATH.unlink()
    with sqlite3.connect(DB_PATH) as conn:
        build(conn)
