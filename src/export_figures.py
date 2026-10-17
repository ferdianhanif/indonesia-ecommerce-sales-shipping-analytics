"""
High-Resolution Analytical Visualizations for Indonesia E-Commerce Study
Optimized for high legibility, large labels, and crisp executive presentation.
Author: Ferdian Hanif
Email: ferdianhanif001@gmail.com
"""

import os
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from metrics import (
    get_connection,
    get_monthly_runrate,
    get_payment_cancellation_analysis,
    get_regional_logistics_disparity,
    get_logistics_cost_structure
)

OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "reports", "figures"))
os.makedirs(OUTPUT_DIR, exist_ok=True)

# High-contrast, large-font typography
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Segoe UI", "DejaVu Sans", "Arial"],
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.labelweight": "bold",
    "axes.titlesize": 13,
    "axes.titleweight": "bold",
    "xtick.labelsize": 10.5,
    "ytick.labelsize": 10.5,
    "figure.titlesize": 14,
    "figure.titleweight": "bold",
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "axes.edgecolor": "#CBD5E1",
    "axes.linewidth": 1.2,
    "grid.color": "#F1F5F9",
    "grid.linestyle": "--",
    "grid.alpha": 0.9,
})

def plot_monthly_trend(conn):
    """Figure 1: Monthly sales volume and revenue trend (2023-2025)."""
    df = get_monthly_runrate(conn)

    fig, ax1 = plt.subplots(figsize=(7.8, 5.2), facecolor="#FFFFFF")
    ax1.set_facecolor("#FFFFFF")

    x = np.arange(len(df))
    # Simplify x-axis labels: show every 3 months
    labels = [ym[2:] if i % 2 == 0 or i == len(df)-1 else "" for i, ym in enumerate(df["year_month"])]

    color1 = "#2563EB"
    color2 = "#059669"

    # Bar chart for Order Volume
    bars = ax1.bar(x, df["total_orders"], width=0.6, color=color1, alpha=0.85, label="Volume Pesanan (Order)")
    ax1.set_ylabel("Volume Pesanan per Bulan", color=color1, labelpad=8)
    ax1.tick_params(axis="y", labelcolor=color1)
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, rotation=45, ha="right", fontweight="bold")
    ax1.set_xlabel("Periode Transaksi (Tahun-Bulan)", labelpad=8)

    # Line chart for Revenue
    ax2 = ax1.twinx()
    line = ax2.plot(x, df["revenue_million_idr"], color=color2, marker="o", linewidth=2.5, markersize=5, label="Nilai Transaksi (Juta Rp)")
    ax2.set_ylabel("Nilai Transaksi (Juta Rp)", color=color2, labelpad=8)
    ax2.tick_params(axis="y", labelcolor=color2)
    ax2.grid(False)

    # Annotate peak
    peak_idx = df["total_orders"].idxmax()
    peak_val = df.loc[peak_idx, "total_orders"]
    ax1.annotate(f"Puncak: {peak_val:,} Pesanan",
                 xy=(peak_idx, peak_val), xytext=(peak_idx - 5, peak_val + 70),
                 arrowprops=dict(facecolor="#DC2626", shrink=0.08, width=1.5, headwidth=6),
                 fontsize=10, fontweight="bold", color="#DC2626")

    ax1.set_title("Tren Volume Pesanan & Nilai Transaksi Bulanan (2023 - 2025)", pad=12)
    ax1.spines["top"].set_visible(False)
    ax2.spines["top"].set_visible(False)

    plt.tight_layout()
    output_path = os.path.join(OUTPUT_DIR, "fig1_monthly_sales_trend.png")
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_path}")

