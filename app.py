import streamlit as st
import pandas as pd
import numpy as np

# Sayfa Ayarları
st.set_page_config(page_title="Lifebox Pricing Strategy", layout="wide")

st.title("🛡️ Lifebox Strategic Pricing Cockpit")
st.write("Rakiplere ve pazar hedeflerine göre optimize edilmiş fiyatlandırma modeli.")

# --- SOL PANEL: GİRDİLER ---
with st.sidebar:
    st.header("📊 Global Rakip Fiyatları")
    google = st.number_input("Google One (100GB) TL", value=59.99)
    apple = st.number_input("iCloud+ (50GB) TL", value=39.99)
    dropbox = st.number_input("Dropbox (2TB) TL", value=350.00)
    
    st.divider()
    st.header("🎯 Strateji Seçimi")
    strategy_mode = st.radio(
        "Pazar Hedefi Belirleyin:",
        ["Agresif Büyüme", "Dengeli", "Yüksek Karlılık"],
        index=1
    )
    st.caption("Bu seçim, rakiplerle aramızdaki fiyat farkını (Gap) otomatik ayarlar.")

# --- HESAPLAMA MANTIĞI ---
if strategy_mode == "Agresif Büyüme":
    gap_p1, gap_p2 = 0.45, 0.55
elif strategy_mode == "Dengeli":
    gap_p1, gap_p2 = 0.25, 0.35
else: # Yüksek Karlılık
    gap_p1, gap_p2 = 0.10, 0.15

# Paket Önerileri
# 250GB Paketi Apple'a göre, 2.5TB Paketi Dropbox birim fiyatına göre
suggested_p1 = apple * (1 - gap_p1)
suggested_p2 = (dropbox / 4) * (1 - gap_p2) # Dropbox 2TB, biz 2.5TB üzerinden normalize ediyoruz

# --- ANA EKRAN: ÖNERİLER ---
st.header(f"🎯 Önerilen Paket Fiyatları ({strategy_mode})")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📦 250 GB Paketi")
    st.metric(label="Önerilen Fiyat (Aylık)", value=f"{suggested_p1:.2f} TL")
    st.write(f"Hedef: Apple 50GB fiyatının %{gap_p1*100:.0f} altında kalmak.")

with col2:
    st.subheader("🚀 2.5 TB Paketi")
    st.metric(label="Önerilen Fiyat (Aylık)", value=f"{suggested_p2:.2f} TL")
    st.write(f"Hedef: Dropbox 2TB birim maliyetinin %{gap_p2*100:.0f} altında kalmak.")

# --- STRATEJİK METRİKLER ---
st.divider()
st.header("📈 Birim Ekonomi (Unit Economics)")

m1, m2, m3 = st.columns(3)

# Basit ama okunaklı LTV/CAC hesabı
avg_revenue = (suggested_p1 + suggested_p2) / 2
ltv = avg_revenue * 33 # 33 ay ortalama kalış süresi
cac = 150 if strategy_mode == "Agresif Büyüme" else 100

m1.metric("Tahmini LTV", f"{ltv:.0f} TL", help="Müşteri ömrü boyunca beklenen toplam ciro.")
m2.metric("Tahmini CAC", f"{cac} TL", help="Bir yeni aboneyi kazanma maliyeti.")
m3.metric("LTV / CAC Verimliliği", f"{ltv/cac:.1f}x")

# --- GRAFİK ---
st.divider()
st.header("📊 Gelir Potansiyeli Analizi")
p_points = np.linspace(10, 250, 50)
# Fiyat arttıkça talep düşer mantığıyla basit bir eğri
demand = (10000 / (p_points + 20)) * (1.3 if strategy_mode == "Agresif Büyüme" else 1.0)
revenue = p_points * demand

df_chart = pd.DataFrame({'Fiyat': p_points, 'Toplam Ciro Projeksiyonu': revenue})
st.line_chart(df_chart.set_index('Fiyat'))

st.info("💡 **Not:** Bu dashboard tamamen standart bileşenlerle kurulmuştur, tüm cihazlarda ve ışık modlarında sorunsuz okunur.")
