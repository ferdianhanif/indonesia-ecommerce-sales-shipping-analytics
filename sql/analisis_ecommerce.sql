-- ====================================================================
-- Portofolio Analisis Data E-Commerce & Logistik Indonesia (2023–2025)
-- Berkas Tunggal Kueri SQL Terpadu (Single Consolidated SQL File)
-- 
-- Author : Ferdian Hanif
-- Email  : ferdianhanif001@gmail.com
-- Dialek : ANSI SQL (Kompatibel langsung dengan PostgreSQL, MySQL 8.0+, dan SQLite)
-- Tabel  : orders (20.848 baris data transaksi tervalidasi)
-- ====================================================================


-- --------------------------------------------------------------------
-- BAGIAN 1: RINGKASAN METRIK EKSEKUTIF MAKRO & TREN BULANAN
-- --------------------------------------------------------------------

-- 1.1 Metrik Agregat Keseluruhan (Macro Portfolio KPIs)
SELECT 
    COUNT(*) AS total_pesanan,
    SUM(CASE WHEN status_kategori = 'Selesai' THEN 1 ELSE 0 END) AS pesanan_selesai,
    SUM(CASE WHEN status_kategori = 'Batal' THEN 1 ELSE 0 END) AS pesanan_batal,
    ROUND(CAST(SUM(CASE WHEN status_kategori = 'Batal' THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100, 2) AS rasio_pembatalan_pct,
    SUM(order_qty) AS total_unit_terjual,
    ROUND(SUM(total_payment) / 1000000.0, 2) AS total_omzet_juta_rp,
    ROUND(AVG(CASE WHEN status_kategori = 'Selesai' THEN total_payment ELSE NULL END), 0) AS aov_pesanan_selesai_rp,
    ROUND(SUM(shipping_actual_cost) / 1000000.0, 2) AS total_biaya_riil_logistik_juta_rp,
    ROUND(SUM(shipping_subsidy) / 1000000.0, 2) AS total_subsidi_ongkir_juta_rp,
    ROUND(CAST(SUM(is_free_shipping) AS FLOAT) / COUNT(*) * 100, 2) AS adopsi_gratis_ongkir_pct
FROM orders;


-- 1.2 Tren Bulanan (Monthly Run-Rate: Volume, Omzet, dan Tingkat Pembatalan)
SELECT 
    year_month,
    COUNT(*) AS total_pesanan,
    SUM(order_qty) AS total_unit,
    ROUND(SUM(total_payment) / 1000000.0, 2) AS omzet_juta_rp,
    SUM(CASE WHEN status_kategori = 'Batal' THEN 1 ELSE 0 END) AS pesanan_batal,
    ROUND(CAST(SUM(CASE WHEN status_kategori = 'Batal' THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100, 2) AS rasio_pembatalan_pct,
    ROUND(AVG(shipping_actual_cost), 0) AS rata_rata_ongkir_rp
FROM orders
GROUP BY year_month
ORDER BY year_month ASC;


-- --------------------------------------------------------------------
-- BAGIAN 2: EVALUASI RISIKO PEMBATALAN BERDASARKAN METODE PEMBAYARAN
-- --------------------------------------------------------------------

-- 2.1 Analisis Pembatalan per Kelompok Metode Pembayaran
SELECT 
    payment_group,
    COUNT(*) AS total_transaksi,
    ROUND(CAST(COUNT(*) AS FLOAT) / (SELECT COUNT(*) FROM orders) * 100, 2) AS pangsa_pesanan_pct,
    SUM(CASE WHEN status_kategori = 'Selesai' THEN 1 ELSE 0 END) AS pesanan_berhasil,
    SUM(CASE WHEN status_kategori = 'Batal' THEN 1 ELSE 0 END) AS pesanan_gagal,
    ROUND(CAST(SUM(CASE WHEN status_kategori = 'Batal' THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100, 2) AS tingkat_pembatalan_pct,
    ROUND(SUM(total_payment) / 1000000.0, 2) AS total_nilai_pembayaran_juta_rp,
    ROUND(AVG(total_payment), 0) AS rata_rata_nilai_pesanan_rp
FROM orders
GROUP BY payment_group
ORDER BY total_transaksi DESC;


-- 2.2 Alasan Utama Pembatalan Pesanan pada Metode COD vs Non-COD
SELECT 
    CASE WHEN payment_group = 'COD (Bayar di Tempat)' THEN 'Metode COD' ELSE 'Metode Non-COD' END AS segmentasi_metode,
    COALESCE("Alasan Pembatalan", 'Alasan Tidak Dicantumkan / Sistem') AS alasan_pembatalan_ringkas,
    COUNT(*) AS frekuensi_pembatalan,
    ROUND(CAST(COUNT(*) AS FLOAT) / SUM(COUNT(*)) OVER (PARTITION BY (CASE WHEN payment_group = 'COD (Bayar di Tempat)' THEN 'Metode COD' ELSE 'Metode Non-COD' END)) * 100, 2) AS proporsi_alasan_pct
FROM orders
WHERE status_kategori = 'Batal'
GROUP BY segmentasi_metode, "Alasan Pembatalan"
ORDER BY segmentasi_metode, frekuensi_pembatalan DESC
LIMIT 12;


-- --------------------------------------------------------------------
-- BAGIAN 3: DISPARITAS LOGISTIK REGIONAL & BEBAN SUBSIDI ONGKIR
-- --------------------------------------------------------------------

-- 3.1 Perbandingan Kinerja Logistik: Pulau Jawa vs Luar Pulau Jawa
SELECT 
    region_group,
    COUNT(*) AS total_pesanan,
    ROUND(CAST(COUNT(*) AS FLOAT) / (SELECT COUNT(*) FROM orders) * 100, 2) AS pangsa_pesanan_pct,
    ROUND(SUM(total_payment) / 1000000.0, 2) AS total_omzet_juta_rp,
    ROUND(AVG(shipping_actual_cost), 0) AS rata_rata_biaya_ongkir_rp,
    ROUND(AVG(shipping_buyer_paid), 0) AS rata_rata_ongkir_dibayar_pembeli_rp,
    ROUND(AVG(shipping_subsidy), 0) AS rata_rata_subsidi_ongkir_rp,
    ROUND(AVG(weight_grams), 0) AS rata_rata_berat_gram,
    ROUND(CAST(SUM(is_cancelled) AS FLOAT) / COUNT(*) * 100, 2) AS tingkat_pembatalan_pct
FROM orders
GROUP BY region_group;


-- 3.2 Evaluasi Efisiensi dan Pangsa Kurir Pengiriman
SELECT 
    courier_group,
    COUNT(*) AS total_pengiriman,
    ROUND(CAST(COUNT(*) AS FLOAT) / (SELECT COUNT(*) FROM orders) * 100, 2) AS pangsa_volume_pct,
    ROUND(AVG(shipping_actual_cost), 0) AS rata_rata_biaya_ongkir_rp,
    ROUND(AVG(weight_grams), 0) AS rata_rata_berat_paket_gram,
    ROUND(CAST(SUM(is_cancelled) AS FLOAT) / COUNT(*) * 100, 2) AS tingkat_pembatalan_pct
FROM orders
GROUP BY courier_group
ORDER BY total_pengiriman DESC;
