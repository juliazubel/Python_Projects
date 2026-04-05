# Financial Data Analysis Pipeline

> End-to-end Python pipeline for financial transaction analysis — data cleaning, feature engineering, anomaly detection, and automated report generation.

---

## Quick Start

```bash
# 1. Clone & install dependencies
pip install pandas numpy matplotlib seaborn

# 2. Generate demo data and run the full pipeline
python main.py --generate

# 3. Or use your own CSV
python main.py --file path/to/your/data.csv
```

Outputs land in `report/` — open `results.png` for the full dashboard.

---

## Project Structure

```
financial-data-analysis/
├── data/
│   ├── generate_data.py       # Synthetic dataset generator (2 years, 2 000 rows)
│   └── transactions.csv       # Generated dataset (git-ignored)
│
├── src/
│   ├── data_cleaning.py       # Schema validation, null handling, anomaly flagging
│   ├── analysis.py            # KPIs, monthly trend, regional & dept breakdowns
│   └── visualization.py       # All matplotlib charts + dashboard renderer
│
├── report/                    # Pipeline outputs (auto-created)
│   ├── results.png            ← Main 6-panel dashboard
│   ├── mom_growth.png         ← Month-over-month revenue growth
│   ├── clean_data.csv
│   ├── monthly_trend.csv
│   ├── category_breakdown.csv
│   ├── department_analysis.csv
│   └── anomalies.csv
│
├── main.py                    # Pipeline orchestrator (CLI entry point)
└── README.md
```

---

## What the Pipeline Does

### 1 · Data Cleaning (`src/data_cleaning.py`)

| Step | Technique |
|---|---|
| Schema validation | Raises on missing required columns |
| Null handling | Drops rows with null `amount`; fills categorical nulls |
| Deduplication | Unique `transaction_id` enforcement |
| Type coercion | Numeric + boolean casting with error reporting |
| Anomaly flagging | **IQR method** (3× fence) per category → `is_anomaly` column |
| Feature engineering | `year`, `month`, `quarter`, `weekday`, `is_weekend` |

### 2 · Analysis (`src/analysis.py`)

- **KPI summary** — total revenue, expenses, net cash flow, approval rate
- **Monthly trend** — absolute totals + MoM % growth + 3-month rolling average
- **Category breakdown** — sum, mean, count, std per transaction type
- **Regional analysis** — pivot table of volume per region
- **Department analysis** — financials per department with anomaly counts
- **Anomaly report** — flagged transactions with Z-scores, sorted by severity

### 3 · Visualisation (`src/visualization.py`)

Six charts in a single dark-theme dashboard:

| Chart | Insight |
|---|---|
| Monthly Revenue vs Expenses | Trend over time with rolling average |
| Cumulative Net Cash Flow | Running total with +/- colour fill |
| Category Donut | Distribution of transaction types |
| Anomaly Scatter | All transactions; anomalies highlighted in red |
| Regional Volume | Horizontal bar chart by region |
| MoM Growth | Month-over-month revenue % change (separate file) |

---

## Stack

| Library | Version | Role |
|---|---|---|
| `pandas` | ≥ 2.0 | Data wrangling, aggregations |
| `numpy` | ≥ 1.24 | Statistical calculations |
| `matplotlib` | ≥ 3.7 | All visualisations |

---

## Example Output

After running `python main.py --generate`:

```
══════════════════════════════════════════════════════════
  FINANCIAL DATA ANALYSIS PIPELINE
══════════════════════════════════════════════════════════

[1/5] Loading data …        INFO | Loaded 2000 rows × 7 columns
[2/5] Cleaning data …       INFO | Removed 40 rows with null 'amount'
                            INFO | Anomalies flagged in 'Revenue': 18
[3/5] Running analysis …

  ── KPI Summary ─────────────────────────────────
  Total Transactions        1 958
  Total Revenue         $17 342 801
  Total Expenses        -$8 124 330
  Net Cashflow           $9 218 471
  Anomaly Count                 62
  Anomaly Pct                 3.17%
  Approval Rate              92.1%

[4/5] Saving result tables …
[5/5] Generating visualisations …
  ✓ Dashboard saved  → report/results.png
  ✓ MoM growth chart → report/mom_growth.png
```

