"""
visualization.py
----------------
Generates all charts and saves a multi-page PDF report.

Skills demonstrated:
- Matplotlib subplots with custom styling
- Seaborn heatmaps / bar charts
- Annotated anomaly scatter plot
- Professional color palette & typography
"""

import matplotlib
matplotlib.use("Agg")           # headless rendering (no display needed)
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
from pathlib import Path

#  Palette 
COLORS = {
    "revenue":  "#2ecc71",
    "expenses": "#e74c3c",
    "net":      "#3498db",
    "rolling":  "#f39c12",
    "anomaly":  "#e74c3c",
    "normal":   "#95a5a6",
    "accent":   "#8e44ad",
    "bg":       "#0f1117",
    "surface":  "#1a1d2e",
    "text":     "#ecf0f1",
    "grid":     "#2c3e50",
}

CAT_COLORS = ["#2ecc71","#e74c3c","#3498db","#f39c12","#8e44ad"]

def _apply_dark_style(fig, axes):
    fig.patch.set_facecolor(COLORS["bg"])
    for ax in (axes if hasattr(axes, "__iter__") else [axes]):
        ax.set_facecolor(COLORS["surface"])
        ax.tick_params(colors=COLORS["text"], labelsize=9)
        ax.xaxis.label.set_color(COLORS["text"])
        ax.yaxis.label.set_color(COLORS["text"])
        if ax.get_title():
            ax.title.set_color(COLORS["text"])
        ax.spines[:].set_color(COLORS["grid"])
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))


#  Individual Charts 

def plot_monthly_trend(trend: pd.DataFrame, ax: plt.Axes) -> None:
    """Revenue bars + expense bars + rolling average line."""
    months = range(len(trend))
    w = 0.35

    bars_rev = ax.bar([m - w/2 for m in months], trend["revenue"],
                      width=w, color=COLORS["revenue"], alpha=0.85, label="Revenue", zorder=3)
    bars_exp = ax.bar([m + w/2 for m in months], trend["expenses"],
                      width=w, color=COLORS["expenses"], alpha=0.85, label="Expenses", zorder=3)

    if "revenue_rolling3" in trend.columns:
        ax.plot(months, trend["revenue_rolling3"], color=COLORS["rolling"],
                linewidth=2, linestyle="--", marker="o", markersize=4,
                label="3-month rolling avg", zorder=4)

    ax.set_xticks(list(months))
    ax.set_xticklabels(
        trend["month"].dt.strftime("%b %Y") if hasattr(trend["month"], "dt") else trend["month"],
        rotation=45, ha="right", fontsize=8
    )
    ax.set_title("Monthly Revenue vs Expenses", fontweight="bold", pad=10)
    ax.set_ylabel("Amount (USD)")
    ax.legend(fontsize=8, facecolor=COLORS["surface"], labelcolor=COLORS["text"],
               framealpha=0.8, loc="upper left")
    ax.grid(axis="y", color=COLORS["grid"], alpha=0.5, zorder=0)


def plot_net_cashflow(trend: pd.DataFrame, ax: plt.Axes) -> None:
    """Cumulative net cash flow with +/- fill."""
    months = range(len(trend))
    net = trend["cumulative_net"]

    ax.plot(months, net, color=COLORS["net"], linewidth=2.5, zorder=3)
    ax.fill_between(months, net, 0,
                    where=(net >= 0), alpha=0.25, color=COLORS["revenue"], label="Positive", zorder=2)
    ax.fill_between(months, net, 0,
                    where=(net < 0), alpha=0.25, color=COLORS["expenses"], label="Negative", zorder=2)

    ax.set_xticks(list(months))
    ax.set_xticklabels(
        trend["month"].dt.strftime("%b %Y") if hasattr(trend["month"], "dt") else trend["month"],
        rotation=45, ha="right", fontsize=8
    )
    ax.axhline(0, color=COLORS["text"], linewidth=0.8, linestyle=":")
    ax.set_title("Cumulative Net Cash Flow", fontweight="bold", pad=10)
    ax.set_ylabel("Cumulative USD")
    ax.legend(fontsize=8, facecolor=COLORS["surface"], labelcolor=COLORS["text"], framealpha=0.8)
    ax.grid(axis="y", color=COLORS["grid"], alpha=0.5, zorder=0)


def plot_category_pie(cat_df: pd.DataFrame, ax: plt.Axes) -> None:
    """Donut chart of transaction volume by category (absolute amounts)."""
    labels = cat_df["category"].tolist()
    sizes  = cat_df["count"].tolist()

    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, colors=CAT_COLORS,
        autopct="%1.1f%%", startangle=140,
        wedgeprops=dict(width=0.55, edgecolor=COLORS["bg"], linewidth=1.5),
        pctdistance=0.75,
    )
    for t in texts + autotexts:
        t.set_color(COLORS["text"])
        t.set_fontsize(9)

    ax.set_title("Transaction Count by Category", fontweight="bold", pad=10)


def plot_anomaly_scatter(df: pd.DataFrame, ax: plt.Axes) -> None:
    """Scatter: date × amount, anomalies highlighted in red."""
    normal  = df[~df["is_anomaly"]]
    anomaly = df[df["is_anomaly"]]

    ax.scatter(normal["date"],  normal["amount"],
               s=8, alpha=0.35, color=COLORS["normal"], label=f"Normal ({len(normal):,})", zorder=2)
    ax.scatter(anomaly["date"], anomaly["amount"],
               s=40, alpha=0.9, color=COLORS["anomaly"],
               edgecolors="white", linewidths=0.5,
               label=f"Anomaly ({len(anomaly):,})", zorder=3)

    ax.axhline(df["amount"].mean(), color=COLORS["net"],
               linestyle="--", linewidth=1, label="Mean", alpha=0.7)

    ax.set_title("Anomaly Detection — All Transactions", fontweight="bold", pad=10)
    ax.set_ylabel("Amount (USD)")
    ax.legend(fontsize=8, facecolor=COLORS["surface"], labelcolor=COLORS["text"], framealpha=0.8)
    ax.grid(color=COLORS["grid"], alpha=0.4, zorder=0)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))


