"""
Executive Presentation Deck Generator for Indonesia E-Commerce Sales & Shipping Analytics
Clean, professional, pixel-perfect 16:9 Landscape presentation deck.
Exact styling match for 'AWS Cloud Engineering Labs - Ferdian Hanif (ID).pdf':
- Canvas: 1080pt x 607.92pt (exact 16:9)
- Warm cream background (#FAF9F5)
- Title: Barlow Condensed ExtraBold (#4361EE), font-size 38pt - 45pt
- Subtitle: Inter Bold uppercase green (#059669), font-size 15.5pt - 16pt
- Body & Bullets: Inter, font-size 14.8pt - 15.5pt, line-height 1.55
- Crisp White Cards with high-res figures & centered captions
- Cover slide with concentric rings on left and wavy contour lines on bottom right
- Pill badge on cover: Ferdian Hanif & ferdianhanif001@gmail.com (NO DEGREES)
- Slide 6: Strategy Cards + Terminal Diagnostic Bar matching AWS Slide 10
- 100% natural Indonesian using humanizer principles (Junior-to-Mid Data Analyst POV)
Author: Ferdian Hanif
Email: ferdianhanif001@gmail.com
"""

import os
import asyncio
from playwright.async_api import async_playwright

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
HTML_TEMPLATE_PATH = os.path.join(BASE_DIR, "reports", "deck_template.html")
PDF_OUTPUT_PATH = os.path.join(BASE_DIR, "reports", "presentation_deck.pdf")
FIG_DIR = os.path.join(BASE_DIR, "reports", "figures")

def get_file_uri(filename):
    path = os.path.join(FIG_DIR, filename).replace("\\", "/")
    return f"file:///{path}"

FIG1_URI = get_file_uri("fig1_monthly_sales_trend.png")
FIG2_URI = get_file_uri("fig2_payment_method_cancellation_risk.png")
FIG3_URI = get_file_uri("fig3_regional_shipping_cost_and_cancellation.png")
FIG4_URI = get_file_uri("fig4_logistics_cost_structure_and_subsidy.png")

# Corner graphics
CONTOUR_BOTTOM_LEFT = """
<svg class="contour-svg bottom-left" viewBox="0 0 500 500" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M-60 460 C 40 370, 160 480, 240 390 C 320 300, 190 170, 300 70" stroke="#7DD3FC" stroke-width="2" stroke-linecap="round"/>
  <path d="M-80 480 C 30 380, 150 490, 250 400 C 340 310, 200 160, 320 60" stroke="#7DD3FC" stroke-width="2" stroke-linecap="round"/>
  <path d="M-100 500 C 20 390, 140 500, 260 410 C 360 320, 210 150, 340 50" stroke="#7DD3FC" stroke-width="2" stroke-linecap="round"/>
  <path d="M-120 520 C 10 400, 130 510, 270 420 C 380 330, 220 140, 360 40" stroke="#7DD3FC" stroke-width="2" stroke-linecap="round"/>
  <path d="M-140 540 C 0 410, 120 520, 280 430 C 400 340, 230 130, 380 30" stroke="#7DD3FC" stroke-width="2" stroke-linecap="round"/>
  <path d="M-160 560 C -10 420, 110 530, 290 440 C 420 350, 240 120, 400 20" stroke="#7DD3FC" stroke-width="2" stroke-linecap="round"/>
</svg>
"""

