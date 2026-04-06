"""
analysis.py
-----------
Core financial analytics: aggregations, trend analysis, KPIs, anomaly summary.

Goals:
- GroupBy aggregations (multi-level)
- Rolling / resampling time-series
- Feature engineering (MoM growth, cumulative sums)
- Statistical summaries (Z-score, percentile bands)
"""

import pandas as pd
import numpy as np


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def compute_kpis(df: pd.DataFrame) -> dict:
    """Top-level KPIs for the executive summary card."""
    revenue   = df.loc[df["category"] == "Revenue",   "amount"].sum()
    expenses  = df.loc[df["category"] == "Expenses",  "amount"].sum()
    net       = revenue + expenses          # expenses are negative
    anomalies = df["is_anomaly"].sum() if "is_anomaly" in df.columns else 0

    return {
        "total_transactions": len(df),
        "total_revenue":      round(revenue, 2),
        "total_expenses":     round(expenses, 2),
        "net_cashflow":       round(net, 2),
        "anomaly_count":      int(anomalies),
        "anomaly_pct":        round(anomalies / len(df) * 100, 2),
        "approval_rate":      round(df["approved"].mean() * 100, 2) if "approved" in df else None,
    }


def monthly_trend(df: pd.DataFrame) -> pd.DataFrame:
    """
    Monthly revenue vs expenses with:
    - absolute totals
    - MoM % growth
    - 3-month rolling average
    """
    rev = (
        df[df["category"] == "Revenue"]
        .set_index("date")["amount"]
        .resample("MS")
        .sum()
        .rename("revenue")
    )
    exp = (
        df[df["category"] == "Expenses"]
        .set_index("date")["amount"]
        .abs()
        .resample("MS")
        .sum()
        .rename("expenses")
    )

    trend = pd.concat([rev, exp], axis=1).fillna(0)
    trend["net"]              = trend["revenue"] - trend["expenses"]
    trend["revenue_mom_pct"]  = trend["revenue"].pct_change() * 100
    trend["revenue_rolling3"] = trend["revenue"].rolling(3).mean()
    trend["cumulative_net"]   = trend["net"].cumsum()
    return trend.reset_index().rename(columns={"date": "month"})


def category_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    """Sum, mean, count, std per category."""
    return (
        df.groupby("category")["amount"]
        .agg(total="sum", mean="mean", count="count", std="std")
        .round(2)
        .reset_index()
        .sort_values("total", ascending=False)
    )


def regional_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Revenue & expense totals by region, plus net and transaction count."""
    pivot = df.pivot_table(
        index="region",
        columns="category",
        values="amount",
        aggfunc="sum",
        fill_value=0,
    ).round(2)
    pivot["total_volume"] = df.groupby("region")["amount"].sum().abs()
    pivot["tx_count"]     = df.groupby("region")["transaction_id"].count()
    return pivot.reset_index()


def department_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregated financials by department."""
    return (
        df.groupby("department")
        .agg(
            total_amount=("amount", "sum"),
            avg_transaction=("amount", "mean"),
            transaction_count=("transaction_id", "count"),
            anomaly_count=("is_anomaly", "sum"),
        )
        .round(2)
        .reset_index()
        .sort_values("total_amount", ascending=False)
    )


def anomaly_report(df: pd.DataFrame) -> pd.DataFrame:
    """Return the anomalous transactions with a Z-score column."""
    if "is_anomaly" not in df.columns:
        return pd.DataFrame()

    anom = df[df["is_anomaly"]].copy()
    anom["z_score"] = (
        (anom["amount"] - df["amount"].mean()) / df["amount"].std()
    ).round(2)
    return anom[
        ["transaction_id", "date", "category", "amount", "region", "department", "z_score"]
    ].sort_values("z_score", key=abs, ascending=False)


def quarterly_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Revenue, expenses, and net per quarter."""
    q = (
        df.groupby(["year", "quarter", "category"])["amount"]
        .sum()
        .unstack(fill_value=0)
        .round(2)
    )
    if "Revenue" in q.columns and "Expenses" in q.columns:
        q["Net"] = q["Revenue"] + q["Expenses"]
    return q.reset_index()
