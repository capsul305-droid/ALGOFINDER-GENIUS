import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import io

# Konfigurasi Halaman
st.set_page_config(page_title="ALGOFINDER GENIUS PRO", layout="wide")

st.title("🏆 ALGOFINDER GENIUS - PRO MACHINE")

# --- DASHBOARD KONTROL ---
col1, col2, col3 = st.columns(3)
with col1: st.selectbox("Pilih Pasar", ["Hongkong Pools", "Singapore", "Sydney"])
with col2: st.selectbox("Mode", ["Harian", "Warna"])
with col3: st.selectbox("Periode", ["Terakhir 30 Hari", "Terakhir 90 Hari"])

url = st.text_input("Masukkan URL situs paito:")

# Fungsi untuk memberi warna pada tabel (Update ke .map)
def highlight_cells(val):
    target = ['4', '8', '5', '1', '9']
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
                # Membaca tabel
                df = pd.read_html(io.StringIO(str(table)))[0]
                
                # --- TAMPILAN TABEL ---
                st.subheader("📊 Paito Visual")
                
                # Menggunakan .map() sebagai pengganti .applymap() yang sudah usang
                styled_df = df.style.map(highlight_cells)
                st.dataframe(styled_df, use_container_width=True)
                
                st.markdown("---")
                
                # --- MESIN ANALISIS OTOMATIS ---
                st.subheader("⚙️ Mesin Analisis Pola")
                
                # Menampilkan ringkasan kolom terakhir
                cols = st.columns(4)
                posisi = ["AS", "KOP", "KEPALA", "EKOR"]
                
                for i, c in enumerate(cols):
                    if i < len(posisi):
                        val_now = int(df.iloc[-1, i])
                        val_prev = int(df.iloc[-2, i])
                        trend = "Naik 📈" if val_now > val_prev else ("Turun 📉" if val_now < val_prev else "Datar ➖")
                        
                        with c:
                            st.metric(label=posisi[i], value=val_now, delta=trend)

                # Deteksi Pola Berulang (Kotak Merah)
                last_val = str(df.iloc[-1, 0])
                st.info(f"Analisis Histori: Mesin memindai angka '{last_val}' di kolom AS...")

            else:
                st.error("Tabel tidak ditemukan. Pastikan URL benar.")
        except Exception as e:
            st.error(f"Error Sistem: {e}")