CONTOUR_BOTTOM_RIGHT = """
<svg class="contour-svg bottom-right" viewBox="0 0 500 500" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M220 480 C 290 390, 390 470, 460 380 C 530 290, 410 170, 520 90" stroke="#7DD3FC" stroke-width="2" stroke-linecap="round"/>
  <path d="M200 500 C 280 400, 380 480, 470 390 C 550 300, 420 160, 540 80" stroke="#7DD3FC" stroke-width="2" stroke-linecap="round"/>
  <path d="M180 520 C 270 410, 370 490, 480 400 C 570 310, 430 150, 560 70" stroke="#7DD3FC" stroke-width="2" stroke-linecap="round"/>
  <path d="M160 540 C 260 420, 360 500, 490 410 C 590 320, 440 140, 580 60" stroke="#7DD3FC" stroke-width="2" stroke-linecap="round"/>
  <path d="M140 560 C 250 430, 350 510, 500 420 C 610 330, 450 130, 600 50" stroke="#7DD3FC" stroke-width="2" stroke-linecap="round"/>
</svg>
"""

RINGS_TOP_LEFT = """
<svg class="contour-svg top-left" viewBox="0 0 300 500" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="10" cy="110" r="105" stroke="#7DD3FC" stroke-width="1.8"/>
  <circle cx="10" cy="170" r="105" stroke="#7DD3FC" stroke-width="1.8"/>
  <circle cx="10" cy="230" r="105" stroke="#7DD3FC" stroke-width="1.8"/>
  <circle cx="10" cy="290" r="105" stroke="#7DD3FC" stroke-width="1.8"/>
  <circle cx="10" cy="350" r="105" stroke="#7DD3FC" stroke-width="1.8"/>
</svg>
"""

