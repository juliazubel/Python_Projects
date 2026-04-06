"""
data_cleaning.py
----------------
Handles loading, validation, and cleaning of raw financial data.

Goals:
- Missing value imputation strategy
- Outlier / anomaly detection (IQR + Z-score)
- Type coercion and schema enforcement
- Audit logging of every cleaning step
"""

import pandas as pd
import numpy as np
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------
REQUIRED_COLUMNS = ["transaction_id", "date", "category", "amount", "region", "department"]
CATEGORY_VALUES  = {"Revenue", "Expenses", "Investment", "Refund", "Transfer"}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def load_data(filepath: str | Path) -> pd.DataFrame:
    """Load CSV and enforce basic schema."""
    filepath = Path("desktop/data/transactions.csv")
    if not filepath.exists():
        raise FileNotFoundError(f"Dataset not found: {filepath}")

    df = pd.read_csv(filepath, parse_dates=["date"])
    log.info("Loaded %d rows × %d columns from '%s'", len(df), len(df.columns), filepath.name)

    _validate_schema(df)
    return df


def clean_data(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """
    Run full cleaning pipeline.

    Returns
    -------
    df_clean : cleaned DataFrame
    report   : dict with audit counts for each cleaning step
    """
    report: dict = {}
    df = df.copy()

    df, report["null_rows_removed"]   = _handle_nulls(df)
    df, report["duplicates_removed"]  = _remove_duplicates(df)
    df, report["type_fixes"]          = _fix_types(df)
    df, report["invalid_categories"]  = _filter_invalid_categories(df)
    df, report["anomalies_flagged"]   = _flag_anomalies(df)
    df                                = _add_time_features(df)

    log.info("Cleaning complete. Summary: %s", report)
    return df, report


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _validate_schema(df: pd.DataFrame) -> None:
    missing = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def _handle_nulls(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    before = len(df)
    df = df.dropna(subset=["amount"])          # drop rows without amount
    df["region"]     = df["region"].fillna("Unknown")
    df["department"] = df["department"].fillna("Unknown")
    removed = before - len(df)
    if removed:
        log.info("Removed %d rows with null 'amount'", removed)
    return df, removed


def _remove_duplicates(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    before = len(df)
    df = df.drop_duplicates(subset=["transaction_id"])
    removed = before - len(df)
    if removed:
        log.warning("Removed %d duplicate transaction IDs", removed)
    return df, removed


def _fix_types(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    fixes = 0
    if not pd.api.types.is_float_dtype(df["amount"]):
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
        fixes += 1
    if "approved" in df.columns and df["approved"].dtype != bool:
        df["approved"] = df["approved"].astype(bool)
        fixes += 1
    return df, fixes


def _filter_invalid_categories(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    mask = ~df["category"].isin(CATEGORY_VALUES)
    invalid_count = mask.sum()
    if invalid_count:
        log.warning("Removed %d rows with unknown category", invalid_count)
        df = df[~mask]
    return df, int(invalid_count)


def _flag_anomalies(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """
    Flags outliers using IQR method per category.
    Adds boolean column `is_anomaly`.
    """
    df["is_anomaly"] = False
    total_flagged = 0

    for cat, group in df.groupby("category"):
        q1, q3 = group["amount"].quantile([0.25, 0.75])
        iqr = q3 - q1
        fence_lo = q1 - 3.0 * iqr
        fence_hi = q3 + 3.0 * iqr

        mask = (df["category"] == cat) & (
            (df["amount"] < fence_lo) | (df["amount"] > fence_hi)
        )
        df.loc[mask, "is_anomaly"] = True
        flagged = mask.sum()
        total_flagged += flagged
        if flagged:
            log.info("Anomalies flagged in '%s': %d", cat, flagged)

    return df, total_flagged


def _add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """Feature engineering: extract year, month, quarter, weekday."""
    df = df.copy()
    df["year"]      = df["date"].dt.year
    df["month"]     = df["date"].dt.month
    df["quarter"]   = df["date"].dt.quarter
    df["month_name"]= df["date"].dt.strftime("%b")
    df["weekday"]   = df["date"].dt.day_name()
    df["is_weekend"]= df["date"].dt.weekday >= 5
    return df
