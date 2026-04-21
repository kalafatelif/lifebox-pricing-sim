import streamlit as st
import pandas as pd
import numpy as np

# Sayfa Ayarları
st.set_page_config(page_title="Lifebox Pricing Strategy", layout="wide")

st.title("🛡️ Lifebox Strategic Pricing Cockpit")
st.write("Rakiplerle olan fiyat farkını anlık yönetin ve birim ekonomiyi analiz edin.")

# --- SOL PANEL: GİRDİLER ---
with st.sidebar:
    st.header("📊 Global Rakip Fiyatları")
    google = st.number_input("Google One (100GB) TL", value=59.99)
    apple = st.number_input("iCloud+ (50GB) TL", value=39.99)
    dropbox = st.number_input("Dropbox (2TB) TL", value=350.00)
    
    st.divider()
    st.header("🎯 Strateji Ayarı")
    # "Özel" seçeneği ile kullanıcı kendi indirimini belirleyebilir
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
suggested_p1 = apple * (1 - gap_p1)
suggested_p2 = (dropbox / 4) * (1 - gap_p2)

# --- ANA EKRAN: ÖNERİLER ---
st.header(f"🎯 Önerilen Paket Fiyatları")
col1, col2 = st.columns(2)

with col1:
    st.metric(label="📦 250 GB Paketi", value=f"{suggested_p1:.2f} TL")
    st.caption(f"Apple 50GB'dan %{gap_p1*100:.0f} daha ucuz.")

with col2:
    st.metric(label="🚀 2.5 TB Paketi", value=f"{suggested_p2:.2f} TL")
    st.caption(f"Dropbox 2TB (Birim) %{gap_p2*100:.0f} daha ucuz.")

# --- STRATEJİK KIYASLAMA TABLOSU ---
st.divider()
st.header("📋 Stratejik Karşılaştırma Tablosu")

comparison_data = {
    "Paket": ["250 GB", "2.5 TB"],
    "Önerilen Fiyat": [f"{suggested_p1:.2f} TL", f"{suggested_p2:.2f} TL"],
    "Google (100GB) Farkı": [f"%{((suggested_p1/google)-1)*100:.1f}", f"%{((suggested_p2/google)-1)*100:.1f}"],
    "Apple (50GB) Farkı": [f"%{((suggested_p1/apple)-1)*100:.1f}", f"%{((suggested_p2/apple)-1)*100:.1f}"],
    "Dropbox (Birim) Farkı": [f"%{((suggested_p1/(dropbox/20))-1)*100:.1f}", f"%{((suggested_p2/(dropbox/0.8))-1)*100:.1f}"]
}

df_comp = pd.DataFrame(comparison_data)
st.table(df_comp) # st.table her zaman en net ve okunaklı tablodur.

# --- BİRİM EKONOMİ (UNIT ECONOMICS) ---
st.divider()
st.header("📈 Birim Ekonomi Analizi")
m1, m2, m3 = st.columns(3)

avg_revenue = (suggested_p1 + suggested_p2) / 2
ltv = avg_revenue * 33 
cac = 150 if strategy_mode == "Agresif Büyüme" else 100

m1.metric("Tahmini LTV", f"{ltv:.0f} TL")
m2.metric("Tahmini CAC", f"{cac} TL")
m3.metric("LTV / CAC Skoru", f"{ltv/cac:.1f}x")

# --- GRAFİK ---
st.divider()
st.header("📊 Toplam Gelir Projeksiyonu")
p_points = np.linspace(10, 250, 50)
demand = (10000 / (p_points + 20)) * (1.3 if strategy_mode == "Agresif Büyüme" else 1.0)
revenue = p_points * demand

df_chart = pd.DataFrame({'Fiyat': p_points, 'Gelir': revenue})
st.line_chart(df_chart.set_index('Fiyat'))

st.info("💡 **PM Notu:** Tablodaki negatif yüzdeler rakipten daha ucuz olduğumuzu, pozitifler ise daha pahalı olduğumuzu gösterir.")
