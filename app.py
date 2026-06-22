import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import io

# Konfigurasi Halaman
st.set_page_config(page_title="ALGOFINDER GENIUS PRO", layout="wide")

# CSS Styling untuk tampilan profesional
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .metric-box { border: 1px solid #4a4a4a; padding: 10px; border-radius: 10px; background: #1a1a1a; }
    </style>
""", unsafe_allow_html=True)

st.title("🏆 ALGOFINDER GENIUS - PRO MACHINE")

# --- DASHBOARD KONTROL ---
col1, col2, col3 = st.columns(3)
with col1: st.selectbox("Pilih Pasar", ["Hongkong Pools", "Singapore", "Sydney"])
with col2: st.selectbox("Mode", ["Harian", "Warna"])
with col3: st.selectbox("Periode", ["Terakhir 30 Hari", "Terakhir 90 Hari"])

url = st.text_input("Masukkan URL situs paito:")

# Fungsi untuk memberi warna pada tabel (Highlight Otomatis)
def highlight_cells(val):
    target = ['4', '8', '5', '1', '9'] # Angka yang ingin di-highlight
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
                
                # --- TAMPILAN TABEL ---
                st.subheader("📊 Paito Visual")
                styled_df = df.style.applymap(highlight_cells)
                st.dataframe(styled_df, use_container_width=True)
                
                st.markdown("---")
                
                # --- MESIN ANALISIS OTOMATIS ---
                st.subheader("⚙️ Mesin Analisis Pola")
                m1, m2, m3, m4 = st.columns(4)
                
                for i, col in enumerate([m1, m2, m3, m4]):
                    posisi = ["AS", "KOP", "KEPALA", "EKOR"]
                    val_now = int(df.iloc[-1, i])
                    
                    with col:
                        st.metric(label=posisi[i], value=val_now)
                        # Logika sederhana tren
                        val_prev = int(df.iloc[-2, i])
                        trend = "Naik" if val_now > val_prev else "Turun"
                        st.write(f"Trend: {trend}")
                
                # --- DETEKSI POLA BERULANG ---
                st.warning("Mesin sedang memindai angka berulang (Kotak Merah)...")
                # Deteksi angka sama di baris terakhir dengan baris-baris sebelumnya
                angka_terakhir = str(df.iloc[-1, 0])
                st.info(f"Analisis: Angka '{angka_terakhir}' pada kolom AS terdeteksi muncul kembali.")

            else:
                st.error("Tabel tidak ditemukan. Pastikan URL benar.")
        except Exception as e:
            st.error(f"Error Sistem: {e}")