def plot_regional_bar(regional_df: pd.DataFrame, ax: plt.Axes) -> None:
    """Horizontal bar chart of total volume per region."""
    if "region" not in regional_df.columns or "total_volume" not in regional_df.columns:
        ax.set_visible(False)
        return

    data = regional_df.sort_values("total_volume", ascending=True)
    colors = [CAT_COLORS[i % len(CAT_COLORS)] for i in range(len(data))]

    bars = ax.barh(data["region"], data["total_volume"],
                   color=colors, alpha=0.85, edgecolor=COLORS["bg"])

    for bar, val in zip(bars, data["total_volume"]):
        ax.text(bar.get_width() * 1.01, bar.get_y() + bar.get_height() / 2,
                f"${val:,.0f}", va="center", fontsize=8, color=COLORS["text"])

    ax.set_title("Transaction Volume by Region", fontweight="bold", pad=10)
    ax.set_xlabel("Total Volume (USD)")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    ax.grid(axis="x", color=COLORS["grid"], alpha=0.5, zorder=0)


def plot_mom_growth(trend: pd.DataFrame, ax: plt.Axes) -> None:
    """Month-over-month revenue growth bar chart."""
    growth = trend.dropna(subset=["revenue_mom_pct"])
    months = range(len(growth))
    colors = [COLORS["revenue"] if v >= 0 else COLORS["expenses"]
              for v in growth["revenue_mom_pct"]]

    ax.bar(months, growth["revenue_mom_pct"], color=colors, alpha=0.85, zorder=3)
    ax.axhline(0, color=COLORS["text"], linewidth=0.8)
    ax.set_xticks(list(months))
    ax.set_xticklabels(
        growth["month"].dt.strftime("%b %Y") if hasattr(growth["month"], "dt") else growth["month"],
        rotation=45, ha="right", fontsize=8
    )
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.1f}%"))
    ax.set_title("Month-over-Month Revenue Growth (%)", fontweight="bold", pad=10)
    ax.set_ylabel("Growth %")
    ax.grid(axis="y", color=COLORS["grid"], alpha=0.5, zorder=0)


#  Master Report 

def generate_report(
    df: pd.DataFrame,
    trend: pd.DataFrame,
    cat_df: pd.DataFrame,
    regional_df: pd.DataFrame,
    kpis: dict,
    output_path: str | Path = "report/results.png",
) -> None:
    """Render a 3×2 dashboard and save to PNG (and PDF)."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig = plt.figure(figsize=(20, 14))
    fig.patch.set_facecolor(COLORS["bg"])

    #  Title banner 
    fig.text(0.5, 0.97, "Financial Data Analysis Pipeline",
             ha="center", va="top", fontsize=20, fontweight="bold",
             color=COLORS["text"], fontfamily="monospace")

    kpi_text = (
        f"  Transactions: {kpis['total_transactions']:,}   |   "
        f"Revenue: ${kpis['total_revenue']:,.0f}   |   "
        f"Expenses: ${abs(kpis['total_expenses']):,.0f}   |   "
        f"Net: ${kpis['net_cashflow']:,.0f}   |   "
        f"Anomalies: {kpis['anomaly_count']} ({kpis['anomaly_pct']}%)  "
    )
    fig.text(0.5, 0.935, kpi_text, ha="center", va="top", fontsize=10,
             color=COLORS["net"], fontfamily="monospace",
             bbox=dict(boxstyle="round,pad=0.4", facecolor=COLORS["surface"],
                       edgecolor=COLORS["grid"], alpha=0.9))

    #  Grid 
    gs = gridspec.GridSpec(3, 2, figure=fig,
                           top=0.91, bottom=0.06,
                           left=0.06, right=0.97,
                           hspace=0.55, wspace=0.30)

    ax1 = fig.add_subplot(gs[0, :])    # full-width: monthly trend
    ax2 = fig.add_subplot(gs[1, 0])    # net cashflow
    ax3 = fig.add_subplot(gs[1, 1])    # category donut
    ax4 = fig.add_subplot(gs[2, 0])    # anomaly scatter
    ax5 = fig.add_subplot(gs[2, 1])    # regional bar

    all_axes = [ax1, ax2, ax3, ax4, ax5]

    plot_monthly_trend(trend, ax1)
    plot_net_cashflow(trend, ax2)
    plot_category_pie(cat_df, ax3)
    plot_anomaly_scatter(df, ax4)
    plot_regional_bar(regional_df, ax5)

    _apply_dark_style(fig, all_axes)

    # Donut center label override
    ax3.set_facecolor(COLORS["bg"])

    fig.savefig(output_path, dpi=150, bbox_inches="tight",
                facecolor=COLORS["bg"])

    # Also save MoM growth chart separately
    fig2, ax_mom = plt.subplots(figsize=(14, 4))
    fig2.patch.set_facecolor(COLORS["bg"])
    plot_mom_growth(trend, ax_mom)
    _apply_dark_style(fig2, [ax_mom])
    mom_path = output_path.parent / "mom_growth.png"
    fig2.savefig(mom_path, dpi=150, bbox_inches="tight", facecolor=COLORS["bg"])

    plt.close("all")
    print(f"✓ Dashboard saved  → {output_path}")
    print(f"✓ MoM growth chart → {mom_path}")
