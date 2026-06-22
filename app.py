import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import io

# Konfigurasi Layout Profesional
st.set_page_config(page_title="ALGOFINDER GENIUS PRO", layout="wide")

# CSS Styling agar tampilan rapi, padat, dan nyaman di mata
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stDataFrame { font-size: 11px !important; }
    .css-1r6slb0 { font-size: 12px; }
    </style>
""", unsafe_allow_html=True)

st.title("🏆 ALGOFINDER GENIUS PRO")

# Dashboard Kontrol
col1, col2, col3 = st.columns(3)
with col1: st.selectbox("Pilih Pasar", ["Hongkong Pools", "Singapore", "Sydney"])
with col2: st.selectbox("Mode", ["Harian", "Mingguan"])
with col3: st.selectbox("Tampilan", ["Warna", "Hitam Putih"])

url = st.text_input("Masukkan URL situs paito:")

# Fungsi logika warna
def highlight_cells(val):
    target = ['4', '8', '5', '1', '9'] # Angka target
    if str(val) in target:
        return 'background-color: #ff4b4b; color: white; font-weight: bold'
    return ''

if st.button("RUN ENGINE"):
    if url:
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table', {'id': 'drawing-table'})
            
            if table:
                df = pd.read_html(io.StringIO(str(table)))[0]
                
                # Pembersihan angka menjadi format bulat (integer)
                df = df.map(lambda x: str(int(x)) if str(x).replace('.','',1).isdigit() else x)
                
                st.subheader("📊 Paito Visual Otomatis")
                
                # Menampilkan tabel
                styled_df = df.style.map(highlight_cells)
                st.dataframe(styled_df, use_container_width=True)
                
                st.success("Analisa selesai: Tabel paito telah diperbarui.")
                
            else:
                st.error("Tabel tidak ditemukan. Pastikan URL benar.")
        except Exception as e:
            st.error(f"Error Sistem: {e}")
