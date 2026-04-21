import streamlit as st
import pandas as pd
import numpy as np

# Tasarımı Güzelleştirelim
st.set_page_config(page_title="Lifebox Pricing Strategy", layout="wide")

# CSS ile biraz "Corporate & Dark" hava katalım
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #262730; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Lifebox Pricing War Room")
st.caption("Rakiplere ve Pazar Koşullarına Duyarlı Parametrik Fiyatlandırma Modeli")

# --- SOL PANEL: STRATEJİK GİRDİLER ---
with st.sidebar:
    st.header("📊 Global Rakip Benchmarks")
    google = st.number_input("Google One (100GB) TL", value=59.90)
    apple = st.number_input("iCloud+ (50GB) TL", value=39.90)
    dropbox = st.number_input("Dropbox (2TB) TL", value=350.0)
    
    st.divider()
    st.header("🎯 Lifebox Konumlandırma")
    target_discount = st.slider("Pazar Liderinden % İndirim Hedefi", 5, 50, 25)
    retention_focus = st.select_slider("Stratejik Odak", options=["Agresif Büyüme", "Dengeli", "Yüksek Karlılık"])

# --- MEKANİK: HESAPLAMA MOTORU ---
# En ucuz global rakibi baz alan 'Underdog' algoritması
market_min = min(google, apple)
suggested_price = market_min * (1 - (target_discount / 100))

# --- ANA EKRAN: SENARYO BUTONLARI ---
st.subheader("🚨 Pazar Senaryolarını Simüle Et")
c1, c2, c3, c4 = st.columns(4)

# Butonların durumlarını session_state ile tutalım ki "oynak" olsunlar
if 'scenario' not in st.session_state: st.session_state.scenario = "Normal"

if c1.button("📉 Devalüasyon"): st.session_state.scenario = "Crash"
if c2.button("⚔️ Fiyat Savaşı"): st.session_state.scenario = "War"
if c3.button("🌟 Google Değişikliği"): st.session_state.scenario = "Opportunity"
if c4.button("🔄 Reset"): st.session_state.scenario = "Normal"

# Senaryo Etkileri
impact_msg = "Pazar stabil seyrediyor."
status_color = "info"

if st.session_state.scenario == "Crash":
    suggested_price *= 1.2
    impact_msg = "UYARI: Operasyonel maliyetler %20 arttı. Fiyat yukarı revize edildi."
    st.error(impact_msg)
elif st.session_state.scenario == "War":
    suggested_price *= 0.7
    impact_msg = "Rakipler kampanya başlattı! Pazar payını korumak için fiyat aşağı çekildi."
    st.warning(impact_msg)
elif st.session_state.scenario == "Opportunity":
    target_discount = 5 # Rakip alanı daralttığı için indirime gerek kalmadı
    suggested_price = market_min * 0.95
    impact_msg = "Google alanı kısıtladı! Organik talep artıyor, yüksek fiyatla kar maksimizasyonu mümkün."
    st.success(impact_msg)

# --- GÖSTERGELER ---
st.divider()
m1, m2, m3 = st.columns(3)
m1.metric("Önerilen Lifebox Fiyatı", f"{suggested_price:.2f} TL", f"-{target_discount}% vs Rakip")
m2.metric("Tahmini Market Share Etkisi", "+%14" if suggested_price < market_min else "-%5")
m3.metric("LTV / CAC Projeksiyonu", "3.8x" if st.session_state.scenario != "War" else "2.1x")

# --- GRAFİK ---
st.subheader("📈 Fiyat Hassasiyet Analizi")
price_range = np.linspace(10, 100, 20)
# Basit bir talep eğrisi: Fiyat düştükçe abone artar
subs_growth = (1000 / (price_range + 5)) * (1.5 if st.session_state.scenario == "Opportunity" else 1.0)
df_chart = pd.DataFrame({'Fiyat': price_range, 'Tahmini Yeni Abone (K)': subs_growth})
st.area_chart(df_chart.set_index('Fiyat'))

st.write(f"**Strateji Notu:** Şu anki pazar koşullarında '{st.session_state.scenario}' senaryosu aktif. {impact_msg}")
