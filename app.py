import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import io

st.set_page_config(page_config="wide")

# CSS "Paito Mode" - Memaksa tabel menjadi rapat dan padat
st.markdown("""
    <style>
    .stDataFrame {
        padding: 0 !important;
    }
    table {
        border-collapse: collapse !important;
        font-family: monospace !important;
    }
    td {
        width: 20px !important;
        height: 20px !important;
        padding: 1px !important;
        text-align: center !important;
        font-size: 10px !important;
    }
    .red-cell {
        background-color: #ff4444 !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏆 ALGOFINDER GENIUS - COMPACT")
url = st.text_input("Masukkan URL situs paito:")

def style_paito(val):
    # Mengubah warna latar belakang sel jika angka cocok
    if str(val) in ['4', '8', '5', '1', '9']:
        return 'background-color: #ff4444; color: white; font-weight: bold;'
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
                
                # Membersihkan data dari koma/titik desimal
                df = df.map(lambda x: str(int(x)) if str(x).replace('.','',1).isdigit() else x)
                
                # Menampilkan tabel dengan gaya kustom
                st.dataframe(df.style.map(style_paito), use_container_width=False, hide_index=True)
            else:
                st.error("Tabel tidak terbaca dengan benar.")
        except Exception as e:
            st.error(f"Error: {e}")
