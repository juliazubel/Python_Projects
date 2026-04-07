"""
reporting.py
------------
Generates all charts and assembles the final PNG dashboard report.

Goals:
- Matplotlib multi-panel dashboard
- Data labelling and annotations
- Professional colour palette
- Saving publication-quality PNGs
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
from pathlib import Path

# ── Palette ───────────────────────────────────────────────────────────────────
C = {
    "primary":   "#2563EB",   
    "success":   "#16A34A",   
    "warning":   "#D97706",   
    "danger":    "#DC2626",   
    "purple":    "#7C3AED",
    "teal":      "#0D9488",
    "bg":        "#0F172A",   
    "surface":   "#1E293B",   
    "border":    "#334155",   
    "text":      "#F1F5F9",   
    "muted":     "#94A3B8",   
}

CAT_PALETTE = [C["primary"], C["success"], C["warning"], C["purple"], C["teal"], C["danger"]]


def _apply_style(fig, axes):
    fig.patch.set_facecolor(C["bg"])
    for ax in (axes if hasattr(axes, "__iter__") else [axes]):
        ax.set_facecolor(C["surface"])
        ax.tick_params(colors=C["text"], labelsize=9)
        ax.xaxis.label.set_color(C["muted"])
        ax.yaxis.label.set_color(C["muted"])
        ax.title.set_color(C["text"]) if ax.get_title() else None
        for spine in ax.spines.values():
            spine.set_color(C["border"])
        ax.grid(color=C["border"], alpha=0.5, linewidth=0.5)


def _money(x, _):
    if abs(x) >= 1_000_000:
        return f"${x/1_000_000:.1f}M"
    if abs(x) >= 1_000:
        return f"${x/1_000:.0f}K"
    return f"${x:.0f}"


# ── Individual charts ─────────────────────────────────────────────────────────

def plot_monthly_revenue(df: pd.DataFrame, ax: plt.Axes) -> None:
    months = range(len(df))
    bars   = ax.bar(months, df["revenue"], color=C["primary"], alpha=0.8, zorder=3)

    if "revenue_rolling3" in df.columns:
        ax.plot(months, df["revenue_rolling3"],
                color=C["warning"], linewidth=2, linestyle="--",
                marker="o", markersize=3, label="3-mo avg", zorder=4)
        ax.legend(fontsize=8, facecolor=C["surface"], labelcolor=C["text"],
                  framealpha=0.8)

    ax.set_xticks(list(months))
    ax.set_xticklabels(df["month"].tolist(), rotation=45, ha="right", fontsize=7)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(_money))
    ax.set_title("Monthly Revenue", fontweight="bold", pad=8)
    ax.set_ylabel("Revenue")


def plot_mom_growth(df: pd.DataFrame, ax: plt.Axes) -> None:
    valid = df.dropna(subset=["mom_growth_pct"]).copy()
    months = range(len(valid))
    colors = [C["success"] if v >= 0 else C["danger"]
              for v in valid["mom_growth_pct"]]

    ax.bar(months, valid["mom_growth_pct"], color=colors, alpha=0.85, zorder=3)
    ax.axhline(0, color=C["text"], linewidth=0.7, linestyle=":")
    ax.set_xticks(list(months))
    ax.set_xticklabels(valid["month"].tolist(), rotation=45, ha="right", fontsize=7)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.1f}%"))
    ax.set_title("Month-over-Month Growth", fontweight="bold", pad=8)
    ax.set_ylabel("Growth %")


def plot_category_bars(df: pd.DataFrame, ax: plt.Axes) -> None:
    cats   = df["category"].tolist()
    rev    = df["revenue"].tolist()
    colors = CAT_PALETTE[:len(cats)]

    bars = ax.barh(cats, rev, color=colors, alpha=0.85, zorder=3)
    for bar, val in zip(bars, rev):
        ax.text(bar.get_width() * 1.01, bar.get_y() + bar.get_height() / 2,
                _money(val, None), va="center", fontsize=8, color=C["text"])

    ax.xaxis.set_major_formatter(mticker.FuncFormatter(_money))
    ax.set_title("Revenue by Category", fontweight="bold", pad=8)
    ax.set_xlabel("Revenue")
    ax.invert_yaxis()


def plot_channel_donut(df: pd.DataFrame, ax: plt.Axes) -> None:
    wedges, texts, autotexts = ax.pie(
        df["revenue"],
        labels=df["channel"].tolist(),
        colors=CAT_PALETTE[:len(df)],
        autopct="%1.1f%%",
        startangle=140,
        wedgeprops=dict(width=0.55, edgecolor=C["bg"], linewidth=1.5),
        pctdistance=0.75,
    )
    for t in texts + autotexts:
        t.set_color(C["text"])
        t.set_fontsize(9)
    ax.set_title("Revenue by Channel", fontweight="bold", pad=8)
    ax.set_facecolor(C["bg"])


def plot_regional_bars(df: pd.DataFrame, ax: plt.Axes) -> None:
    colors = CAT_PALETTE[:len(df)]
    bars = ax.bar(df["region"].tolist(), df["revenue"].tolist(),
                  color=colors, alpha=0.85, zorder=3)
    for bar, val in zip(bars, df["revenue"]):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() * 1.01,
                _money(val, None), ha="center", fontsize=8, color=C["text"])

    ax.yaxis.set_major_formatter(mticker.FuncFormatter(_money))
    ax.set_title("Revenue by Region", fontweight="bold", pad=8)
    ax.set_ylabel("Revenue")


def plot_top_products(df: pd.DataFrame, ax: plt.Axes) -> None:
    top    = df.head(8)
    colors = [CAT_PALETTE[i % len(CAT_PALETTE)] for i in range(len(top))]

    bars = ax.barh(top["product"].tolist(), top["revenue"].tolist(),
                   color=colors, alpha=0.85, zorder=3)
    for bar, val in zip(bars, top["revenue"]):
        ax.text(bar.get_width() * 1.01, bar.get_y() + bar.get_height() / 2,
                _money(val, None), va="center", fontsize=8, color=C["text"])

    ax.xaxis.set_major_formatter(mticker.FuncFormatter(_money))
    ax.set_title("Top Products by Revenue", fontweight="bold", pad=8)
    ax.set_xlabel("Revenue")
    ax.invert_yaxis()


# ── Master dashboard ──────────────────────────────────────────────────────────

def generate_dashboard(
    monthly:   pd.DataFrame,
    mom:       pd.DataFrame,
    categories: pd.DataFrame,
    channels:  pd.DataFrame,
    regional:  pd.DataFrame,
    products:  pd.DataFrame,
    kpis:      dict,
    output_path: str | Path = "reports/dashboard.png",
) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig = plt.figure(figsize=(22, 15))
    fig.patch.set_facecolor(C["bg"])

    # ── Header ────────────────────────────────────────────────────────────────
    fig.text(0.5, 0.975, "SQL Data Automation — Business Intelligence Dashboard",
             ha="center", va="top", fontsize=18, fontweight="bold", color=C["text"])

    kpi_str = (
        f"Total Revenue: ${kpis['total_revenue']:,.0f}  ·  "
        f"Orders: {kpis['total_orders']:,}  ·  "
        f"Avg Order Value: ${kpis['avg_order_value']:,.2f}  ·  "
        f"Last Month: ${kpis['last_month_revenue']:,.0f}  ·  "
        f"MoM: {kpis['mom_growth_pct']:+.1f}%  ·  "
        f"Top Region: {kpis['best_region']}"
    )
    fig.text(0.5, 0.945, kpi_str, ha="center", va="top", fontsize=10,
             color=C["primary"], fontfamily="monospace",
             bbox=dict(boxstyle="round,pad=0.4", facecolor=C["surface"],
                       edgecolor=C["border"], alpha=0.9))

    # ── Grid ──────────────────────────────────────────────────────────────────
    gs = gridspec.GridSpec(3, 3, figure=fig,
                           top=0.92, bottom=0.06,
                           left=0.05, right=0.97,
                           hspace=0.55, wspace=0.30)

    ax1 = fig.add_subplot(gs[0, :2])   # monthly revenue (wide)
    ax2 = fig.add_subplot(gs[0,  2])   # channel donut
    ax3 = fig.add_subplot(gs[1,  0])   # MoM growth
    ax4 = fig.add_subplot(gs[1,  1])   # category bars
    ax5 = fig.add_subplot(gs[1,  2])   # regional bars
    ax6 = fig.add_subplot(gs[2, :])    # top products (full width)

    plot_monthly_revenue(monthly, ax1)
    plot_channel_donut(channels, ax2)
    plot_mom_growth(mom, ax3)
    plot_category_bars(categories, ax4)
    plot_regional_bars(regional, ax5)
    plot_top_products(products, ax6)

    _apply_style(fig, [ax1, ax2, ax3, ax4, ax5, ax6])

    fig.savefig(output_path, dpi=150, bbox_inches="tight", facecolor=C["bg"])
    plt.close("all")
    print(f"✓ Dashboard saved → {output_path}")
    return output_path


# ── Text summary report ───────────────────────────────────────────────────────

def save_text_report(kpis: dict, output_path: str | Path = "reports/summary.txt") -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "=" * 60,
        "  SQL DATA AUTOMATION — EXECUTIVE SUMMARY",
        "=" * 60,
        "",
        "  REVENUE",
        f"    Total revenue       : ${kpis['total_revenue']:>12,.2f}",
        f"    Last month          : ${kpis['last_month_revenue']:>12,.2f}",
        f"    MoM growth          : {kpis['mom_growth_pct']:>+11.2f}%",
        "",
        "  ORDERS & CUSTOMERS",
        f"    Total orders        : {kpis['total_orders']:>12,}",
        f"    Unique customers    : {kpis['unique_customers']:>12,}",
        f"    Avg order value     : ${kpis['avg_order_value']:>12,.2f}",
        f"    Loyal customers (5+): {kpis['loyal_customers']:>12,}",
        "",
        "  TOP PERFORMERS",
        f"    Best region         : {kpis['best_region']}",
        f"    Best region revenue : ${kpis['best_region_revenue']:>12,.2f}",
        f"    Top product         : {kpis['top_product']}",
        f"    Top product revenue : ${kpis['top_product_revenue']:>12,.2f}",
        "",
        "=" * 60,
    ]
    output_path.write_text("\n".join(lines))
    print(f"✓ Text report saved → {output_path}")
