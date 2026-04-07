"""
main.py
-------
Orchestrates the full SQL Data Automation pipeline.

Usage:
    python main.py                        # run against default sample.db
    python main.py --db path/to/other.db  # custom SQLite file
    python main.py --seed                 # (re)seed sample.db first
    python main.py --top 15              # show top 15 products
"""

import argparse
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from db_connection import get_sqlite_connection, query_to_df, get_table_info
from queries       import (
    MONTHLY_REVENUE, REVENUE_BY_CATEGORY, REGIONAL_PERFORMANCE,
    CHANNEL_BREAKDOWN, CUSTOMER_COHORT, MOM_GROWTH,
    top_products,
)
from analysis  import (
    compute_executive_kpis, enrich_monthly_trend,
    add_revenue_share, rank_regions, classify_growth, validate_dataframe,
)
from reporting import generate_dashboard, save_text_report

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)-8s %(message)s",
)
log = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────

def run(db_path: Path, top_n: int = 10) -> None:
    print("\n" + "=" * 62)
    print("  SQL DATA AUTOMATION PIPELINE")
    print("=" * 62)

    # ── 1. Connect & inspect ──────────────────────────────────────────────────
    print("\n[1/5] Connecting to database …")
    with get_sqlite_connection(db_path) as conn:

        info = get_table_info(conn)
        for _, row in info.iterrows():
            print(f"      {row['table']:<20} {row['row_count']:>6,} rows")

        # ── 2. Run SQL queries ────────────────────────────────────────────────
        print("\n[2/5] Running SQL queries …")
        monthly    = query_to_df(conn, MONTHLY_REVENUE)
        categories = query_to_df(conn, REVENUE_BY_CATEGORY)
        regional   = query_to_df(conn, REGIONAL_PERFORMANCE)
        channels   = query_to_df(conn, CHANNEL_BREAKDOWN)
        cohort     = query_to_df(conn, CUSTOMER_COHORT)
        mom        = query_to_df(conn, MOM_GROWTH)

        sql, params = top_products(top_n)
        products = query_to_df(conn, sql, params)

        print(f"      monthly trend  : {len(monthly)} months")
        print(f"      categories     : {len(categories)}")
        print(f"      regions        : {len(regional)}")
        print(f"      channels       : {len(channels)}")
        print(f"      top products   : {len(products)}")

    # ── 3. Validate & process ─────────────────────────────────────────────────
    print("\n[3/5] Processing & enriching data …")
    validate_dataframe(monthly,    "monthly",    ["month", "revenue", "order_count"])
    validate_dataframe(regional,   "regional",   ["region", "revenue", "customers"])
    validate_dataframe(categories, "categories", ["category", "revenue"])
    validate_dataframe(products,   "products",   ["product", "revenue"])

    monthly    = enrich_monthly_trend(monthly)
    mom        = classify_growth(mom)
    regional   = rank_regions(regional)
    categories = add_revenue_share(categories)

    # ── 4. Compute KPIs ───────────────────────────────────────────────────────
    print("\n[4/5] Computing KPIs …")
    kpis = compute_executive_kpis(monthly, regional, products, cohort)

    print("\n  ── Executive KPIs " + "─" * 40)
    for k, v in kpis.items():
        label = k.replace("_", " ").title()
        val   = f"${v:,.2f}" if "revenue" in k else (
                f"{v:+.2f}%" if "pct" in k else str(v))
        print(f"  {label:<30} {val}")

    # MoM growth table
    print("\n  ── Month-over-Month Growth (last 6 months) " + "─" * 16)
    recent = mom.dropna(subset=["mom_growth_pct"]).tail(6)
    for _, row in recent.iterrows():
        arrow = "▲" if row["mom_growth_pct"] >= 0 else "▼"
        print(f"  {row['month']}  {arrow} {row['mom_growth_pct']:>+6.1f}%  "
              f"({row['growth_label']})")

    # ── 5. Generate reports ───────────────────────────────────────────────────
    print("\n[5/5] Generating reports …")
    generate_dashboard(
        monthly=monthly, mom=mom, categories=categories,
        channels=channels, regional=regional, products=products,
        kpis=kpis, output_path="reports/dashboard.png",
    )
    save_text_report(kpis, "reports/summary.txt")

    print("\n" + "=" * 62)
    print("  PIPELINE COMPLETE")
    print("=" * 62)
    print("  Outputs:")
    print("    reports/dashboard.png   ← BI dashboard")
    print("    reports/summary.txt     ← executive summary")
    print("=" * 62 + "\n")


# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SQL Data Automation Pipeline")
    parser.add_argument("--db",   default="database/sample.db",
                        help="Path to SQLite database")
    parser.add_argument("--seed", action="store_true",
                        help="(Re)seed the sample database before running")
    parser.add_argument("--top",  type=int, default=10,
                        help="Number of top products to include (default: 10)")
    args = parser.parse_args()

    if args.seed:
        print("Seeding sample database …")
        import runpy, os
        os.chdir(Path(__file__).parent)
        runpy.run_path("database/seed.py")

    run(Path(args.db), top_n=args.top)
