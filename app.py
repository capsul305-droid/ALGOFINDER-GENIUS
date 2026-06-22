import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import io

st.set_page_config(page_title="ALGOFINDER GENIUS", layout="wide")

st.title("🏆 ALGOFINDER GENIUS")

url = st.text_input("Masukkan URL situs paito:")

if st.button("Jalankan Analisa"):
    if url:
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # MENCARI TABEL SECARA SPESIFIK (berdasarkan id di foto Anda)
            table = soup.find('table', {'id': 'drawing-table'})
            
            if table:
                # Mengonversi tabel menjadi dataframe
                df = pd.read_html(str(table))[0]
                st.success("Tabel Berhasil Ditemukan!")
                st.dataframe(df) # Menampilkan tabel agar Anda bisa melihat apakah datanya benar
                
                # Di sini Anda bisa mulai menambahkan logika analisis 
                # (misalnya menghitung pola AS, KOP, KEPALA, EKOR)
                st.info("Tabel dimuat. Anda sekarang bisa menambahkan rumus analisis di bawah ini.")
            else:
                st.error("Tabel dengan id 'drawing-table' tidak ditemukan. Pastikan URL benar.")
                
        except Exception as e:
            st.error(f"Error: {e}")
