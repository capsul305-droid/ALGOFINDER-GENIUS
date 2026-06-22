import streamlit as st
import pandas as pd
import requests

# 1. Konfigurasi Layout
st.set_page_config(layout="wide", page_title="Algofinder Genius")

# 2. Fungsi Engine (Scraping & Analisis)
def get_data(url):
    # Mengambil data dari web
    try:
        dfs = pd.read_html(url)
        return dfs[0]
    except:
        return None

def hitung_kekuatan(series):
    # Contoh logika: mencari tren kenaikan (Naik)
    diffs = series.diff()
    naik = (diffs > 0).sum()
    total = len(series) - 1
    return (naik / total) * 100

# 3. Dasbor Utama
st.title("🛡️ ALGOFINDER GENIUS")

with st.sidebar:
    url = st.text_input("Masukkan URL Paito:")
    if st.button("RUN ENGINE"):
        data = get_data(url)
        if data is not None:
            st.session_state['df'] = data
        else:
            st.error("URL tidak valid atau tidak ada tabel.")

if 'df' in st.session_state:
    df = st.session_state['df']
    
    # Layout 2 Kolom
    col_kiri, col_kanan = st.columns([1, 1])
    
    with col_kiri:
        st.subheader("📊 Tabel Paito")
        st.dataframe(df, use_container_width=True)
        
    with col_kanan:
        st.subheader("💡 Analisis Pola")
        # Analisis otomatis per kolom
        for col in df.select_dtypes(include=['number']).columns:
            kekuatan = hitung_kekuatan(df[col])
            st.write(f"**Posisi: {col}**")
            st.progress(kekuatan/100)
            st.write(f"Kekuatan Pola: {kekuatan:.1f}%")
