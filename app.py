import streamlit as st
import pandas as pd
import numpy as np

# Sayfa Ayarları
st.set_page_config(page_title="Lifebox Growth & Pricing Simulator", layout="wide")

st.title("🛡️ Lifebox Growth & Pricing Simulator")
st.write("ARPU ve Tenure bazlı dinamik gelir projeksiyonu ve pazar analizi.")

# --- SOL PANEL: GİRDİLER ---
with st.sidebar:
    st.header("📊 Rakip & Market Verileri")
    google = st.number_input("Google One (100GB) TL", value=59.99)
    apple = st.number_input("iCloud+ (50GB) TL", value=39.99)
    dropbox = st.number_input("Dropbox (2TB) TL", value=350.00)
    
    st.divider()
    st.header("⚙️ Projeksiyon Parametreleri")
    # Kullanıcının elle müdahale edebileceği ARPU ve Tenure alanları
    manual_arpu = st.number_input("Hedef Ortalama ARPU (TL)", value=45.0)
    manual_tenure = st.number_input("Hedef Ortalama Tenure (Ay)", value=24)
    total_users = st.number_input("Hedef Abone Sayısı", value=100000)

    st.divider()
    st.header("🎯 Strateji Ayarı")
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
    else: # Yüksek Karlılık
        gap_p1, gap_p2 = 0.10, 0.15

# --- HESAPLAMALAR ---
suggested_p1 = apple * (1 - gap_p1)
suggested_p2 = (dropbox / 4) * (1 - gap_p2)

# --- ANA EKRAN: ÖNERİLER ---
st.header("🎯 Önerilen Paket Fiyatları")
col1, col2 = st.columns(2)

with col1:
    st.metric(label="📦 250 GB Paketi", value=f"{suggested_p1:.2f} TL")
    st.caption(f"Apple 50GB'dan %{gap_p1*100:.0f} indirimli.")

with col2:
    st.metric(label="🚀 2.5 TB Paketi", value=f"{suggested_p2:.2f} TL")
    st.caption(f"Dropbox 2TB (Birim) %{gap_p2*100:.0f} indirimli.")

# --- KIYASLAMA TABLOSU ---
st.divider()
st.header("📋 Stratejik Karşılaştırma Tablosu")
comparison_data = {
    "Paket": ["250 GB", "2.5 TB"],
    "Önerilen Fiyat": [f"{suggested_p1:.2f} TL", f"{suggested_p2:.2f} TL"],
    "Google Farkı": [f"%{((suggested_p1/google)-1)*100:.1f}", f"%{((suggested_p2/google)-1)*100:.1f}"],
    "Apple Farkı": [f"%{((suggested_p1/apple)-1)*100:.1f}", f"%{((suggested_p2/apple)-1)*100:.1f}"],
    "Dropbox Farkı": [f"%{((suggested_p1/(dropbox/20))-1)*100:.1f}", f"%{((suggested_p2/(dropbox/0.8))-1)*100:.1f}"]
}
st.table(pd.DataFrame(comparison_data))

# --- BİRİM EKONOMİ (ELLE GİRİLEN VERİLERLE) ---
st.divider()
st.header("📈 Büyüme Motoru Verileri")
m1, m2, m3 = st.columns(3)

# LTV artık tamamen senin girdiğin manual_arpu ve manual_tenure'dan besleniyor
ltv = manual_arpu * manual_tenure
cac = 150 if strategy_mode == "Agresif Büyüme" else 100

m1.metric("LTV (Lifetime Value)", f"{ltv:.0f} TL", help="ARPU x Tenure")
m2.metric("CAC", f"{cac} TL")
m3.metric("LTV / CAC", f"{ltv/cac:.1f}x")

# --- GRAFİK: ZAMANA BAĞLI GELİR PROJEKSİYONU ---
st.divider()
st.header("📊 Kümülatif Gelir Projeksiyonu")
st.write(f"Abone Sayısı: {total_users:,} | ARPU: {manual_arpu} TL | Tenure: {manual_tenure} Ay")

# Zaman içindeki kümülatif geliri gösteren bir tablo
months = np.arange(1, manual_tenure + 1)
monthly_revenue = total_users * manual_arpu
cumulative_revenue = months * monthly_revenue

df_proj = pd.DataFrame({
    'Ay': months,
    'Kümülatif Gelir (Mn TL)': cumulative_revenue / 1_000_000
})

st.line_chart(df_proj.set_index('Ay'))
st.caption("Bu grafik, girdiğiniz ARPU ve Abone sayısı ile belirlenen süre (Tenure) boyunca birikecek toplam nakit akışını gösterir.")

st.info("💡 **PM Notu:** Projeksiyon parametrelerini sol panelden değiştirerek farklı Tenure senaryolarını test edebilirsiniz.")
