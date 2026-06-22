import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import io

# 1. Konfigurasi halaman
st.set_page_config(page_title="ALGOFINDER GENIUS", layout="wide")

# 2. CSS untuk membuat tampilan "Ultra-Compact" (mirip kertas paito)
st.markdown("""
    <style>
    /* Hilangkan padding default streamlit */
    .block-container { padding-top: 1rem !important; }
    
    /* Grid Paito: Membuat tabel sangat rapat */
    div[data-testid="stDataFrame"] { padding: 0 !important; }
    table {
        border-collapse: collapse !important;
        width: auto !important;
        font-family: monospace !important;
    }
    td {
        width: 28px !important;
        height: 28px !important;
        padding: 0px !important;
        text-align: center !important;
        border: 1px solid #ddd !important;
        font-size: 12px !important;
        color: #333;
    }
    /* Warna sel untuk pola */
    .red-cell { background-color: #ff4444 !important; color: white !important; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.title("🏆 ALGOFINDER GENIUS - PRO GRID")

url = st.text_input("Masukkan URL situs paito:")

def style_paito(df):
    # Logika pewarnaan sel berdasarkan pola
    return df.style.map(lambda x: 'background-color: #ff4444; color: white; font-weight: bold;' 
                        if str(x) in ['4', '8', '5', '1', '9'] else '')

if st.button("RUN ENGINE"):
    if url:
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table', {'id': 'drawing-table'})
            
            if table:
                df = pd.read_html(io.StringIO(str(table)))[0]
                
                # Pembersihan angka (buang desimal)
                df = df.map(lambda x: str(int(float(x))) if str(x).replace('.','',1).isdigit() else x)
                
                # Tampilkan tabel tanpa indeks
                # Gunakan st.write untuk tabel agar lebih fleksibel dengan CSS kita
                styled_table = style_paito(df)
                st.write(styled_table.to_html(index=False), unsafe_allow_html=True)
                
            else:
                st.error("Tabel tidak ditemukan.")
        except Exception as e:
            st.error(f"Error Sistem: {e}")
