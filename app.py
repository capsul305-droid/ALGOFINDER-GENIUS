import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Pengaturan Halaman
st.set_page_config(page_title="ALGOFINDER GENIUS", layout="wide")

# CSS untuk tampilan gelap (dark mode) agar mirip aplikasi asli
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏆 ALGOFINDER GENIUS")
st.markdown("---")

# Input URL
url = st.text_input("Masukkan URL situs paito:")

if st.button("Jalankan Analisa"):
    if url:
        try:
            # Mengambil data dengan header agar tidak diblokir
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Mencari tabel di dalam halaman
            table = soup.find('table')
            if table:
                df = pd.read_html(str(table))[0]
                st.success("Data Paito Berhasil Dimuat!")
                st.dataframe(df.head(15)) # Tampilkan 15 data terakhir
                
                # Fitur Ringkasan Prediksi (4 Posisi)
                st.subheader("RINGKASAN PREDIKSI - 4 POSISI")
                
                # Membuat 4 kolom
                cols = st.columns(4)
                posisi = ["AS", "KOP", "KEPALA", "EKOR"]
                
                for i, col in enumerate(cols):
                    with col:
                        # Logika analisis: Mengambil angka paling dominan
                        # Anda bisa mengganti 'mode' dengan rumus matematika khusus Anda
                        nilai_kuat = df.iloc[:, i].mode()[0] if not df.empty else "-"
                        
                        st.info(posisi[i])
                        st.metric(label="KUAT-P", value=str(nilai_kuat))
                        st.write("Status: *Terkonfirmasi*")
            else:
                st.error("Tabel tidak ditemukan di URL tersebut.")
        except Exception as e:
            st.error(f"Terjadi kesalahan saat memproses data: {e}")
    else:
        st.warning("Silakan masukkan URL paito.")
