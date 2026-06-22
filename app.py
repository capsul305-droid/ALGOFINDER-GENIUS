import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import io

# Konfigurasi halaman agar memaksimalkan lebar layar
st.set_page_config(page_title="ALGOFINDER GENIUS PRO", layout="wide")

# CSS KUSTOM UNTUK MEMADATKAN TABEL
st.markdown("""
    <style>
    /* Mengurangi margin dan padding agar tabel rapat */
    .stApp { background-color: #ffffff; color: #000000; }
    div.stDataFrame { padding: 0px !important; }
    
    /* Mengatur font agar sangat kecil dan rapat seperti paito asli */
    table { font-size: 10px !important; border-collapse: collapse !important; }
    td, th { padding: 2px 4px !important; text-align: center !important; }
    
    /* Style untuk kotak merah */
    .red-cell { background-color: #ff4b4b !important; color: white !important; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.title("🏆 ALGOFINDER GENIUS - PRO")

url = st.text_input("Masukkan URL situs paito:")

def style_paito(val):
    # Logika warna yang lebih spesifik
    target = ['4', '8', '5', '1', '9']
    if str(val) in target:
        return 'background-color: #ff4b4b; color: white; font-weight: bold;'
    return 'color: #333;'

if st.button("RUN ENGINE"):
    if url:
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table', {'id': 'drawing-table'})
            
            if table:
                df = pd.read_html(io.StringIO(str(table)))[0]
                
                # Pembersihan data agar sel tidak meluas
                df = df.map(lambda x: str(int(x)) if str(x).replace('.','',1).isdigit() else x)
                
                st.subheader("📊 Analisa Paito Visual")
                
                # Menampilkan tabel dengan gaya 'compact'
                styled_df = df.style.map(style_paito)
                st.dataframe(styled_df, use_container_width=True, hide_index=True)
                
            else:
                st.error("Tabel tidak ditemukan. Pastikan URL target benar.")
        except Exception as e:
            st.error(f"Sistem Error: {e}")
