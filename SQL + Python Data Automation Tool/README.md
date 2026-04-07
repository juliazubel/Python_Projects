# SQL Data Automation Tool

> Python pipeline that connects to a SQL database, runs analytical queries, processes results with pandas, and generates an automated BI dashboard — no BI tool required.

---

## Quick Start

```bash
# 1. Install dependencies
pip install pandas matplotlib

# 2. Seed the sample database (creates database/sample.db)
python database/seed.py

# 3. Run the full pipeline
python main.py

# Or combine both steps
python main.py --seed
```


## Project Structure

```
sql-data-automation/
├── database/
│   ├── seed.py          # Generates sample e-commerce SQLite DB
│   └── sample.db        # Auto-generated (gitignored)
│
├── src/
│   ├── db_connection.py # Connection manager (SQLite + PostgreSQL)
│   ├── queries.py       # All SQL as named constants + query builders
│   ├── analysis.py      # Pandas data processing & KPI computation
│   └── reporting.py     # Chart generation & report assembly
│
├── reports/             # Auto-created pipeline outputs
│   ├── dashboard.png    ← 6-panel BI dashboard
│   └── summary.txt      ← Executive text summary
│
├── main.py              # CLI pipeline orchestrator
└── README.md
```

---

## What the Pipeline Produces

### Dashboard (6 panels)

| Panel | Content |
|---|---|
| Monthly Revenue | Bar chart + 3-month rolling average line |
| Revenue by Channel | Donut chart (Online / Retail / B2B / Reseller) |
| MoM Growth | Month-over-month % change with +/- colour coding |
| Revenue by Category | Horizontal bar chart |
| Revenue by Region | Regional comparison |
| Top Products | Revenue ranking, full-width bar chart |

### Executive KPIs

- Total revenue, last month revenue, MoM growth %
- Total orders, unique customers, average order value
- Best region, top product, loyal customer count

---

## SQL Techniques

```sql
-- Window functions
LAG(revenue) OVER (ORDER BY month)          -- previous period comparison
SUM(...) OVER ()                             -- window total for % share

-- CTEs
WITH order_counts AS (...)                   -- customer cohort analysis

-- Multi-table JOINs
orders → order_items → products → customers

-- Aggregations
GROUP BY + HAVING, strftime() for date bucketing
```

All queries use **bind parameters** — no string interpolation, no SQL injection.

---

## PostgreSQL Support

Switch from SQLite to PostgreSQL by swapping the connection:

```python
from src.db_connection import get_postgres_connection

with get_postgres_connection(
    host="localhost", port=5432,
    dbname="mydb", user="user", password="pass"
) as conn:
    df = query_to_df(conn, MONTHLY_REVENUE)
```

Install driver: `pip install psycopg2-binary`

Queries use standard SQL — compatible with PostgreSQL with minor dialect adjustments (`strftime` → `DATE_TRUNC`).

---

## CLI Options

```bash
python main.py                    # default: database/sample.db, top 10 products
python main.py --seed             # (re)seed sample DB then run
python main.py --db path/to.db    # custom SQLite file
python main.py --top 15           # show top 15 products in dashboard
```

---

## Database Schema

```
customers      orders          order_items     products
──────────     ──────────      ───────────     ──────────
id             id              id              id
name           customer_id ←── order_id        name
email          order_date       product_id ──→ category
region         status          quantity        unit_price
created_at     channel         unit_price
```

Sample data: 300 customers · 1,200 orders · ~3,000 order items · 15 products · 5 regions · 4 channels · 2 years

---

## Stack

| Library | Role |
|---|---|
| `pandas` ≥ 2.0 | DataFrame processing, aggregations |
| `matplotlib` ≥ 3.7 | Chart generation |
| `sqlite3` | Built-in — no install needed |
| `psycopg2-binary` | Optional PostgreSQL driver |

---

- **SQL** — JOINs, CTEs, window functions, aggregations, parameterised queries
- **Python/SQL integration** — context-manager connection pattern, `query_to_df()`
- **Data processing** — rolling averages, YoY growth, cohort classification
- **Reporting automation** — multi-panel dashboard generated entirely in code
- **Software design** — separation of concerns across 4 focused modules
- **Security** — bind parameters throughout, no raw string SQL injection risk

