import streamlit as st
import pandas as pd

# Konfigurasi Halaman
st.set_page_config(page_title="AlgoFinder Genius Pro", layout="wide")
st.title("🚀 AlgoFinder Genius - All In One Analyzer")

# --- 1. Inisialisasi Data ---
if 'data_paito' not in st.session_state:
    st.session_state['data_paito'] = None

# --- 2. Sidebar Input & Kontrol ---
st.sidebar.header("⚙️ Kontrol Aplikasi")
data_input = st.sidebar.text_area("Masukkan Data 4D (satu per baris):", height=150)
if st.sidebar.button("Simpan & Proses Data"):
    st.session_state['data_paito'] = [line.strip() for line in data_input.split('\n') if line.strip() if len(line.strip()) == 4]
    st.sidebar.success("Data berhasil diproses!")

menu = st.sidebar.radio("Pilih Fitur:", ["Analisis Terkuat & Pola", "Paito Warna"])

# --- 3. Logika Utama ---
if st.session_state['data_paito']:
    data = st.session_state['data_paito']
    df = pd.DataFrame(data, columns=['Full'])
    df['As'] = df['Full'].str[0].astype(int)
    df['Kop'] = df['Full'].str[1].astype(int)
    df['Kepala'] = df['Full'].str[2].astype(int)
    df['Ekor'] = df['Full'].str[3].astype(int)

    # --- Fitur 1: Analisis Terkuat & Finishing ---
    if menu == "Analisis Terkuat & Pola":
        st.subheader("🎯 Ringkasan Analisis & Angka Terkuat")
        cols = st.columns(4)
        posisi = ['As', 'Kop', 'Kepala', 'Ekor']
        
        for i, pos in enumerate(posisi):
            with cols[i]:
                terkuat = df[pos].value_counts().idxmax()
                st.metric(pos, df[pos].iloc[-1], delta=f"Terkuat: {terkuat}")
                tren = "Naik 📈" if df[pos].iloc[-1] > df[pos].iloc[-2] else "Turun 📉"
                st.write(f"Tren: {tren}")
                st.write(f"Top 3 Muncul: {df[pos].value_counts().head(3).index.tolist()}")

    # --- Fitur 2: Paito Warna ---
    elif menu == "Paito Warna":
        st.subheader("🎨 Paito Warna Historis")
        def color_paito(val):
            colors = {'0':'#FFD1DC', '1':'#B2EBF2', '2':'#C8E6C9', '3':'#FFF9C4', '4':'#E1BEE7', '5':'#FFCCBC', '6':'#D7CCC8', '7':'#CFD8DC', '8':'#F8BBD0', '9':'#B3E5FC'}
            return f'background-color: {colors.get(str(val)[-1], "white")}'
        
        st.dataframe(df.style.applymap(color_paito, subset=['Full']), use_container_width=True)

else:
    st.info("👋 Selamat Datang. Silakan masukkan data di sidebar untuk memulai analisis.")
