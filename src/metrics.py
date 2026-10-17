"""
Analytical Metrics and Business Intelligence Calculations
Indonesia E-Commerce Sales & Shipping Analytics (2023-2025)
Author: Ferdian Hanif
Email: ferdianhanif001@gmail.com
"""

import os
import sqlite3
import pandas as pd
import numpy as np

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "processed", "ecommerce_analytics.db"))

def get_connection():
    return sqlite3.connect(DB_PATH)

def get_executive_kpis(conn=None):
    """Retrieve macro KPIs for the entire portfolio."""
    close_at_end = False
    if conn is None:
        conn = get_connection()
        close_at_end = True

    query = """
    SELECT 
        COUNT(*) AS total_orders,
        SUM(is_completed) AS completed_orders,
        SUM(is_cancelled) AS cancelled_orders,
        ROUND(CAST(SUM(is_cancelled) AS FLOAT) / COUNT(*) * 100, 2) AS cancellation_rate_pct,
        SUM(order_qty) AS total_units_sold,
        ROUND(SUM(total_payment) / 1000000.0, 2) AS total_revenue_million_idr,
        ROUND(AVG(CASE WHEN is_completed = 1 THEN total_payment ELSE NULL END), 0) AS aov_completed_idr,
        ROUND(SUM(shipping_actual_cost) / 1000000.0, 2) AS total_logistics_cost_million_idr,
        ROUND(SUM(shipping_subsidy) / 1000000.0, 2) AS total_subsidy_million_idr,
        ROUND(CAST(SUM(is_free_shipping) AS FLOAT) / COUNT(*) * 100, 2) AS free_shipping_adoption_pct
    FROM orders;
    """
    df = pd.read_sql_query(query, conn)
    if close_at_end:
        conn.close()
    return df

def get_monthly_runrate(conn=None):
    """Retrieve monthly trend of sales volume, revenue, and cancellation rate."""
    close_at_end = False
    if conn is None:
        conn = get_connection()
        close_at_end = True

    query = """
    SELECT 
        year_month,
        COUNT(*) AS total_orders,
        SUM(order_qty) AS total_units,
        ROUND(SUM(total_payment) / 1000000.0, 2) AS revenue_million_idr,
        SUM(is_cancelled) AS cancelled_orders,
        ROUND(CAST(SUM(is_cancelled) AS FLOAT) / COUNT(*) * 100, 2) AS cancellation_rate_pct,
        ROUND(AVG(shipping_actual_cost), 0) AS avg_shipping_cost_idr
    FROM orders
    GROUP BY year_month
    ORDER BY year_month ASC;
    """
    df = pd.read_sql_query(query, conn)
    if close_at_end:
        conn.close()
    return df

def get_payment_cancellation_analysis(conn=None):
    """Analyze transaction share and cancellation risk per payment method."""
    close_at_end = False
    if conn is None:
        conn = get_connection()
        close_at_end = True

    query = """
    SELECT 
        payment_group,
        COUNT(*) AS total_orders,
        ROUND(CAST(COUNT(*) AS FLOAT) / (SELECT COUNT(*) FROM orders) * 100, 2) AS order_share_pct,
        SUM(is_completed) AS completed_orders,
        SUM(is_cancelled) AS cancelled_orders,
        ROUND(CAST(SUM(is_cancelled) AS FLOAT) / COUNT(*) * 100, 2) AS cancellation_rate_pct,
        ROUND(SUM(total_payment) / 1000000.0, 2) AS total_revenue_million_idr,
        ROUND(AVG(total_payment), 0) AS avg_order_value_idr
    FROM orders
    GROUP BY payment_group
    ORDER BY total_orders DESC;
    """
    df = pd.read_sql_query(query, conn)
    if close_at_end:
        conn.close()
    return df

def get_regional_logistics_disparity(conn=None):
    """Analyze logistics cost, subsidy, and cancellation between Java and Outer Islands."""
    close_at_end = False
    if conn is None:
        conn = get_connection()
        close_at_end = True

    query = """
    SELECT 
        region_group,
        COUNT(*) AS total_orders,
        ROUND(CAST(COUNT(*) AS FLOAT) / (SELECT COUNT(*) FROM orders) * 100, 2) AS order_share_pct,
        ROUND(SUM(total_payment) / 1000000.0, 2) AS total_revenue_million_idr,
        ROUND(AVG(shipping_actual_cost), 0) AS avg_shipping_cost_idr,
        ROUND(AVG(shipping_buyer_paid), 0) AS avg_buyer_paid_idr,
        ROUND(AVG(shipping_subsidy), 0) AS avg_subsidy_idr,
        ROUND(AVG(weight_grams), 0) AS avg_weight_grams,
        ROUND(CAST(SUM(is_cancelled) AS FLOAT) / COUNT(*) * 100, 2) AS cancellation_rate_pct
    FROM orders
    GROUP BY region_group;
    """
    df = pd.read_sql_query(query, conn)
    if close_at_end:
        conn.close()
    return df

def get_logistics_cost_structure(conn=None):
    """Calculate the breakdown of shipping cost burden: buyer paid vs platform subsidy."""
    close_at_end = False
    if conn is None:
        conn = get_connection()
        close_at_end = True

    query = """
    SELECT 
        ROUND(SUM(shipping_actual_cost) / 1000000.0, 2) AS total_actual_cost_million,
        ROUND(SUM(shipping_buyer_paid) / 1000000.0, 2) AS total_buyer_paid_million,
        ROUND(SUM(shipping_subsidy) / 1000000.0, 2) AS total_subsidy_million
    FROM orders;
    """
    df = pd.read_sql_query(query, conn)
    if close_at_end:
        conn.close()
    return df

if __name__ == "__main__":
    conn = get_connection()
    print("=== Executive KPIs ===")
    print(get_executive_kpis(conn))
    print("\n=== Monthly Trends (Sample) ===")
    print(get_monthly_runrate(conn).head(4))
    print("\n=== Payment Cancellation Analysis ===")
    print(get_payment_cancellation_analysis(conn))
    print("\n=== Regional Logistics Disparity ===")
    print(get_regional_logistics_disparity(conn))
    conn.close()
