"""
analysis.py
-----------
Pure Python/pandas data processing layer.
No SQL here — receives DataFrames, returns DataFrames or dicts.

Goals:
- Pandas aggregation and transformation
- Derived KPI calculation
- Data validation before analysis
- Type-safe return values
"""

import pandas as pd
import numpy as np
import logging

log = logging.getLogger(__name__)


# KPI summary 

def compute_executive_kpis(
    monthly: pd.DataFrame,
    regional: pd.DataFrame,
    products: pd.DataFrame,
    cohort: pd.DataFrame,
) -> dict:
    """
    Aggregate top-level KPIs from multiple DataFrames.
    Returns a flat dict for easy display / export.
    """
    total_revenue = monthly["revenue"].sum()
    last_month    = monthly.iloc[-1]["revenue"] if not monthly.empty else 0
    prev_month    = monthly.iloc[-2]["revenue"] if len(monthly) >= 2 else 0
    mom_delta     = ((last_month - prev_month) / prev_month * 100) if prev_month else 0

    return {
        "total_revenue":        round(total_revenue, 2),
        "total_orders":         int(monthly["order_count"].sum()),
        "unique_customers":     int(monthly["unique_customers"].sum()),
        "avg_order_value":      round(total_revenue / monthly["order_count"].sum(), 2),
        "best_region":          regional.iloc[0]["region"] if not regional.empty else "N/A",
        "best_region_revenue":  round(regional.iloc[0]["revenue"], 2) if not regional.empty else 0,
        "top_product":          products.iloc[0]["product"] if not products.empty else "N/A",
        "top_product_revenue":  round(products.iloc[0]["revenue"], 2) if not products.empty else 0,
        "last_month_revenue":   round(last_month, 2),
        "mom_growth_pct":       round(mom_delta, 2),
        "loyal_customers":      int(
            cohort.loc[cohort["cohort"] == "Loyal (5+)", "customers"].sum()
        ),
    }


#  Monthly trend enrichment 

def enrich_monthly_trend(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add derived columns to monthly revenue data:
    - cumulative_revenue
    - revenue_rolling3  (3-month moving average)
    - yoy_growth_pct    (year-over-year, if 12+ months available)
    """
    df = df.copy().sort_values("month").reset_index(drop=True)
    df["cumulative_revenue"] = df["revenue"].cumsum()
    df["revenue_rolling3"]   = df["revenue"].rolling(window=3, min_periods=1).mean()

    if len(df) >= 13:
        df["yoy_growth_pct"] = (
            (df["revenue"] - df["revenue"].shift(12))
            / df["revenue"].shift(12) * 100
        ).round(2)
    else:
        df["yoy_growth_pct"] = np.nan

    return df


# Category share

def add_revenue_share(df: pd.DataFrame, revenue_col: str = "revenue") -> pd.DataFrame:
    """Append a `revenue_share_pct` column (0–100) to any grouped DataFrame."""
    df = df.copy()
    total = df[revenue_col].sum()
    df["revenue_share_pct"] = (df[revenue_col] / total * 100).round(2)
    return df


#  Regional ranking 

def rank_regions(df: pd.DataFrame) -> pd.DataFrame:
    """Add rank and revenue_per_customer columns."""
    df = df.copy().sort_values("revenue", ascending=False).reset_index(drop=True)
    df["rank"]                  = df.index + 1
    df["revenue_per_customer"]  = (df["revenue"] / df["customers"]).round(2)
    return df


#  MoM growth classification 

def classify_growth(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a `growth_label` column:
      Strong growth  > +10 %
      Moderate       +2 % to +10 %
      Flat           -2 % to +2 %
      Decline        < -2 %
    """
    df = df.copy()

    def _label(pct):
        if pd.isna(pct):
            return "N/A"
        if pct > 10:
            return "Strong growth"
        if pct > 2:
            return "Moderate growth"
        if pct >= -2:
            return "Flat"
        return "Decline"

    df["growth_label"] = df["mom_growth_pct"].apply(_label)
    return df


#  Validation 

def validate_dataframe(df: pd.DataFrame, name: str, required_cols: list[str]) -> None:
    """Raise ValueError if df is empty or missing required columns."""
    if df.empty:
        raise ValueError(f"DataFrame '{name}' is empty — check your DB query.")
    missing = set(required_cols) - set(df.columns)
    if missing:
        raise ValueError(f"DataFrame '{name}' missing columns: {missing}")
    log.debug("Validated '%s': %d rows, %d cols", name, len(df), len(df.columns))