HTML_CONTENT = f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700;800;900&family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet">
<style>
  @page {{
    size: 1080pt 607.92pt;
    margin: 0;
  }}
  * {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }}
  body {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    color: #1E293B;
    background-color: #F8FAFC;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}
  .slide {{
    width: 1080pt;
    height: 607.92pt;
    padding: 34pt 52pt 28pt 52pt;
    page-break-after: always;
    position: relative;
    background-color: #F8FAFC;
    overflow: hidden;
    display: flex;
    flex-direction: column;
  }}

  /* Background SVGs */
  .contour-svg {{
    position: absolute;
    pointer-events: none;
    z-index: 1;
    opacity: 0.75;
  }}
  .contour-svg.bottom-left {{
    width: 280pt;
    height: 280pt;
    bottom: -30pt;
    left: -30pt;
  }}
  .contour-svg.bottom-right {{
    width: 280pt;
    height: 280pt;
    bottom: -25pt;
    right: -25pt;
  }}
  .contour-svg.top-left {{
    width: 200pt;
    height: 320pt;
    top: 30pt;
    left: -25pt;
  }}

  /* Content Wrapper */
  .content-layer {{
    position: relative;
    z-index: 10;
    display: flex;
    flex-direction: column;
    height: 100%;
  }}

  /* Slide Header */
  .slide-header {{
    text-align: center;
    margin-bottom: 22pt;
  }}
  .slide-title {{
    font-family: 'Barlow Condensed', 'Impact', sans-serif;
    font-size: 38pt;
    font-weight: 800;
    letter-spacing: 0.8pt;
    text-transform: uppercase;
    color: #0C4A6E;
    line-height: 1.1;
    margin-bottom: 4pt;
  }}
  .slide-subtitle {{
    font-family: 'Inter', sans-serif;
    font-size: 15.5pt;
    font-weight: 700;
    letter-spacing: 1.4pt;
    text-transform: uppercase;
    color: #D97706;
  }}

  /* 2-Column Grid Layout */
  .grid-2 {{
    display: grid;
    grid-template-columns: 505pt 450pt;
    gap: 20pt;
    align-items: center;
    flex: 1;
  }}

  /* Bullets & Typography */
  .bullet-list {{
    list-style: none;
    margin: 0;
    padding: 0;
  }}
  .bullet-list > li {{
    font-size: 14.8pt;
    line-height: 1.55;
    color: #1E293B;
    margin-bottom: 14pt;
    position: relative;
    padding-left: 22pt;
  }}
  .bullet-list > li:last-child {{
    margin-bottom: 0;
  }}
  .bullet-list > li::before {{
    content: "•";
    color: #0F172A;
    font-size: 20pt;
    position: absolute;
    left: 0;
    top: -3pt;
    font-weight: bold;
  }}
  .bullet-list strong {{
    color: #0F172A;
    font-weight: 700;
  }}
  .sub-bullet-list {{
    list-style: none;
    margin-top: 5pt;
    margin-left: 4pt;
  }}
  .sub-bullet-list li {{
    font-size: 13.8pt;
    line-height: 1.5;
    color: #334155;
    margin-bottom: 5pt;
    position: relative;
    padding-left: 18pt;
  }}
  .sub-bullet-list li:last-child {{
    margin-bottom: 0;
  }}
  .sub-bullet-list li::before {{
    content: "○";
    color: #0284C7;
    font-size: 12pt;
    position: absolute;
    left: 0;
    top: 0;
    font-weight: bold;
  }}

  /* White Card Containers */
  .chart-card-single {{
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12pt;
    padding: 10pt;
    box-shadow: 0 4pt 12pt rgba(0, 0, 0, 0.03);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
  }}
  .chart-card-single img {{
    width: 100%;
    height: 330pt;
    object-fit: contain;
    border-radius: 6pt;
  }}
  .chart-card-caption {{
    font-size: 13.5pt;
    font-weight: 700;
    color: #0F172A;
    text-align: center;
    margin-top: 8pt;
  }}

  /* Stacked Half Cards (Slide 5) */
  .card-stack {{
    display: flex;
    flex-direction: column;
    gap: 12pt;
    width: 100%;
  }}
  .chart-card-half {{
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 10pt;
    padding: 8pt 10pt 6pt 10pt;
    box-shadow: 0 3pt 8pt rgba(0, 0, 0, 0.03);
    display: flex;
    flex-direction: column;
    align-items: center;
  }}
  .chart-card-half img {{
    width: 100%;
    height: 148pt;
    object-fit: contain;
    border-radius: 4pt;
  }}
  .chart-card-half .caption {{
    font-size: 11.5pt;
    font-weight: 700;
    color: #0F172A;
    text-align: center;
    margin-top: 4pt;
  }}

  /* Slide 2 Macro KPI Cards */
  .kpi-container {{
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12pt;
    padding: 16pt;
    box-shadow: 0 4pt 12pt rgba(0, 0, 0, 0.03);
    display: flex;
    flex-direction: column;
    justify-content: center;
    height: 100%;
  }}
  .kpi-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12pt;
    margin-bottom: 12pt;
  }}
  .kpi-box {{
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-left: 4pt solid #0284C7;
    border-radius: 8pt;
    padding: 12pt 14pt;
  }}
  .kpi-box.green {{
    border-left-color: #0D9488;
  }}
  .kpi-box.amber {{
    border-left-color: #D97706;
  }}
  .kpi-box.purple {{
    border-left-color: #6366F1;
  }}
  .kpi-label {{
    font-size: 11pt;
    font-weight: 700;
    letter-spacing: 0.8pt;
    text-transform: uppercase;
    color: #64748B;
    margin-bottom: 3pt;
  }}
  .kpi-val {{
    font-size: 24pt;
    font-weight: 800;
    color: #0F172A;
    line-height: 1.1;
    margin-bottom: 3pt;
  }}
  .kpi-desc {{
    font-size: 10.5pt;
    color: #475569;
  }}
  .kpi-highlight {{
    background: #F0F9FF;
    border: 1px solid #BAE6FD;
    border-radius: 8pt;
    padding: 10pt 14pt;
    font-size: 11.5pt;
    color: #0369A1;
    line-height: 1.5;
  }}

  /* Slide 6 Strategic Cards (matching AWS Slide 10) */
  .strategy-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 18pt;
    margin-bottom: 16pt;
  }}
  .strategy-card {{
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12pt;
    padding: 18pt 20pt;
    box-shadow: 0 4pt 12pt rgba(0, 0, 0, 0.03);
  }}
  .strategy-card-title {{
    font-size: 15.5pt;
    font-weight: 800;
    letter-spacing: 0.5pt;
    text-transform: uppercase;
    margin-bottom: 12pt;
  }}
  .strategy-card-title.pricing {{
    color: #0C4A6E;
  }}
  .strategy-card-title.logistics {{
    color: #D97706;
  }}
  .strategy-bullets {{
    list-style: none;
    margin: 0;
    padding: 0;
  }}
  .strategy-bullets li {{
    font-size: 13.5pt;
    line-height: 1.5;
    color: #334155;
    margin-bottom: 9pt;
    position: relative;
    padding-left: 18pt;
  }}
  .strategy-bullets li:last-child {{
    margin-bottom: 0;
  }}
  .strategy-bullets li::before {{
    content: "•";
    color: #0F172A;
    font-size: 18pt;
    position: absolute;
    left: 0;
    top: -3pt;
    font-weight: bold;
  }}
  .strategy-bullets strong {{
    color: #0F172A;
  }}
  .diagnostic-terminal {{
    background: #0B132B;
    border-radius: 8pt;
    padding: 12pt 18pt;
    font-family: 'JetBrains Mono', 'Consolas', monospace;
    color: #F8FAFC;
    font-size: 11.5pt;
    line-height: 1.6;
  }}
  .diagnostic-terminal .term-title {{
    color: #38BDF8;
    font-weight: 700;
    margin-bottom: 4pt;
  }}
  .diagnostic-terminal .term-line {{
    color: #CBD5E1;
  }}
  .diagnostic-terminal .term-highlight {{
    color: #FBBF24;
    font-weight: 700;
  }}

  /* Cover Slide Layout */
  .cover-box {{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    text-align: center;
  }}
  .cover-title {{
    font-family: 'Barlow Condensed', 'Impact', sans-serif;
    font-size: 44pt;
    font-weight: 800;
    letter-spacing: 1.2pt;
    text-transform: uppercase;
    color: #0C4A6E;
    line-height: 1.15;
    max-width: 860pt;
    margin-bottom: 14pt;
  }}
  .cover-subtitle {{
    font-family: 'Inter', sans-serif;
    font-size: 15.5pt;
    font-weight: 600;
    color: #475569;
    letter-spacing: 1.2pt;
    text-transform: uppercase;
    max-width: 820pt;
    line-height: 1.5;
    margin-bottom: 32pt;
  }}
  .cover-author-label {{
    font-size: 16.5pt;
    color: #1E293B;
    margin-bottom: 12pt;
  }}
  .cover-badge {{
    border: 2pt solid #0C4A6E;
    border-radius: 9999px;
    padding: 10pt 42pt;
    background: rgba(255, 255, 255, 0.85);
    display: inline-flex;
    flex-direction: column;
    align-items: center;
  }}
  .author-name {{
    font-size: 20pt;
    font-weight: 700;
    color: #0C4A6E;
  }}
  .author-contact {{
    font-size: 14.5pt;
    font-weight: 500;
    color: #0284C7;
    margin-top: 2pt;
  }}
