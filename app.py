import streamlit as st
import pandas as pd
import numpy as np

# Sayfa Ayarları
st.set_page_config(page_title="Lifebox Pricing Öneri Modeli", layout="wide")

st.title("🛡️ Lifebox Pricing Öneri Modeli")

# --- SOL PANEL: GİRDİLER ---
with st.sidebar:
    st.header("📊 Market & Rakip Verileri")
    google = st.number_input("Google One (100GB) TL", value=59.99)
    apple = st.number_input("iCloud+ (50GB) TL", value=39.99)
    dropbox = st.number_input("Dropbox (2TB) TL", value=350.00)
    
    st.divider()
    st.header("⚙️ Growth Parametreleri")
    manual_arpu = st.number_input("Hedef Ortalama ARPU (TL)", value=45.0)
    manual_tenure = st.number_input("Hedef Ortalama Tenure (Ay)", value=24)
    total_users = st.number_input("Hedef Abone Sayısı", value=100000)

    st.divider()
    st.header("🎯 Stratejik Konumlandırma")
    strategy_mode = st.radio(
        "Pazar Hedefi:",
        ["Agresif Büyüme", "Dengeli", "Yüksek Karlılık", "Özel (Manuel)"],
        index=1
    )
    
    if strategy_mode == "Özel (Manuel)":
        manual_gap = st.slider("Özel İndirim Oranı (%)", 0, 80, 20)
        gap_p1 = gap_p2 = manual_gap / 100
    elif strategy_mode == "Agresif Büyüme":
        gap_p1, gap_p2 = 0.45, 0.55
    elif strategy_mode == "Dengeli":
        gap_p1, gap_p2 = 0.25, 0.35
    else:
        gap_p1, gap_p2 = 0.10, 0.15

# --- HESAPLAMALAR ---
suggested_p1 = apple * (1 - gap_p1)
suggested_p2 = (dropbox / 4) * (1 - gap_p2) # 2.5TB'ı 2TB'lık Dropbox'a göre oranlıyoruz

# Birim Fiyatlar (TL/GB)
lb_unit_p1 = suggested_p1 / 250
lb_unit_p2 = suggested_p2 / 2500
google_unit = google / 100
apple_unit = apple / 50
dropbox_unit = dropbox / 2000

# --- ANA EKRAN: ÖNERİLER ---
st.header("🎯 Paket Fiyat Önerileri")
col1, col2 = st.columns(2)
with col1:
    st.metric(label="📦 250 GB Paketi", value=f"{suggested_p1:.2f} TL")
with col2:
    st.metric(label="🚀 2.5 TB Paketi", value=f"{suggested_p2:.2f} TL")

# --- TABLO 1: TOPLAM FİYAT KIYASI ---
st.divider()
st.header("📋 Tablo 1: Toplam Fiyat Kıyası (Cüzdan Payı)")
st.write("Müşterinin cebinden çıkacak toplam TL tutarının rakiplerle kıyaslanması.")

df_total = pd.DataFrame({
    "Paket": ["250 GB", "2.5 TB"],
    "Lifebox Öneri": [f"{suggested_p1:.2f} TL", f"{suggested_p2:.2f} TL"],
    "Google (100GB)": [f"{google:.2f} TL", f"{google:.2f} TL"],
    "Apple (50GB)": [f"{apple:.2f} TL", f"{apple:.2f} TL"],
    "Dropbox (2TB)": [f"{dropbox:.2f} TL", f"{dropbox:.2f} TL"]
})
st.table(df_total)

# --- TABLO 2: BİRİM FİYAT KIYASI ---
st.divider()
st.header("⚖️ Tablo 2: Birim Fiyat Kıyası (1 GB Maliyeti)")
st.write("Verimlilik odaklı kullanıcılar için 1 GB başına düşen TL maliyeti.")

df_unit = pd.DataFrame({
    "Paket": ["250 GB", "2.5 TB"],
    "Lifebox (TL/GB)": [f"{lb_unit_p1:.3f}", f"{lb_unit_p2:.3f}"],
    "Google (TL/GB)": [f"{google_unit:.3f}", f"{google_unit:.3f}"],
    "Apple (TL/GB)": [f"{apple_unit:.3f}", f"{apple_unit:.3f}"],
    "Dropbox (TL/GB)": [f"{dropbox_unit:.3f}", f"{dropbox_unit:.3f}"]
})
st.table(df_unit)

# --- UNIT ECONOMICS ---
st.divider()
st.header("📈 Birim Ekonomi ve LTV")
m1, m2, m3 = st.columns(3)
ltv_calculated = manual_arpu * manual_tenure
cac_estimated = 150 if strategy_mode == "Agresif Büyüme" else 100
m1.metric("LTV (Lifetime Value)", f"{ltv_calculated:.0f} TL")
m2.metric("Tahmini CAC", f"{cac_estimated} TL")
m3.metric("LTV / CAC Oranı", f"{ltv_calculated/cac_estimated:.1f}x")

# --- GRAFİK ---
st.divider()
st.header("📊 Kümülatif Gelir Projeksiyonu")
months = np.arange(1, manual_tenure + 1)
cumulative_rev = months * (total_users * manual_arpu)
df_proj = pd.DataFrame({'Ay': months, 'Milyon TL': cumulative_rev / 1_000_000})
st.line_chart(df_proj.set_index('Ay'))
