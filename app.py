import streamlit as st
import pandas as pd
import requests

# 1. Konfigurasi Halaman (Layout Lebar)
st.set_page_config(layout="wide", page_title="Algofinder Genius")

# 2. Judul Dasbor
st.title("🛡️ ALGOFINDER GENIUS")

# 3. Fungsi Scraping (Mengambil data dari URL)
def get_paito_data(url):
    try:
        # Menggunakan pandas untuk membaca tabel dari URL
        dfs = pd.read_html(url)
        return dfs[0] 
    except Exception as e:
        st.error(f"Gagal mengambil data: {e}")
        return None

# 4. Layout 2 Kolom (Kiri: Input & Tabel, Kanan: Analisis)
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("INPUT DATA")
    url_input = st.text_input("Masukkan URL situs paito:")
    if st.button("RUN ENGINE"):
        if url_input:
            data = get_paito_data(url_input)
            if data is not None:
                st.session_state['data'] = data
                st.success("Data berhasil dimuat!")
            else:
                st.warning("Tabel tidak ditemukan di URL tersebut.")

    st.subheader("TABEL PAITO")
    if 'data' in st.session_state:
        st.dataframe(st.session_state['data'], use_container_width=True)

with col2:
    st.subheader("RINGKASAN ANALISIS POLA")
    if 'data' in st.session_state:
        df = st.session_state['data']
        # Logika Analisis Sederhana (contoh untuk kolom pertama)
        st.write("Analisis Posisi AS (Kolom 1):")
        # Logika: membandingkan baris saat ini dengan sebelumnya
        st.progress(0.45) # Bar kekuatan (contoh)
        st.write("Kekuatan Pola: 45% (NAIK)")
        
        st.markdown("---")
        st.write("Grafik Tren:")
        st.line_chart(df.iloc[:, 0]) # Grafik kolom pertama
    else:
        st.info("Masukkan URL dan klik RUN ENGINE untuk melihat hasil analisis.")
