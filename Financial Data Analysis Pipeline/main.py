"""
main.py
-------
Orchestrates the full Financial Data Analysis Pipeline.

Usage:
    python main.py                  # uses data/transactions.csv
    python main.py --file my.csv    # custom dataset
    python main.py --generate       # generate demo data first, then run
"""

import argparse
import sys
from pathlib import Path

# ── Make sure src/ is on the path when running from project root ──────────────
sys.path.insert(0, str(Path(__file__).parent / "src"))

from data_cleaning  import load_data, clean_data
from analysis       import (compute_kpis, monthly_trend, category_breakdown,
                            regional_analysis, department_analysis, anomaly_report)
from visualization  import generate_report


# ─────────────────────────────────────────────────────────────────────────────

def run_pipeline(filepath: str) -> None:
    print("\n" + "="*60)
    print("  FINANCIAL DATA ANALYSIS PIPELINE")
    print("="*60)

    # 1. LOAD ─────────────────────────────────────────────────────────────────
    print("\n[1/5] Loading data …")
    df_raw = load_data(filepath)

    # 2. CLEAN ────────────────────────────────────────────────────────────────
    print("[2/5] Cleaning data …")
    df, cleaning_report = clean_data(df_raw)
    print(f"      → Rows after cleaning: {len(df):,}")
    for step, val in cleaning_report.items():
        print(f"      {step}: {val}")

    # 3. ANALYSE ──────────────────────────────────────────────────────────────
    print("[3/5] Running analysis …")
    kpis       = compute_kpis(df)
    trend      = monthly_trend(df)
    cat_df     = category_breakdown(df)
    regional   = regional_analysis(df)
    dept       = department_analysis(df)
    anomalies  = anomaly_report(df)

    # Print KPIs
    print("\n  ── KPI Summary ─────────────────────────────────")
    for k, v in kpis.items():
        label = k.replace("_", " ").title()
        print(f"  {label:<25} {v}")

    # Print top 5 anomalies
    if not anomalies.empty:
        print(f"\n  ── Top Anomalies (showing 5 of {len(anomalies)}) ──────────")
        print(anomalies.head(5).to_string(index=False))

    # 4. SAVE CSV RESULTS ─────────────────────────────────────────────────────
    print("\n[4/5] Saving result tables …")
    Path("report").mkdir(exist_ok=True)
    df.to_csv("report/clean_data.csv", index=False)
    trend.to_csv("report/monthly_trend.csv", index=False)
    cat_df.to_csv("report/category_breakdown.csv", index=False)
    dept.to_csv("report/department_analysis.csv", index=False)
    if not anomalies.empty:
        anomalies.to_csv("report/anomalies.csv", index=False)
    print("      → CSVs written to report/")

    # 5. VISUALISE ────────────────────────────────────────────────────────────
    print("[5/5] Generating visualisations …")
    generate_report(
        df=df,
        trend=trend,
        cat_df=cat_df,
        regional_df=regional,
        kpis=kpis,
        output_path="report/results.png",
    )

    print("\n" + "="*60)
    print("  PIPELINE COMPLETE")
    print("="*60)
    print("  Outputs:")
    print("    report/results.png       ← main dashboard")
    print("    report/mom_growth.png    ← MoM growth chart")
    print("    report/clean_data.csv")
    print("    report/monthly_trend.csv")
    print("    report/category_breakdown.csv")
    print("    report/department_analysis.csv")
    print("    report/anomalies.csv")
    print("="*60 + "\n")


# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Financial Data Analysis Pipeline")
    parser.add_argument("--file",     default="data/transactions.csv",
                        help="Path to input CSV (default: data/transactions.csv)")
    parser.add_argument("--generate", action="store_true",
                        help="Generate synthetic demo data before running")
    args = parser.parse_args()

    if args.generate:
        print("Generating synthetic dataset …")
        import runpy
        runpy.run_path("data/generate_data.py")

    run_pipeline(args.file)
