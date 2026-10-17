"""
Exploratory Data Audit for Indonesia E-Commerce Sales & Shipping 2023-2025
Author: Ferdian Hanif
Email: ferdianhanif001@gmail.com
"""

import os
import pandas as pd
import numpy as np

RAW_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "ecommerce_sales_shipping.csv")

def audit():
    df = pd.read_csv(RAW_PATH, sep=";", encoding="utf-8-sig", low_memory=False)
    print("=== DATASET OVERVIEW ===")
    print(f"Total Rows: {len(df):,}")
    print(f"Total Columns: {len(df.columns)}")
    print("Columns:", df.columns.tolist())

    # Order Status
    print("\n=== STATUS PESANAN ===")
    print(df["Status Pesanan"].value_counts())

    # Payment Methods
    print("\n=== METODE PEMBAYARAN ===")
    df["is_cancelled"] = df["Status Pesanan"].str.lower().str.contains("batal").astype(int)
    pm = df.groupby("Metode Pembayaran").agg(
        total_orders=("order_id", "count"),
        cancelled_orders=("is_cancelled", "sum"),
        total_revenue=("Total Pembayaran", "sum")
    ).reset_index()
    pm["cancellation_rate_pct"] = (pm["cancelled_orders"] / pm["total_orders"]) * 100
    pm["order_share_pct"] = (pm["total_orders"] / len(df)) * 100
    pm = pm.sort_values("total_orders", ascending=False)
    print(pm.to_string(index=False))

    # Shipping & Logistics Economics
    print("\n=== LOGISTIK & SUBSIDI ONGKIR ===")
    total_buyer_ship = df["Ongkos Kirim Dibayar oleh Pembeli"].sum()
    total_subsidy = df["Estimasi Potongan Biaya Pengiriman"].sum()
    total_actual_cost = df["Perkiraan Ongkos Kirim"].sum()
    zero_ship_orders = (df["Ongkos Kirim Dibayar oleh Pembeli"] == 0).sum()
    print(f"Pesanan dengan Gratis Ongkir Penuh (Pembeli Bayar Rp 0): {zero_ship_orders:,} ({(zero_ship_orders/len(df))*100:.1f}%)")
    print(f"Total Ongkos Kirim Dibayar Pembeli: Rp {total_buyer_ship:,.0f}")
    print(f"Total Subsidi Potongan Pengiriman: Rp {total_subsidy:,.0f}")
    print(f"Total Perkiraan Biaya Riil Logistik: Rp {total_actual_cost:,.0f}")
    print(f"Rasio Subsidi terhadap Total Biaya Logistik: {(total_subsidy/total_actual_cost)*100:.1f}%")

    # Regional Distribution (Jawa vs Luar Jawa)
    print("\n=== DISTRIBUSI REGIONAL (PROVINSI) ===")
    jawa_provinces = ["DKI JAKARTA", "JAWA BARAT", "JAWA TENGAH", "JAWA TIMUR", "BANTEN", "DI YOGYAKARTA"]
    df["is_jawa"] = df["Provinsi"].str.upper().apply(lambda x: "Pulau Jawa" if any(p in str(x) for p in jawa_provinces) else "Luar Pulau Jawa")
    reg = df.groupby("is_jawa").agg(
        total_orders=("order_id", "count"),
        total_revenue=("Total Pembayaran", "sum"),
        avg_shipping_cost=("Perkiraan Ongkos Kirim", "mean"),
        avg_weight_gr=("total_weight_gr", "mean"),
        cancellation_rate=("is_cancelled", "mean")
    ).reset_index()
    reg["cancellation_rate"] = reg["cancellation_rate"] * 100
    reg["revenue_share_pct"] = (reg["total_revenue"] / df["Total Pembayaran"].sum()) * 100
    print(reg.to_string(index=False))

    # Product Categories
    print("\n=== TOP 10 KATEGORI PRODUK ===")
    cat = df.groupby("product_categories").agg(
        total_orders=("order_id", "count"),
        total_qty=("total_qty", "sum"),
        total_revenue=("Total Pembayaran", "sum")
    ).reset_index().sort_values("total_orders", ascending=False).head(10)
    print(cat.to_string(index=False))

    # Shipping Couriers
    print("\n=== KINERJA KURIR PENGIRIMAN ===")
    # Extract courier family
    def clean_courier(val):
        val = str(val)
        if "SPX" in val:
            return "Shopee Xpress (SPX)"
        elif "J&T" in val:
            return "J&T Express"
        elif "JNE" in val:
            return "JNE Express"
        elif "SiCepat" in val:
            return "SiCepat"
        elif "Anteraja" in val:
            return "Anteraja"
        else:
            return "Lainnya"

    df["courier_group"] = df["Opsi Pengiriman"].apply(clean_courier)
    cr = df.groupby("courier_group").agg(
        total_orders=("order_id", "count"),
        cancellation_rate=("is_cancelled", "mean"),
        avg_shipping_cost=("Perkiraan Ongkos Kirim", "mean"),
        total_revenue=("Total Pembayaran", "sum")
    ).reset_index()
    cr["cancellation_rate"] = cr["cancellation_rate"] * 100
    cr["share_pct"] = (cr["total_orders"] / len(df)) * 100
    cr = cr.sort_values("total_orders", ascending=False)
    print(cr.to_string(index=False))

if __name__ == "__main__":
    audit()
