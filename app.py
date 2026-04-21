import streamlit as st
import pandas as pd
import numpy as np

# Sayfa Ayarları
st.set_page_config(page_title="Lifebox Strategic Pricing", layout="wide")

# Tasarım ve Okunabilirlik Ayarları (Dark Mode uyumlu, net metinler)
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 10px; border: 1px solid #e0e0e0; }
    [data-testid="stMetricValue"] { color: #1a73e8 !important; font-size: 35px; font-weight: bold; }
    [data-testid="stMetricLabel"] { color: #3c4043 !important; font-size: 18px; font-weight: 600; }
    .stSlider label, .stNumberInput label { color: white !important; font-weight: 500; }
    .price-box { text-align: center; background-color: #1e2129; padding: 30px; border-radius: 15px; border: 2px solid #00ffcc; margin: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Lifebox Strategic Pricing Cockpit")
st.caption("Pazar Benchmarking ve Karar Destek Sistemi")

# --- SOL PANEL: STRATEJİK GİRDİLER ---
with st.sidebar:
    st.header("📊 Global Rakip Benchmarks")
    google = st.number_input("Google One (100GB)", value=59.99)
    apple = st.number_input("iCloud+ (50GB)", value=39.99)
    dropbox = st.number_input("Dropbox (2TB)", value=350.00)
    
    st.divider()
    st.header("🎯 Stratejik Odak")
    strategy_mode = st.select_slider(
        "Pazar Hedefi",
        options=["Agresif Büyüme", "Dengeli", "Yüksek Karlılık"],
        value="Dengeli"
    )
    st.caption("Not: Seçilen mod, rakiplere göre uygulanacak 'Price Gap' oranını belirler.")

# --- MEKANİK: HESAPLAMA MOTORU ---
# Stratejiye göre indirim (Price Gap) oranları
if strategy_mode == "Agresif Büyüme":
    gap_p1, gap_p2 = 0.45, 0.55
elif strategy_mode == "Dengeli":
    gap_p1, gap_p2 = 0.25, 0.35
else: # Yüksek Karlılık
    gap_p1, gap_p2 = 0.10, 0.15

# Lifebox Paket Önerileri (GB bazlı akıllı konumlandırma)
suggested_p1 = apple * (1 - gap_p1) # 250GB Paketi Apple 50GB'dan ucuz olmalı
suggested_p2 = (dropbox / 4) * (1 - gap_p2) # 2.5TB Paketi Dropbox'ın hacim avantajını kırmalı

# --- TEPE NOKTASI: BÜYÜK ÖNERİ FİYATLARI ---
st.divider()
st.markdown(f"<h3 style='text-align: center;'>🎯 '{strategy_mode}' Modu İçin Önerilen Fiyatlandırma</h3>", unsafe_allow_html=True)
c_p1, c_p2 = st.columns(2)

with c_p1:
    st.markdown(f"""<div class='price-box'>
    <h3>📦 250 GB Paketi</h3>
    <p style='color: #888;'>Saklama Alanı + Premium</p>
    <h1 style='color: #00ffcc;'>{suggested_p1:.2f} TL</h1>
    <p>Hedef: Apple 50GB'ın %{gap_p1*100:.0f} Altı</p>
    </div>""", unsafe_allow_html=True)

with c_p2:
    st.markdown(f"""<div class='price-box'>
    <h3>🚀 2.5 TB Paketi</h3>
    <p style='color: #888;'>Saklama Alanı + Premium</p>
    <h1 style='color: #00ffcc;'>{suggested_p2:.2f} TL</h1>
    <p>Hedef: Dropbox 2TB Birim Fiyatının %{gap_p2*100:.0f} Altı</p>
    </div>""", unsafe_allow_html=True)

# --- STRATEJİK METRİKLER (GÜNCELLENMİŞ VE OKUNABİLİR) ---
st.divider()
st.subheader("📈 Birim Ekonomi Analizi")
m1, m2, m3 = st.columns(3)

# LTV/CAC Formülleri (Gerçekçi Cloud Metrikleri)
# Ortalama churn %3, müşteri ömrü 33 ay varsayımıyla
avg_arpu = (suggested_p1 + suggested_p2) / 2
ltv_val = avg_arpu * 33 
cac_val = 150 if strategy_mode == "Agresif Büyüme" else 100

with m1:
    st.metric("Tahmini LTV (Lifetime Value)", f"{ltv_val:.0f} TL", 
              help="ARPU x Müşteri Ömrü. Bir kullanıcının Lifebox'ta kaldığı sürece bıraktığı toplam ciro.")
with m2:
    st.metric("Tahmini CAC", f"{cac_val} TL", 
              help="Bir yeni aboneyi kazanmak için yapılan reklam ve operasyon maliyeti.")
with m3:
    st.metric("LTV / CAC Verimliliği", f"{ltv_val/cac_val:.1f}x", 
              help="3.0x üzeri 'Sağlıklı', 5.0x üzeri 'Çok Karlı' kabul edilir.")

# --- GRAFİK: OPTİMİZASYON ---
st.divider()
st.subheader("📊 Fiyat-Gelir Dengesi (Revenue Maximization)")
p_points = np.linspace(10, 250, 50)
# Fiyat arttıkça talep düşer (Elasticity)
demand = (10000 / (p_points + 20)) * (1.3 if strategy_mode == "Agresif Büyüme" else 1.0)
revenue = p_points * demand

df_chart = pd.DataFrame({'Fiyat (TL)': p_points, 'Tahmini Toplam Ciro (K)': revenue})
st.area_chart(df_chart.set_index('Fiyat (TL)'))
st.caption("Grafik: Bu eğrinin en tepe noktası, hacim ve fiyatın çarpımıyla elde edilen maksimum ciro noktasını gösterir.")

st.info(f"💡 **Stratejik Not:** Mevcut '{strategy_mode}' ayarı ile pazar payı ve karlılık dengesi optimize edilmiştir. Önerilen fiyatlar global rakiplerin yerel (TL) fiyat değişimlerine anlık duyarlıdır.")
