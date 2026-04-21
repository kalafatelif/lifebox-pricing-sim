import streamlit as st
import pandas as pd
import numpy as np

# Sayfa Ayarları
st.set_page_config(page_title="Lifebox Pricing Öneri Modeli", layout="wide")

# Başlık
st.title("🛡️ Lifebox Pricing Öneri Modeli")
st.write("Rakiplerle olan fiyat farkını anlık yönetin ve büyüme metrikleri üzerinden gelir projeksiyonu oluşturun.")

# --- SOL PANEL: GİRDİLER ---
with st.sidebar:
    st.header("📊 Market & Rakip Verileri")
    google = st.number_input("Google One (100GB) TL", value=59.99)
    apple = st.number_input("iCloud+ (50GB) TL", value=39.99)
    dropbox = st.number_input("Dropbox (2TB) TL", value=350.00)
    
    st.divider()
    st.header("⚙️ Growth Parametreleri")
    # Elle girilebilen ARPU ve Tenure alanları
    manual_arpu = st.number_input("Hedef Ortalama ARPU (TL)", value=45.0)
    manual_tenure = st.number_input("Hedef Ortalama Tenure (Ay)", value=24)
    total_users = st.number_input("Hedef Abone Sayısı", value=100000)

    st.divider()
    st.header("🎯 Stratejik Konumlandırma")
    strategy_mode = st.radio(
        "Pazar Hedefi Belirleyin:",
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
    else: # Yüksek Karlılık
        gap_p1, gap_p2 = 0.10, 0.15

# --- HESAPLAMALAR ---
# 250GB Paketi Apple bazlı, 2.5TB Paketi Dropbox bazlı hesaplanır
suggested_p1 = apple * (1 - gap_p1)
suggested_p2 = (dropbox / 4) * (1 - gap_p2)

# --- ANA EKRAN: FİYAT ÖNERİLERİ ---
st.header("🎯 Paket Fiyat Önerileri")
col1, col2 = st.columns(2)

with col1:
    st.metric(label="📦 250 GB Paketi", value=f"{suggested_p1:.2f} TL")
    st.caption(f"Apple 50GB fiyatından %{gap_p1*100:.0f} daha ucuz.")

with col2:
    st.metric(label="🚀 2.5 TB Paketi", value=f"{suggested_p2:.2f} TL")
    st.caption(f"Dropbox 2TB birim maliyetinden %{gap_p2*100:.0f} daha ucuz.")

# --- STRATEJİK TABLO ---
st.divider()
st.header("📋 Karşılaştırmalı Pazar Analizi")
comparison_data = {
    "Paket Segmenti": ["250 GB (Giriş)", "2.5 TB (Yüksek Kapasite)"],
    "Önerilen Fiyat": [f"{suggested_p1:.2f} TL", f"{suggested_p2:.2f} TL"],
    "Google (100GB) Kıyas": [f"%{((suggested_p1/google)-1)*100:.1f}", f"%{((suggested_p2/google)-1)*100:.1f}"],
    "Apple (50GB) Kıyas": [f"%{((suggested_p1/apple)-1)*100:.1f}", f"%{((suggested_p2/apple)-1)*100:.1f}"],
    "Dropbox (Birim) Kıyas": [f"%{((suggested_p1/(dropbox/20))-1)*100:.1f}", f"%{((suggested_p2/(dropbox/0.8))-1)*100:.1f}"]
}
st.table(pd.DataFrame(comparison_data))

# --- UNIT ECONOMICS ---
st.divider()
st.header("📈 Birim Ekonomi ve LTV")
m1, m2, m3 = st.columns(3)

# LTV hesabı artık tamamen senin girdiğin ARPU ve Tenure üzerinden
ltv_calculated = manual_arpu * manual_tenure
cac_estimated = 150 if strategy_mode == "Agresif Büyüme" else 100

m1.metric("LTV (Lifetime Value)", f"{ltv_calculated:.0f} TL", help="Formül: Manuel ARPU x Manuel Tenure")
m2.metric("Tahmini CAC", f"{cac_estimated} TL")
m3.metric("LTV / CAC Verimliliği", f"{ltv_calculated/cac_estimated:.1f}x")

# --- GELİR PROJEKSİYONU GRAFİĞİ ---
st.divider()
st.header("📊 Kümülatif Gelir Projeksiyonu")
st.write(f"Hedef: {total_users:,} Abone | Dönemsel Gelir Hedefi")

months = np.arange(1, manual_tenure + 1)
monthly_rev = total_users * manual_arpu
cumulative_rev = months * monthly_rev

df_proj = pd.DataFrame({
    'Ay': months,
    'Kümülatif Gelir (Milyon TL)': cumulative_rev / 1_000_000
})

st.line_chart(df_proj.set_index('Ay'))
st.info("💡 Not: Grafik üzerindeki veriler sol panelde girdiğiniz ARPU, Tenure ve Abone Sayısı değerlerine göre anlık güncellenir.")
