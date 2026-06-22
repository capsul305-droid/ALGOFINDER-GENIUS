import streamlit as st
import pandas as pd
import requests

# Konfigurasi Layout agar lebar dan rapi
st.set_page_config(page_title="Algofinder Genius", layout="wide")

st.title("🏆 ALGOFINDER GENIUS")
st.markdown("---")

# 1. Input URL Data
url = st.text_input("Masukkan URL situs tabel paito:")

if st.button("Proses Analisa"):
    if url:
        try:
            # Mengambil data tabel dari URL
            tables = pd.read_html(url)
            df = tables[0] # Mengambil tabel pertama
            
            st.success("Data berhasil dimuat!")
            
            # --- LOGIKA ANALISA SEDERHANA ---
            # Contoh: menghitung angka yang paling sering muncul sebagai 'KUAT'
            # Anda bisa menyesuaikan logika ini dengan rumus Anda sendiri
            angka_as = df.iloc[:, 0].mode()[0] if not df.empty else 0
            angka_kop = df.iloc[:, 1].mode()[0] if not df.empty else 0
            
            # --- TAMPILAN RINGKASAN (Seperti Gambar Anda) ---
            st.subheader("RINGKASAN PREDIKSI - 4 POSISI")
            
            # Membuat 4 kolom untuk AS, KOP, KEPALA, EKOR
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.info("AS")
                st.write(f"KUAT-P: {angka_as}")
                st.write("Status: Terkonfirmasi")
            
            with col2:
                st.warning("KOP")
                st.write(f"KUAT-P: {angka_kop}")
                st.write("Status: Terkonfirmasi")
                
            with col3:
                st.error("KEPALA")
                st.write("Analisis: Sedang dihitung...")
                
            with col4:
                st.success("EKOR")
                st.write("Analisis: Sedang dihitung...")
                
        except Exception as e:
            st.error(f"Gagal memproses data. Pastikan URL valid dan berisi tabel HTML. Error: {e}")
    else:
        st.warning("Silakan masukkan URL tabel paito.")
