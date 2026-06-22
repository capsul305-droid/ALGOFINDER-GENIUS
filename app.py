import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import io

# 1. Konfigurasi agar tampilan lebar dan bersih
st.set_page_config(page_title="ALGOFINDER GENIUS", layout="wide")

# 2. CSS untuk membuat tabel lebih padat dan berwarna seperti situs paito
st.markdown("""
    <style>
    /* Mengatur tabel agar lebih ringkas */
    .stDataFrame { font-size: 10px !important; }
    /* Warna latar belakang untuk meniru situs paito */
    .css-1r6slb0 { background-color: #f4f4f4; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏆 ALGOFINDER GENIUS")
url = st.text_input("Masukkan URL situs paito:")

# Fungsi untuk memberi warna pada angka (Pewarnaan otomatis)
def color_cells(val):
    # Contoh pewarnaan untuk angka tertentu
    colors = {
        '4': 'background-color: #ff0000; color: white;',
        '8': 'background-color: #0000ff; color: white;',
        '5': 'background-color: #008000; color: white;'
    }
    return colors.get(str(val), '')

if st.button("Jalankan Analisa"):
    if url:
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table', {'id': 'drawing-table'})
            
            if table:
                df = pd.read_html(io.StringIO(str(table)))[0]
                
                # Pembersihan data agar tampilan tidak berantakan
                df = df.applymap(lambda x: int(x) if isinstance(x, (int, float)) else x)
                
                st.subheader("Data Paito Warna")
                
                # Menampilkan tabel dengan gaya warna
                st.dataframe(df.style.map(color_cells), use_container_width=True)
                
            else:
                st.error("Tabel tidak ditemukan.")
        except Exception as e:
            st.error(f"Error: {e}")
