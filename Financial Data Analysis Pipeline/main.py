"""
main.py
-------
Orchestrates the full Financial Data Analysis Pipeline.

Usage:
    python main.py
    python main.py --file data/transactions.csv
    python main.py --generate
"""

import argparse
import sys
from pathlib import Path

# ── Paths setup ──────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
SRC_DIR = BASE_DIR / "src"
DATA_DIR = BASE_DIR / "data"
REPORT_DIR = BASE_DIR / "report"

# Add src/ to Python path
sys.path.insert(0, str(SRC_DIR))

# Imports
from data_cleaning import load_data, clean_data
from analysis import (
    compute_kpis,
    monthly_trend,
    category_breakdown,
    regional_analysis,
    department_analysis,
    anomaly_report,
)
from visualization import generate_report


# ─────────────────────────────────────────────────────────────────────────────

def run_pipeline(filepath: str) -> None:
    print("\n" + "=" * 60)
    print("  FINANCIAL DATA ANALYSIS PIPELINE")
    print("=" * 60)

    filepath = Path(filepath)

    # 1. LOAD ─────────────────────────────────────────────────────────────────
    print("\n[1/5] Loading data …")
    if not filepath.exists():
        raise FileNotFoundError(f"Dataset not found: {filepath.resolve()}")

    df_raw = load_data(str(filepath))

    # 2. CLEAN ────────────────────────────────────────────────────────────────
    print("[2/5] Cleaning data …")
    df, cleaning_report = clean_data(df_raw)
    print(f"      → Rows after cleaning: {len(df):,}")

    for step, val in cleaning_report.items():
        print(f"      {step}: {val}")

    # 3. ANALYSE ──────────────────────────────────────────────────────────────
    print("[3/5] Running analysis …")
    kpis = compute_kpis(df)
    trend = monthly_trend(df)
    cat_df = category_breakdown(df)
    regional = regional_analysis(df)
    dept = department_analysis(df)
    anomalies = anomaly_report(df)

    # Print KPIs
    print("\n  ── KPI Summary ─────────────────────────────────")
    for k, v in kpis.items():
        label = k.replace("_", " ").title()
        print(f"  {label:<25} {v}")

    # Print anomalies
    if not anomalies.empty:
        print(f"\n  ── Top Anomalies (showing 5 of {len(anomalies)}) ──────────")
        print(anomalies.head(5).to_string(index=False))

    # 4. SAVE CSV RESULTS ─────────────────────────────────────────────────────
    print("\n[4/5] Saving result tables …")
    REPORT_DIR.mkdir(exist_ok=True)

    df.to_csv(REPORT_DIR / "clean_data.csv", index=False)
    trend.to_csv(REPORT_DIR / "monthly_trend.csv", index=False)
    cat_df.to_csv(REPORT_DIR / "category_breakdown.csv", index=False)
    dept.to_csv(REPORT_DIR / "department_analysis.csv", index=False)

    if not anomalies.empty:
        anomalies.to_csv(REPORT_DIR / "anomalies.csv", index=False)

    print(f"      → CSVs written to {REPORT_DIR}")

    # 5. VISUALISE ────────────────────────────────────────────────────────────
    print("[5/5] Generating visualisations …")
    generate_report(
        df=df,
        trend=trend,
        cat_df=cat_df,
        regional_df=regional,
        kpis=kpis,
        output_path=str(REPORT_DIR / "results.png"),
    )

    print("\n" + "=" * 60)
    print("  PIPELINE COMPLETE")
    print("=" * 60)
    print("  Outputs:")
    print(f"    {REPORT_DIR / 'results.png'}")
    print(f"    {REPORT_DIR / 'clean_data.csv'}")
    print(f"    {REPORT_DIR / 'monthly_trend.csv'}")
    print(f"    {REPORT_DIR / 'category_breakdown.csv'}")
    print(f"    {REPORT_DIR / 'department_analysis.csv'}")
    print(f"    {REPORT_DIR / 'anomalies.csv'}")
    print("=" * 60 + "\n")


# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Financial Data Analysis Pipeline")

    parser.add_argument(
        "--file",
        default=str(DATA_DIR / "transactions.csv"),
        help="Path to input CSV (default: data/transactions.csv)",
    )

    parser.add_argument(
        "--generate",
        action="store_true",
        help="Generate synthetic demo data before running",
    )

    args = parser.parse_args()

    # Generate demo data if requested
    if args.generate:
        print("Generating synthetic dataset …")
        import runpy

        runpy.run_path(str(SRC_DIR / "generate_data.py"))

    run_pipeline(args.file)
