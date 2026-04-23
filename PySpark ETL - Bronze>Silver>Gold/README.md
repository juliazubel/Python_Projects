# PySpark ETL - Bronze -> Silver -> Gold

---

## Data Model (Raw Sources)

### customers
- customer_id (string, PK)
- name (string)
- email (string)
- country (string)
- created_at (timestamp)
- updated_at (timestamp)

### orders
- order_id (string, PK)
- customer_id (string, FK)
- order_ts (timestamp)
- status (string) [CREATED, PAID, SHIPPED, CANCELLED]
- currency (string) [PLN, EUR, USD]

### order_items
- order_id (string, FK)
- product_id (string)
- quantity (int)
- unit_price (double)

### payments
- order_id (string, FK)
- payment_ts (timestamp)
- method (string) [CARD, BLIK, PAYPAL]
- amount (double)
- status (string) [SUCCESS, FAILED]
