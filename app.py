import streamlit as st
import pandas as pd
import numpy as np

# Sayfa Ayarları
st.set_page_config(page_title="Lifebox Pricing Öneri Modeli", layout="wide")

# --- GÜVENLİK PROTOKOLÜ (ŞİFRE KORUMASI) ---
def check_password():
    """Kullanıcı doğru şifreyi girene kadar dashboard'u gizler."""
    def password_entered():
        """Şifre kontrol fonksiyonu"""
        if st.session_state["password"] == "Lifebox2026":  # ŞİFREN BURASI! İstediğinle değiştirebilirsin.
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Şifreyi session'dan temizle
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # Şifre henüz girilmediyse giriş ekranını göster
        st.markdown("<h2 style='text-align: center;'>🔐 Stratejik Karar Destek Sistemi</h2>", unsafe_allow_html=True)
        st.text_input("Lütfen Giriş Şifresini Yazın", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        # Şifre yanlış girildiyse hata göster ve tekrar sor
        st.markdown("<h2 style='text-align: center;'>🔐 Stratejik Karar Destek Sistemi</h2>", unsafe_allow_html=True)
        st.text_input("Lütfen Giriş Şifresini Yazın", type="password", on_change=password_entered, key="password")
        st.error("❌ Hatalı Şifre. Lütfen tekrar deneyin.")
        return False
    else:
        return True

# Şifre kontrolü geçilemezse kodu durdur
if not check_password():
    st.stop()

# --- ŞİFRE DOĞRUYSA AŞAĞIDAKİ DASHBOARD YÜKLENİR ---

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
    manual_arpu = st.number_input("Hedef Ortalama ARPU (TL)", value=45.0)
    manual_tenure = st.number_input("Hedef Ortalama Tenure (Ay)", value=24)
    total_users = st.number_input("Hedef Abone Sayısı", value=100000)

    st.divider()
    st.header("🎯 Stratejik Konumlandırma")
    strategy_mode = st.radio(
        "Pazar Hedefi Belirleyin:",
        [
            "Agresif Büyüme (Rakipten %45-%55 ucuz / Pazar payı odaklı)", 
            "Dengeli (Rakipten %25-%35 ucuz / Sürdürülebilir büyüme)", 
            "Yüksek Karlılık (Rakipten %10-%15 ucuz / Marj odaklı)", 
            "Özel (Manuel)"
        ],
        index=1
    )
    
    if "Özel" in strategy_mode:
        manual_gap = st.slider("Özel İndirim Oranı (%)", 0, 80, 20)
        gap_p1 = gap_p2 = manual_gap / 100
    elif "Agresif" in strategy_mode:
        gap_p1, gap_p2 = 0.45, 0.55
    elif "Dengeli" in strategy_mode:
        gap_p1, gap_p2 = 0.25, 0.35
    else:
        gap_p1, gap_p2 = 0.10, 0.15

# --- HESAPLAMALAR ---
suggested_p1 = apple * (1 - gap_p1)
suggested_p2 = (dropbox / 4) * (1 - gap_p2) 

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

# --- TABLOLAR ---
st.divider()
st.header("📋 Tablo 1: Toplam Fiyat Kıyası (Cüzdan Payı)")
df_total = pd.DataFrame({
    "Paket": ["250 GB", "2.5 TB"],
    "Lifebox Öneri": [f"{suggested_p1:.2f} TL", f"{suggested_p2:.2f} TL"],
    "Google (100GB)": [f"{google:.2f} TL", f"{google:.2f} TL"],
    "Apple (50GB)": [f"{apple:.2f} TL", f"{apple:.2f} TL"],
    "Dropbox (2TB)": [f"{dropbox:.2