</style>
</head>
<body>

  <!-- ==================== SLIDE 1: COVER ==================== -->
  <div class="slide">
    {RINGS_TOP_LEFT}
    {CONTOUR_BOTTOM_RIGHT}
    <div class="content-layer">
      <div class="cover-box">
        <h1 class="cover-title">ANALISIS PENJUALAN & EFISIENSI LOGISTIK E-COMMERCE</h1>
        <div class="cover-subtitle">STUDI EMPIRIS 20.848 TRANSAKSI, RISIKO PEMBATALAN COD & SUBSIDI ONGKIR (2023–2025)</div>
        <div class="cover-author-label">Oleh:</div>
        <div class="cover-badge">
          <div class="author-name">Ferdian Hanif</div>
          <div class="author-contact">ferdianhanif001@gmail.com</div>
        </div>
      </div>
    </div>
  </div>

  <!-- ==================== SLIDE 2: PENDAHULUAN & RUANG LINGKUP DATA ==================== -->
  <div class="slide">
    {CONTOUR_BOTTOM_LEFT}
    <div class="content-layer">
      <div class="slide-header">
        <h2 class="slide-title">PENDAHULUAN & RUANG LINGKUP DATA</h2>
        <div class="slide-subtitle">AUDIT 20.848 PESANAN E-COMMERCE SELAMA 24 BULAN OPERASIONAL</div>
      </div>
      <div class="grid-2">
        <div>
          <ul class="bullet-list">
            <li>
              <strong>Latar Belakang Bisnis:</strong> Toko e-commerce menghadapi tantangan ganda: ketergantungan tinggi pada metode bayar di tempat (COD) yang rentan gagal kirim, serta tingginya subsidi logistik antarpulau.
            </li>
            <li>
              <strong>Ruang Lingkup Data & Metodologi:</strong>
              <ul class="sub-bullet-list">
                <li><strong>Skala Pencatatan:</strong> 20.848 transaksi dari 24 berkas penjualan bulanan (Desember 2023 hingga November 2025).</li>
                <li><strong>Pembersihan Skema:</strong> Parsing cap waktu, inferensi bulan hilang dari metadata berkas, serta standardisasi klaster kurir dan provinsi.</li>
                <li><strong>Pemodelan Database:</strong> Data ditransformasikan dan dimuat ke SQLite terindeks untuk query agregasi metrik finansial.</li>
              </ul>
            </li>
            <li>
              <strong>Tujuan Analisis:</strong> Memetakan pemicu pembatalan pesanan per metode bayar serta mengukur efisiensi pembebanan subsidi ongkos kirim toko.
            </li>
          </ul>
        </div>
        <div class="kpi-container">
          <div class="kpi-grid">
            <div class="kpi-box">
              <div class="kpi-label">Total Pesanan</div>
              <div class="kpi-val">20.848</div>
              <div class="kpi-desc">Transaksi dalam 24 bulan</div>
            </div>
            <div class="kpi-box green">
              <div class="kpi-label">Nilai Transaksi</div>
              <div class="kpi-val">Rp 1,06 M</div>
              <div class="kpi-desc">Total pembayaran kotor</div>
            </div>
            <div class="kpi-box amber">
              <div class="kpi-label">Pesanan Selesai</div>
              <div class="kpi-val">85,2%</div>
              <div class="kpi-desc">17.768 transaksi sukses</div>
            </div>
            <div class="kpi-box purple">
              <div class="kpi-label">Beban Subsidi</div>
              <div class="kpi-val">58,2%</div>
              <div class="kpi-desc">Rp 223,5 Jt ditanggung promo</div>
            </div>
          </div>
          <div class="kpi-highlight">
            <strong>Konteks Portofolio:</strong> Metode COD menyumbang 55,3% total transaksi toko, namun mendominasi 54,6% dari seluruh pesanan yang dibatalkan.
          </div>
          <div class="chart-card-caption" style="margin-top: 10pt;">Ringkasan Metrik Kunci Portofolio E-Commerce (2023–2025)</div>
        </div>
      </div>
    </div>
  </div>

  <!-- ==================== SLIDE 3: TREN PENJUALAN BULANAN ==================== -->
  <div class="slide">
    {CONTOUR_BOTTOM_LEFT}
    <div class="content-layer">
      <div class="slide-header">
        <h2 class="slide-title">TREN PENJUALAN BULANAN & POLA MUSIMAN</h2>
        <div class="slide-subtitle">FLUKTUASI VOLUME TRANSAKSI & LONJAKAN KAMPANYE TANGGAL KEMBAR</div>
      </div>
      <div class="grid-2">
        <div>
          <ul class="bullet-list">
            <li>
              <strong>Pola Pertumbuhan Volume:</strong> Volume transaksi mengalami akselerasi tajam mulai kuartal kedua 2024, didorong oleh partisipasi aktif pada program promo marketplace.
            </li>
            <li>
              <strong>Temuan Data:</strong>
              <ul class="sub-bullet-list">
                <li><strong>Puncak Transaksi:</strong> Terjadi pada Agustus 2024 (1.293 pesanan) dan Juli 2024 (1.270 pesanan), dengan omzet bulanan melampaui Rp 75 juta.</li>
                <li><strong>Lonjakan Musiman:</strong> Kampanye tanggal kembar (7.7, 8.8, 9.9) dan promo gajian melipatgandakan pesanan hingga 2,9x lipat dibanding awal tahun 2024.</li>
                <li><strong>Konsistensi 2025:</strong> Sepanjang tahun 2025, volume pesanan bertahan di kisaran 800 - 1.200 pesanan per bulan dengan rata-rata nilai transaksi Rp 50.680 per pesanan.</li>
              </ul>
            </li>
            <li>
              <strong>Rekomendasi Analis:</strong> Perlu penyiapan kapasitas stok kemasan dan tenaga operasional packing minimal dua minggu sebelum periode puncak belanja pertengahan tahun.
            </li>
          </ul>
        </div>
        <div class="chart-card-single">
          <img src="{FIG1_URI}" alt="Tren Penjualan Bulanan">
          <div class="chart-card-caption">Tren Volume Pesanan & Nilai Transaksi Bulanan (2023 - 2025)</div>
        </div>
      </div>
    </div>
  </div>

  <!-- ==================== SLIDE 4: RISIKO PEMBATALAN PESANAN ==================== -->
  <div class="slide">
    {CONTOUR_BOTTOM_LEFT}
    <div class="content-layer">
      <div class="slide-header">
        <h2 class="slide-title">RISIKO PEMBATALAN & METODE PEMBAYARAN</h2>
        <div class="slide-subtitle">KETERGANTUNGAN COD VS ANOMALI GAGAL BAYAR GERAI RETAIL</div>
      </div>
      <div class="grid-2">
        <div>
          <ul class="bullet-list">
            <li>
              <strong>Masalah Bisnis:</strong> Pembatalan pesanan menyebabkan kerugian biaya tenaga kerja, material kemasan rusak, dan risiko barang hilang pada proses retur.
            </li>
            <li>
              <strong>Temuan Data:</strong>
              <ul class="sub-bullet-list">
                <li><strong>Dominasi COD (55,3%):</strong> Metode COD mencatat 11.538 pesanan dengan rasio pembatalan 13,4% (1.544 pesanan gagal atau ditolak pembeli).</li>
                <li><strong>Anomali Minimarket:</strong> Pembayaran via gerai retail (Indomaret/Alfamart) mencatat kegagalan ekstrem (48,8% dan 47,2%) akibat pembeli tidak melunasi tagihan.</li>
                <li><strong>Keandalan E-Wallet:</strong> ShopeePay mencatat tingkat pembatalan terendah (hanya 8,7%) karena saldo terpotong seketika saat pesanan dibuat.</li>
              </ul>
            </li>
            <li>
              <strong>Akar Masalah:</strong> 43,1% pembatalan dipicu pembeli berubah pikiran, sedangkan 24,8% dibatalkan otomatis sistem akibat pembayaran melewati batas waktu.
            </li>
            <li>
              <strong>Rekomendasi Analis:</strong> Terapkan pembatasan opsi COD bagi pembeli dengan reputasi retur buruk dan beri insentif koin untuk transaksi nontunai.
            </li>
          </ul>
        </div>
        <div class="chart-card-single">
          <img src="{FIG2_URI}" alt="Risiko Pembatalan Metode Bayar">
          <div class="chart-card-caption">Pangsa Pesanan vs Tingkat Pembatalan Berdasarkan Metode Pembayaran</div>
        </div>
      </div>
    </div>
  </div>

  <!-- ==================== SLIDE 5: DISPARITAS LOGISTIK & SUBSIDI ONGKIR ==================== -->
  <div class="slide">
    {CONTOUR_BOTTOM_LEFT}
    <div class="content-layer">
      <div class="slide-header">
        <h2 class="slide-title">DISPARITAS LOGISTIK & STRUKTUR SUBSIDI</h2>
        <div class="slide-subtitle">BEBAN BIAYA ONGKIR ANTARPULAU & EFISIENSI SUBSIDI PENGIRIMAN</div>
      </div>
      <div class="grid-2">
        <div>
          <ul class="bullet-list">
            <li>
              <strong>Disparitas Antarpulau (Jawa vs Luar Jawa):</strong>
              <ul class="sub-bullet-list">
                <li><strong>Efisiensi Pulau Jawa:</strong> 79,3% pesanan berada di Jawa dengan ongkir terjangkau (Rp 13.544) dan tingkat pembatalan terkendali di 12,2%.</li>
                <li><strong>Lonjakan Biaya Luar Jawa:</strong> Pesanan luar pulau menanggung ongkir rata-rata Rp 37.096 (naik 2,7x lipat), memicu pembatalan naik ke 18,9%.</li>
              </ul>
            </li>
            <li>
              <strong>Struktur Beban Biaya Logistik:</strong>
              <ul class="sub-bullet-list">
                <li><strong>Beban Kurir:</strong> Total tagihan kurir mencapai Rp 384,1 Juta untuk 20.848 pengiriman.</li>
                <li><strong>Distribusi Beban:</strong> Subsidi platform menanggung 58,2% (Rp 223,5 Jt), pembeli 22,7% (Rp 87,4 Jt), dan selisih beban toko 19,1% (Rp 73,2 Jt).</li>
                <li><strong>Adopsi Bebas Ongkir:</strong> 69,8% pesanan (14.552 order) dinikmati pembeli dengan ongkos kirim Rp 0.</li>
              </ul>
            </li>
            <li>
              <strong>Rekomendasi Analis:</strong> Naikkan ambang batas belanja minimum untuk pesanan luar pulau agar margin kotor tidak tergerus selisih subsidi pengiriman.
            </li>
          </ul>
        </div>
        <div class="card-stack">
          <div class="chart-card-half">
            <img src="{FIG3_URI}" alt="Disparitas Ongkir Jawa vs Luar Jawa">
            <div class="caption">Biaya Ongkir Luar Jawa Rp 37,1rb (+174%) Memicu Pembatalan 18,9%</div>
          </div>
          <div class="chart-card-half">
            <img src="{FIG4_URI}" alt="Struktur Beban Logistik">
            <div class="caption">Subsidi Platform Menanggung 58,2% dari Total Biaya Kurir (Rp 384,1 Jt)</div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- ==================== SLIDE 6: STRATEGI & REKOMENDASI (Matching AWS Slide 10) ==================== -->
  <div class="slide">
    {RINGS_TOP_LEFT}
    <div class="content-layer">
      <div class="slide-header">
        <h2 class="slide-title">RANGKUMAN EKSEKUTIF & AKSI STRATEGIS</h2>
        <div class="slide-subtitle">PANDUAN OPERASIONAL MITIGASI RISIKO COD & EFISIENSI LOGISTIK</div>
      </div>
      
      <div class="strategy-grid">
        <div class="strategy-card">
          <div class="strategy-card-title pricing">STRATEGI PEMBAYARAN & MITIGASI COD</div>
          <ul class="strategy-bullets">
            <li><strong>Filter Transaksi COD Luar Pulau:</strong> Nonaktifkan opsi COD untuk pesanan luar pulau dengan nilai di atas Rp 200.000 guna menekan risiko retur barang (RTO).</li>
            <li><strong>Konfirmasi Instan Pesanan:</strong> Lakukan verifikasi otomatis dalam 15 menit pertama setelah order COD dibuat untuk memangkas pembatalan akibat berubah pikiran.</li>
            <li><strong>Insentif Transaksi Nontunai:</strong> Berikan potongan ekstra Rp 2.000 atau cashback koin untuk metode e-wallet (ShopeePay/SeaBank) yang terbukti memiliki pembatalan terendah (8,7%).</li>
            <li><strong>Tutup Jalur Gerai Minimarket:</strong> Hentikan opsi bayar Indomaret/Alfamart yang mencatat tingkat gagal bayar hingga 48,8% dan menahan stok sia-sia selama 24 jam.</li>
          </ul>
        </div>
        
        <div class="strategy-card">
          <div class="strategy-card-title logistics">STRATEGI LOGISTIK & EFISIENSI ONGKIR</div>
          <ul class="strategy-bullets">
            <li><strong>Standarisasi Bobot Paket:</strong> Batasi berat kemasan kardus di bawah 1.000 gram agar tidak terkena pembulatan tarif kiloan kedua pada kurir reguler dan hemat.</li>
            <li><strong>Ambang Batas Minimum Luar Jawa:</strong> Naikkan batas minimum belanja gratis ongkir dari Rp 30.000 menjadi Rp 60.000 khusus pesanan destinasi luar Pulau Jawa.</li>
            <li><strong>Optimasi Alokasi Kurir:</strong> Pertahankan Shopee Xpress (SPX) untuk pengiriman reguler urban (90,1% volume) dan arahkan paket kargo berat (>5 kg) ke JNE Trucking.</li>
            <li><strong>Monitoring Paket Gagal Kirim:</strong> Lakukan audit mingguan terhadap alamat pembeli yang mengalami kegagalan kirim berulang untuk meminimalisasi biaya retur logistik.</li>
          </ul>
        </div>
      </div>

      <div class="diagnostic-terminal">
        <div class="term-title">Rencana Implementasi & Evaluasi Bertahap:</div>
        <div class="term-line">
          • <span class="term-highlight">Bulan 1 (Pengendalian Risiko Pembayaran):</span> Implementasi filter pembatasan COD luar pulau dan integrasi pesan verifikasi instan untuk pesanan baru.
        </div>
        <div class="term-line">
          • <span class="term-highlight">Bulan 2 (Penataan Tarif & Kemasan):</span> Penyesuaian minimum belanja pesanan luar pulau dan audit standarisasi berat packing seluruh SKU utama.
        </div>
      </div>
    </div>
  </div>

