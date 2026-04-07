"""
db_connection.py
----------------
Database abstraction layer.

Goals:
- Context-manager pattern (with statement)
- Support for both SQLite (dev) and PostgreSQL (prod)
- Parameterised queries — no string interpolation → no SQL injection
- Query timing for performance monitoring
- Row-factory so results come back as dicts, not plain tuples
"""

import sqlite3
import time
import logging
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Generator

import pandas as pd

log = logging.getLogger(__name__)

# ── Optional PostgreSQL support (psycopg2) ────────────────────────────────────
try:
    import psycopg2
    import psycopg2.extras
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False


DEFAULT_SQLITE_PATH = Path(__file__).parent.parent / "database" / "sample.db"


# ── Connection helpers ────────────────────────────────────────────────────────

def _sqlite_row_factory(cursor, row) -> dict:
    """Convert SQLite rows to dicts keyed by column name."""
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}


@contextmanager
def get_sqlite_connection(
    db_path: str | Path = DEFAULT_SQLITE_PATH,
) -> Generator[sqlite3.Connection, None, None]:
    """
    Yield an open SQLite connection; auto-close on exit.

    Usage:
        with get_sqlite_connection() as conn:
            df = query_to_df(conn, "SELECT * FROM orders")
    """
    db_path = Path(db_path)
    if not db_path.exists():
        raise FileNotFoundError(
            f"Database not found: {db_path}\n"
            "Run: python database/seed.py"
        )
    conn = sqlite3.connect(db_path)
    conn.row_factory = _sqlite_row_factory
    conn.execute("PRAGMA foreign_keys = ON")
    log.debug("SQLite connection opened: %s", db_path.name)
    try:
        yield conn
    finally:
        conn.close()
        log.debug("SQLite connection closed")


@contextmanager
def get_postgres_connection(
    host: str,
    port: int,
    dbname: str,
    user: str,
    password: str,
):
    """
    Yield a psycopg2 connection with RealDictCursor (rows → dicts).

    Usage:
        with get_postgres_connection(**pg_cfg) as conn:
            df = query_to_df(conn, "SELECT * FROM orders")
    """
    if not PSYCOPG2_AVAILABLE:
        raise ImportError("psycopg2 not installed. Run: pip install psycopg2-binary")

    conn = psycopg2.connect(
        host=host, port=port, dbname=dbname,
        user=user, password=password,
        cursor_factory=psycopg2.extras.RealDictCursor,
    )
    log.debug("PostgreSQL connection opened: %s@%s/%s", user, host, dbname)
    try:
        yield conn
    finally:
        conn.close()
        log.debug("PostgreSQL connection closed")


# ── Query runners ─────────────────────────────────────────────────────────────

def execute_query(
    conn,
    sql: str,
    params: tuple | dict | None = None,
) -> list[dict]:
    """
    Execute a SELECT query and return list of row-dicts.

    Parameters
    ----------
    conn   : open connection (SQLite or psycopg2)
    sql    : SQL string — use ? (SQLite) or %s (psycopg2) for parameters
    params : positional tuple or named dict of bind parameters
    """
    t0 = time.perf_counter()
    cur = conn.cursor()
    cur.execute(sql, params or ())
    rows = cur.fetchall()

    # psycopg2 RealDictRow → plain dict
    if rows and not isinstance(rows[0], dict):
        cols = [d[0] for d in cur.description]
        rows = [dict(zip(cols, r)) for r in rows]

    elapsed = (time.perf_counter() - t0) * 1000
    log.debug("Query returned %d rows in %.1f ms", len(rows), elapsed)
    return rows


def query_to_df(
    conn,
    sql: str,
    params: tuple | dict | None = None,
) -> pd.DataFrame:
    """
    Execute a query and load results directly into a pandas DataFrame.
    This is the primary function used by analysis.py.
    """
    rows = execute_query(conn, sql, params)
    return pd.DataFrame(rows)


def execute_many(
    conn,
    sql: str,
    data: list[tuple],
) -> int:
    """
    Bulk-insert/update with executemany.
    Returns the number of affected rows.
    """
    cur = conn.cursor()
    cur.executemany(sql, data)
    conn.commit()
    log.info("executemany: %d rows affected", cur.rowcount)
    return cur.rowcount


# ── Health check ──────────────────────────────────────────────────────────────

def ping(conn) -> bool:
    """Return True if the connection is alive."""
    try:
        execute_query(conn, "SELECT 1 AS ok")
        return True
    except Exception as exc:
        log.error("DB ping failed: %s", exc)
        return False


def get_table_info(conn) -> pd.DataFrame:
    """Return a DataFrame with row counts for every table."""
    # Works for SQLite; for PostgreSQL swap the SQL below
    tables = execute_query(
        conn,
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name",
    )
    rows = []
    for t in tables:
        name = t["name"]
        count = execute_query(conn, f"SELECT COUNT(*) AS n FROM {name}")[0]["n"]
        rows.append({"table": name, "row_count": count})
    return pd.DataFrame(rows)