def plot_payment_cancellation_risk(conn):
    """Figure 2: Transaction share vs cancellation rate per payment method."""
    df = get_payment_cancellation_analysis(conn)
    df = df[df["payment_group"] != "Lainnya"].sort_values("total_orders", ascending=True)

    fig, ax = plt.subplots(figsize=(7.8, 5.2), facecolor="#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    y = np.arange(len(df))
    height = 0.35

    bars1 = ax.barh(y + height/2, df["order_share_pct"], height, label="Pangsa Pesanan (%)", color="#94A3B8")
    bars2 = ax.barh(y - height/2, df["cancellation_rate_pct"], height, label="Tingkat Pembatalan (%)", color="#DC2626")

    ax.set_yticks(y)
    ax.set_yticklabels(df["payment_group"], fontweight="bold", fontsize=10.5)
    ax.set_xlabel("Persentase (%)", labelpad=8)
    ax.set_title("Pangsa Transaksi vs Tingkat Pembatalan per Metode Bayar", pad=12)
    ax.legend(loc="upper right", bbox_to_anchor=(0.98, 0.42), frameon=True, facecolor="#F8FAFC", edgecolor="#CBD5E1", fontsize=10)
    ax.grid(axis="x", visible=True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    for bar in bars1:
        width = bar.get_width()
        if width > 3:
            ax.text(width + 0.8, bar.get_y() + bar.get_height()/2, f"{width:.1f}%",
                    va="center", ha="left", fontsize=10, fontweight="bold", color="#475569")

    for bar in bars2:
        width = bar.get_width()
        ax.text(width + 0.8, bar.get_y() + bar.get_height()/2, f"{width:.1f}%",
                    va="center", ha="left", fontsize=10, fontweight="bold", color="#991B1B")

    ax.set_xlim(0, 72)
    plt.tight_layout()
    output_path = os.path.join(OUTPUT_DIR, "fig2_payment_method_cancellation_risk.png")
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_path}")

def plot_regional_shipping_disparity(conn):
    """Figure 3: Java vs Outer Islands Shipping Cost Disparity."""
    df = get_regional_logistics_disparity(conn)

    fig, ax1 = plt.subplots(figsize=(8.0, 4.0), facecolor="#FFFFFF")
    ax1.set_facecolor("#FFFFFF")

    x = np.arange(len(df))
    width = 0.38

    color1 = "#2563EB"
    color2 = "#D97706"

    # Bar chart for Shipping Cost
    bars = ax1.bar(x - width/2, df["avg_shipping_cost_idr"] / 1000, width=width, color=color1, label="Rata-rata Ongkir (Ribu Rp)")
    ax1.set_ylabel("Rata-rata Ongkir (Ribu Rp)", color=color1, labelpad=8)
    ax1.tick_params(axis="y", labelcolor=color1)
    ax1.set_xticks(x)
    ax1.set_xticklabels(df["region_group"], fontweight="bold", fontsize=11)

    for bar in bars:
        h = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, h + 1.0, f"Rp {h:.1f}rb",
                 ha="center", va="bottom", fontsize=10, fontweight="bold", color=color1)

    # Bar chart for Cancellation Rate
    ax2 = ax1.twinx()
    bars2 = ax2.bar(x + width/2, df["cancellation_rate_pct"], width=width, color=color2, label="Tingkat Pembatalan (%)")
    ax2.set_ylabel("Tingkat Pembatalan (%)", color=color2, labelpad=8)
    ax2.tick_params(axis="y", labelcolor=color2)
    ax2.grid(False)

    for bar in bars2:
        h = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, h + 0.6, f"{h:.1f}%",
                 ha="center", va="bottom", fontsize=10, fontweight="bold", color=color2)

    ax1.set_ylim(0, 48)
    ax2.set_ylim(0, 26)
    ax1.set_title("Disparitas Biaya Ongkos Kirim & Tingkat Pembatalan Antarwilayah", pad=10)
    ax1.spines["top"].set_visible(False)
    ax2.spines["top"].set_visible(False)

    plt.tight_layout()
    output_path = os.path.join(OUTPUT_DIR, "fig3_regional_shipping_cost_and_cancellation.png")
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_path}")

def plot_logistics_subsidy_structure(conn):
    """Figure 4: Shipping Cost Burden Breakdown (Buyer vs Subsidy vs Gap)."""
    df = get_logistics_cost_structure(conn)
    actual = df.loc[0, "total_actual_cost_million"]
    buyer = df.loc[0, "total_buyer_paid_million"]
    subsidy = df.loc[0, "total_subsidy_million"]
    gap = max(0, actual - (buyer + subsidy))

    fig, ax = plt.subplots(figsize=(8.0, 4.0), facecolor="#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    categories = ["Total Biaya Riil Logistik", "Alokasi Pembebanan Biaya"]
    
    # 100% breakdown
    buyer_pct = (buyer / actual) * 100
    subsidy_pct = (subsidy / actual) * 100
    gap_pct = (gap / actual) * 100

    ax.barh([1], [subsidy], color="#059669", height=0.45, label=f"Subsidi Platform: Rp {subsidy:.1f} Jt ({subsidy_pct:.1f}%)")
    ax.barh([1], [buyer], left=[subsidy], color="#2563EB", height=0.45, label=f"Dibayar Pembeli: Rp {buyer:.1f} Jt ({buyer_pct:.1f}%)")
    ax.barh([1], [gap], left=[subsidy + buyer], color="#D97706", height=0.45, label=f"Selisih Beban Toko: Rp {gap:.1f} Jt ({gap_pct:.1f}%)")

    ax.barh([0], [actual], color="#64748B", height=0.45, label=f"Total Tagihan Kurir: Rp {actual:.1f} Juta (100%)")

    ax.set_yticks([0, 1])
    ax.set_yticklabels(["Biaya Riil", "Komponen Beban"], fontweight="bold", fontsize=11)
    ax.set_xlabel("Nilai Akumulasi Logistik (Juta Rp)", labelpad=8)
    ax.set_title("Struktur Pembebanan Biaya Logistik: Pembeli vs Subsidi Platform", pad=10)
    ax.legend(loc="lower right", frameon=True, facecolor="#F8FAFC", edgecolor="#CBD5E1", fontsize=9.5)
    ax.grid(axis="x", visible=True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()
    output_path = os.path.join(OUTPUT_DIR, "fig4_logistics_cost_structure_and_subsidy.png")
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_path}")

def main():
    conn = get_connection()
    print("Exporting high-resolution analytical figures for e-commerce study...")
    plot_monthly_trend(conn)
    plot_payment_cancellation_risk(conn)
    plot_regional_shipping_disparity(conn)
    plot_logistics_subsidy_structure(conn)
    conn.close()
    print("All figures successfully exported.")

if __name__ == "__main__":
    main()
