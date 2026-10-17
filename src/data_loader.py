"""
Data Loading, Cleaning, and Standardization Pipeline
Indonesia E-Commerce Sales & Shipping Analytics (2023-2025)
Author: Ferdian Hanif
Email: ferdianhanif001@gmail.com
"""

import os
import re
import sqlite3
import pandas as pd
import numpy as np

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "ecommerce_sales_shipping.csv")
CLEAN_CSV_PATH = os.path.join(BASE_DIR, "data", "processed", "clean_ecommerce_sales.csv")
DB_PATH = os.path.join(BASE_DIR, "data", "processed", "ecommerce_analytics.db")

JAWA_PROVINCES = [
    "DKI JAKARTA", "JAWA BARAT", "JAWA TENGAH", "JAWA TIMUR", "BANTEN", "DI YOGYAKARTA"
]

MONTH_MAP = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12
}

def parse_month_year_from_source(source_str):
    """Extract year and month integer from source file name."""
    s = str(source_str).lower()
    year_match = re.search(r"(2023|2024|2025)", s)
    year = int(year_match.group(1)) if year_match else 2024
    
    month = 1
    for m_name, m_val in MONTH_MAP.items():
        if m_name in s:
            month = m_val
            break
    return year, month

def clean_data():
    print(f"Loading raw dataset from {RAW_DATA_PATH}...")
    df = pd.read_csv(RAW_DATA_PATH, sep=";", encoding="utf-8-sig", low_memory=False)
    initial_rows = len(df)
    print(f"Raw records loaded: {initial_rows:,}")

    # 1. Clean order dates and derive year_month
    df["order_timestamp"] = pd.to_datetime(df["Waktu Pesanan Dibuat"], errors="coerce")
    
    years = []
    months = []
    year_months = []
    
    for idx, row in df.iterrows():
        ts = row["order_timestamp"]
        if pd.notnull(ts):
            y = ts.year
            m = ts.month
        else:
            y, m = parse_month_year_from_source(row["source_file"])
        years.append(y)
        months.append(m)
        year_months.append(f"{y:04d}-{m:02d}")

    df["order_year"] = years
    df["order_month"] = months
    df["year_month"] = year_months

    # 2. Standardize Status Pesanan
    status_clean = []
    for s in df["Status Pesanan"].astype(str):
        s_low = s.lower()
        if "selesai" in s_low or "pesanan diterima" in s_low:
            status_clean.append("Selesai")
        elif "batal" in s_low:
            status_clean.append("Batal")
        elif "kirim" in s_low:
            status_clean.append("Dalam Pengiriman")
        else:
            status_clean.append("Lainnya")
    df["status_kategori"] = status_clean
    df["is_cancelled"] = (df["status_kategori"] == "Batal").astype(int)
    df["is_completed"] = (df["status_kategori"] == "Selesai").astype(int)

    # 3. Standardize Payment Method
    def group_payment(p):
        p_str = str(p).strip()
        if "COD" in p_str:
            return "COD (Bayar di Tempat)"
        elif "ShopeePay" in p_str or "SeaBank" in p_str:
            return "E-Wallet / Bank Digital"
        elif "Online Payment" in p_str or "BCA" in p_str or "Kartu" in p_str or "Transfer" in p_str:
            return "Transfer Bank / Kartu"
        elif "SPayLater" in p_str or "Cicilan" in p_str:
            return "PayLater"
        elif "Indomaret" in p_str or "Alfamart" in p_str:
            return "Gerai Retail (Minimarket)"
        else:
            return "Lainnya"

    df["payment_group"] = df["Metode Pembayaran"].apply(group_payment)

    # 4. Standardize Couriers
    def group_courier(c):
        c_str = str(c)
        if "SPX" in c_str:
            return "Shopee Xpress (SPX)"
        elif "J&T" in c_str:
            return "J&T Express"
        elif "JNE" in c_str:
            return "JNE Express"
        elif "SiCepat" in c_str:
            return "SiCepat"
        elif "Anteraja" in c_str:
            return "Anteraja"
        else:
            return "Kargo / Kurir Lainnya"

    df["courier_group"] = df["Opsi Pengiriman"].apply(group_courier)

    # 5. Standardize Regional Classification (Jawa vs Luar Jawa)
    def classify_region(prov):
        prov_clean = str(prov).upper().strip()
        if any(j in prov_clean for j in JAWA_PROVINCES):
            return "Pulau Jawa"
        return "Luar Pulau Jawa"

    df["region_group"] = df["Provinsi"].apply(classify_region)

    # 6. Logistics economics metrics
    df["shipping_actual_cost"] = df["Perkiraan Ongkos Kirim"].clip(lower=0)
    df["shipping_buyer_paid"] = df["Ongkos Kirim Dibayar oleh Pembeli"].clip(lower=0)
    df["shipping_subsidy"] = df["Estimasi Potongan Biaya Pengiriman"].clip(lower=0)
    df["is_free_shipping"] = (df["shipping_buyer_paid"] == 0).astype(int)
    
    # 7. Financial & Order Volume Metrics
    df["total_payment"] = df["Total Pembayaran"].clip(lower=0)
    df["total_discount"] = df["Total Diskon"].clip(lower=0)
    df["order_qty"] = df["total_qty"].clip(lower=1)
    df["weight_grams"] = df["total_weight_gr"].clip(lower=0)

    # Clean product categories
    df["category_clean"] = df["product_categories"].fillna("Lainnya").astype(str).str.strip()

    print(f"Data cleaning complete. Clean records: {len(df):,}")

    # Export to clean CSV
    os.makedirs(os.path.dirname(CLEAN_CSV_PATH), exist_ok=True)
    df.to_csv(CLEAN_CSV_PATH, index=False, encoding="utf-8")
    print(f"Clean CSV saved: {CLEAN_CSV_PATH}")

    # Export to SQLite database
    print(f"Loading data into SQLite database: {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("orders", conn, if_exists="replace", index=False)
    
    # Create indexes for optimal query performance
    cursor = conn.cursor()
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_orders_year_month ON orders(year_month)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status_kategori)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_orders_payment ON orders(payment_group)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_orders_region ON orders(region_group)")
    conn.commit()
    conn.close()
    print("SQLite database successfully created and indexed.")
    return df

if __name__ == "__main__":
    clean_data()
