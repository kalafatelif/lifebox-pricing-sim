import streamlit as st
import pandas as pd
import numpy as np

# Tasarımı Güzelleştirelim
st.set_page_config(page_title="Lifebox Pricing Strategy", layout="wide")

# Kurumsal Tema Uygulaması
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1e2129; padding: 20px; border-radius: 10px; border: 1px solid #3e4451; }
    div[data-testid="stMetricValue"] { font-size: 40px; color: #007bff; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Lifebox Pricing War Room")
st.caption("Rakiplere ve Pazar Koşullarına Duyarlı Karar Destek Mekanizması")

# --- SOL PANEL: STRATEJİK GİRDİLER ---
with st.sidebar:
    st.header("📊 Market Verileri")
    lb_current = st.number_input("Lifebox Mevcut Fiyat (TL)", value=49.90)
    st.divider()
    google = st.number_input("Google One (100GB) TL", value=59.90)
    apple = st.number_input("iCloud+ (50GB) TL", value=39.90)
    
    st.divider()
    st.header("🎯 Strateji Ayarı")
    target_discount = st.slider("Piyasa Liderinden % İndirim Hedefi", 5, 50, 20)
    st.info("Bu slider, global rakiplerin en ucuzuna göre ne kadar agresif olacağımızı belirler.")

# --- MEKANİK: HESAPLAMA MOTORU ---
market_min = min(google, apple)
suggested_price = market_min * (1 - (target_discount / 100))

# --- TEPE NOKTASI: BÜYÜK ÖNERİ FİYATI ---
st.divider()
col_main = st.columns([1, 2, 1])
with col_main[1]:
    st.markdown(f"<h2 style='text-align: center;'>🎯 Önerilen Yeni Fiyat</h2>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align: center; font-size: 80px; color: #00ffcc;'>{suggested_price:.2f} TL</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center;'>Mevcut Fiyata Göre Değişim: %{((suggested_price/lb_current)-1)*100:.1f}</p>", unsafe_allow_html=True)
st.divider()

# --- SENARYOLAR ---
st.subheader("🚨 Senaryo Simülasyonu")
c1, c2, c3 = st.columns(3)
if 'scenario' not in st.session_state: st.session_state.scenario = "Normal"

if c1.button("📉 Devalüasyon (+%25 Maliyet)"): st.session_state.scenario = "Crash"
if c2.button("⚔️ Fiyat Savaşı (Rakip -%40)"): st.session_state.scenario = "War"
if c3.button("🔄 Normal Durum"): st.session_state.scenario = "Normal"

# Senaryo Etkileri
impact_msg = "Pazar stabil."
if st.session_state.scenario == "Crash":
    suggested_price *= 1.25
    impact_msg = "Döviz artışı maliyetleri vurdu, fiyat yukarı revize edildi."
elif st.session_state.scenario == "War":
    suggested_price *= 0.6
    impact_msg = "Rakip agresifleşti, pazar payı koruma moduna geçildi."

# --- SAĞ TARAF: FORMÜLLER VE METRİKLER ---
st.subheader("📈 Stratejik Metrikler ve Formüller")
m1, m2, m3 = st.columns(3)

with m1:
    st.metric("LTV (Lifetime Value)", "1.240 TL", help="Formül: ARPU x Müşteri Ömrü (Ay). Bir müşteriden toplamda kazanılan para.")
with m2:
    st.metric("CAC (Acquisition Cost)", "210 TL", help="Formül: Toplam Pazarlama Gideri / Yeni Müşteri Sayısı. Bir müşteriyi kazanma maliyeti.")
with m3:
    st.metric("LTV / CAC Oranı", f"{(suggested_price*12)/210:.1f}x", help="Formül: LTV / CAC. 3x üzeri sağlıklı kabul edilir.")

# --- GRAFİK: GELİR OPTİMİZASYONU ---
st.subheader("📊 Fiyat-Gelir Optimizasyonu (Hangi Fiyat Daha Çok Kazandırır?)")
price_points = np.linspace(10, 150, 30)
# Fiyat arttıkça kullanıcı azalır ama bir noktada gelir maksimum olur
revenue_curve = (price_points * (2000 / (price_points + 5))) 
df_chart = pd.DataFrame({'Fiyat (TL)': price_points, 'Tahmini Toplam Gelir (K)': revenue_curve})

st.area_chart(df_chart.set_index('Fiyat (TL)'))
st.caption("Grafik Açıklaması: Bu eğri, fiyatı çok düşük tutarsak sürümden kazandığımızı, çok yüksek tutarsak müşteri kaybettiğimizi gösterir. En tepe nokta 'Optimal Gelir' noktasıdır.")

st.info(f"💡 **Strateji Özeti:** {impact_msg}")
