import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="AlgoFinder Genius", layout="wide")

# --- 2. FUNGSI PEWARNAAN TABEL ---
def color_paito(val):
    colors = {
        '0': '#FFD1DC', '1': '#B2EBF2', '2': '#C8E6C9', 
        '3': '#FFF9C4', '4': '#E1BEE7', '5': '#FFCCBC',
        '6': '#D7CCC8', '7': '#CFD8DC', '8': '#F8BBD0', '9': '#B3E5FC'
    }
    digit = str(val)[-1]
    return f'background-color: {colors.get(digit, "white")}; color: black;'

# --- 3. SIDEBAR NAVIGATION ---
st.sidebar.title("🛠️ Menu Navigasi")
menu = st.sidebar.radio("Pilih Fitur:", ["Input Data", "Paito Visualizer", "Hubungkan Link Paito"])

if 'data_paito' not in st.session_state:
    st.session_state['data_paito'] = None

# --- 4. LOGIKA FITUR ---
if menu == "Input Data":
    st.header("Input Data Historis")
    data_input = st.text_area("Masukkan Data 4D (Satu per baris):", height=200)
    if st.button("Simpan Data"):
        if data_input:
            st.session_state['data_paito'] = [line.strip() for line in data_input.split('\n') if line.strip()]
            st.success("Data berhasil disimpan!")

elif menu == "Paito Visualizer":
    st.header("Tabel Paito Warna")
    if st.session_state['data_paito']:
        df = pd.DataFrame(st.session_state['data_paito'], columns=['Data 4D'])
        styled_df = df.style.map(color_paito)
        st.dataframe(styled_df, use_container_width=True)
    else:
        st.info("Silakan masukkan data di menu 'Input Data' terlebih dahulu.")

elif menu == "Hubungkan Link Paito":
    st.header("Akses Situs Paito Warna")
    paito_url = st.text_input("Masukkan URL situs paito:", "https://")
    if paito_url != "https://":
        st.link_button("Buka Paito di Tab Baru", paito_url)
        try:
            components.iframe(paito_url, height=600, scrolling=True)
        except:
            st.warning("Situs ini memblokir tampilan langsung.")
