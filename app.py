import streamlit as st
import pandas as pd
import requests

# 1. Konfigurasi Halaman (Wide Layout untuk tampilan dasbor profesional)
st.set_page_config(layout="wide", page_title="Algofinder Genius")

# 2. CSS untuk Tampilan Gelap (Dark Theme) agar mirip referensi
st.markdown("""
    <style>
    .metric-card { background-color: #0b1a26; padding: 15px; border-radius: 10px; border: 1px solid #1f4769; margin-bottom: 10px; color: white; }
    .stApp { background-color: #050a0f; }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ ALGOFINDER GENIUS - DASHBOARD")

# 3. Fungsi Scraping & Engine Analisis
def scrape_paito(url):
    try:
        # Mengambil tabel dari URL
        dfs = pd.read_html(url)
        return dfs[0]
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        return None

def hitung_pola(series):
    # Mengubah data ke format angka untuk analisis
    series = pd.to_numeric(series, errors='coerce')
    diffs = series.diff()
    naik = (diffs > 0).sum()
    turun = (diffs < 0).sum()
    total = len(series) - 1
    
    # Menghitung kekuatan dan status tren
    kekuatan = (naik / total) * 100 if naik > turun else (turun / total) * 100
    status = "NAIK" if naik > turun else "TURUN"
    return kekuatan, status

# 4. Input Data (Sidebar)
with st.sidebar:
    st.subheader("INPUT DATA")
    url_input = st.text_input("URL Paito:")
    if st.button("RUN ENGINE"):
        data = scrape_paito(url_input)
        if data is not None:
            st.session_state['data'] = data
            st.success("Data Berhasil Dimuat!")

# 5. Tampilan Utama (Dashboard Layout)
if 'data' in st.session_state:
    df = st.session_state['data']
    
    # Layout 2 kolom: Kiri untuk Tabel, Kanan untuk Analisis
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.subheader("📊 Tabel Paito")
        st.dataframe(df, use_container_width=True, height=600)
    
    with col2:
        st.subheader("💡 Ringkasan Analisis")
        # Analisis per kolom (misal 4 kolom pertama: AS, KOP, KEPALA, EKOR)
        for col in df.columns[:4]:
            kekuatan, status = hitung_pola(df[col])
            with st.container():
                st.markdown(f'<div class="metric-card">', unsafe_allow_html=True)
                st.write(f"**Posisi: {col}**")
                st.progress(kekuatan/100)
                st.write(f"Tren: **{status}** | Kekuatan Pola: {kekuatan:.1f}%")
                st.markdown('</div>', unsafe_allow_html=True)
        
        st.subheader("📈 Grafik Tren")
        st.line_chart(df.iloc[:, :4])
else:
    st.info("Silakan masukkan URL Paito di sidebar dan tekan 'RUN ENGINE' untuk mulai menganalisis.")