</body>
</html>
"""

def save_html_template():
    with open(HTML_TEMPLATE_PATH, "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT)
    print(f"HTML template written: {HTML_TEMPLATE_PATH}")

async def render_pdf():
    save_html_template()
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Viewport with exact aspect ratio 1080pt x 607.92pt (1440px x 811px)
        page = await browser.new_page(viewport={"width": 1440, "height": 811})
        file_url = f"file:///{HTML_TEMPLATE_PATH.replace(os.sep, '/')}"
        print(f"Loading slide deck: {file_url}")
        await page.goto(file_url, wait_until="networkidle")
        # Ensure web fonts are completely loaded
        await page.evaluate("document.fonts.ready")
        await asyncio.sleep(1.0)
        
        await page.pdf(
            path=PDF_OUTPUT_PATH,
            prefer_css_page_size=True,
            print_background=True,
            page_ranges="1-6",
            margin={"top": "0", "bottom": "0", "left": "0", "right": "0"}
        )
        await browser.close()
        print(f"Executive Presentation Deck successfully generated: {PDF_OUTPUT_PATH}")
        
    # Clean up temporary HTML file so repository only retains presentation_deck.pdf
    if os.path.exists(HTML_TEMPLATE_PATH):
        os.remove(HTML_TEMPLATE_PATH)
        print("Cleaned up temporary HTML template.")

if __name__ == "__main__":
    asyncio.run(render_pdf())
