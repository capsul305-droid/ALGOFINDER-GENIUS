import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import io

# Konfigurasi Halaman
st.set_page_config(page_title="ALGOFINDER GENIUS", layout="wide")

st.title("🏆 ALGOFINDER GENIUS")

url = st.text_input("Masukkan URL situs paito:")

if st.button("Jalankan Analisa"):
    if url:
        try:
            # Mengambil data web
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Mencari tabel spesifik berdasarkan id yang muncul di error Anda
            table = soup.find('table', {'id': 'drawing-table'})
            
            if table:
                # Mengubah HTML menjadi string, lalu menjadi file virtual (io.StringIO)
                # sehingga pandas bisa membacanya sebagai tabel
                html_str = str(table)
                df = pd.read_html(io.StringIO(html_str))[0]
                
                st.success("Tabel Berhasil Dimuat!")
                st.dataframe(df) # Menampilkan tabel agar Anda bisa cek isinya
                
                # Sisa logika analisis Anda bisa diletakkan di bawah sini
                st.info("Data berhasil diproses ke dalam tabel.")
                
            else:
                st.error("Tabel dengan ID 'drawing-table' tidak ditemukan di URL tersebut.")
                
        except Exception as e:
            st.error(f"Terjadi kesalahan saat memproses data: {e}")
    else:
        st.warning("Masukkan URL terlebih dahulu.")
