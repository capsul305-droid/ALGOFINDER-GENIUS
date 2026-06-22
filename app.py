import streamlit as st
import pandas as pd

# Konfigurasi Layar (Wide)
st.set_page_config(layout="wide", page_title="Algofinder Genius")

st.title("🛡️ ALGOFINDER GENIUS - DASHBOARD")

# 1. Tempat Input Data
url = st.text_input("Masukkan URL situs paito:")
if st.button("RUN ENGINE"):
    # Logika scraping sederhana (sesuaikan dengan kebutuhan Anda)
    try:
        data = pd.read_html(url)[0]
        st.session_state['data'] = data
        st.success("Data berhasil dimuat!")
    except:
        st.error("Gagal memuat data. Periksa URL.")

# 2. Cek apakah ada data, jika ada maka tampilkan layout dua kolom
if 'data' in st.session_state:
    df = st.session_state['data']
    
    # Membuat Layout 2 Kolom (Kiri: Tabel, Kanan: Analisis)
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.subheader("📊 Tabel Paito")
        st.dataframe(df, use_container_width=True)
    
    with col2:
        st.subheader("💡 Ringkasan Analisis")
        # Contoh kotak kartu analisis (Anda bisa menduplikat ini untuk AS, KOP, dll)
        st.markdown("""
        <div style="background-color: #0b1a26; padding: 15px; border-radius: 10px; border: 1px solid #1f4769;">
            <h4 style="color: #4cc9f0;">AS (ANALISIS POLA)</h4>
            <p>Pola Naik: 45%</p>
            <p>Status: <b>KUAT</b></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.subheader("📈 Grafik Tren")
        # Grafik garis otomatis dari data
        st.line_chart(df.iloc[:, :4])
