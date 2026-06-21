import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="AlgoFinder Genius", layout="wide")

st.markdown("""
    <style>
    .reportview-container { background: #0c1020; }
    .main { background-color: #0b0f19; color: #ffffff; }
    div.stButton > button:first-child { background-color: #00cc99; color:white; }
    .position-box {
        background-color: #121826;
        border: 1px solid #1f2c47;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
    }
    .header-pos { color: #00ffcc; font-weight: bold; font-size: 18px; border-bottom: 1px solid #1f2c47; padding-bottom: 5px; }
    .stat-text { color: #8fa0c4; font-size: 14px; }
    .strong-text { color: #00ffaa; font-weight: bold; }
    .cad-text { color: #ffcc00; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ ALGOFINDER GENIUS CLONE")
st.subheader("Ringkasan Prediksi - 4 Posisi Berbasis Algoritma Pola")

st.sidebar.header("Input Data Historis")
paito_input = st.sidebar.text_area("Masukkan Data 4D (Satu per baris):", 
"""4326
3980
3452
7541
4852
9173""")

try:
    lines = [line.strip() for line in paito_input.split("\n") if len(line.strip()) == 4]
    if len(lines) < 2:
        lines = ["4326", "3980", "3452", "7541", "4852", "9173"]
    df = pd.DataFrame([[int(c) for c in num] for num in lines], columns=['AS', 'KOP', 'KEPALA', 'EKOR'])
except:
    df = pd.DataFrame(columns=['AS', 'KOP', 'KEPALA', 'EKOR'])

def hitung_algoritma_posisi(series):
    if len(series) < 2:
        return {"datar": 0, "turun": 0, "naik": 0, "kuat": [0], "cad": [1], "persen": 50}
    selisih = np.diff(series[::-1])
    datar = int(np.sum(selisih == 0))
    turun = int(np.sum(selisih < 0))
    naik = int(np.sum(selisih > 0))
    counts = series.value_counts()
    angka_tersering = list(counts.index[:2])
    angka_kuat = [angka_tersering[0]] if len(angka_tersering) > 0 else [0]
    angka_cad = [angka_tersering[1]] if len(angka_tersering) > 1 else [1]
    total_pergerakan = datar + turun + naik
    dominan = max(datar, turun, naik)
    persen_kekuatan = int((dominan / total_pergerakan) * 100) if total_pergerakan > 0 else 50
    return {"datar": datar, "turun": turun, "naik": naik, "kuat": angka_kuat, "cad": angka_cad, "persen": persen_kekuatan}

if not df.empty:
    col1, col2 = st.columns(2)
    posisi_list = ['AS', 'KOP', 'KEPALA', 'EKOR']
    for idx, pos in enumerate(posisi_list):
        target_col = col1 if idx % 2 == 0 else col2
        res = hitung_algoritma_posisi(df[pos])
        with target_col:
            st.markdown(f"""
            <div class="position-box">
                <div class="header-pos">{pos}</div>
                <p class="stat-text">📊 Pola Datar : {res['datar']}</p>
                <p class="stat-text">📉 Pola Turun : {res['turun']}</p>
                <p class="stat-text">📈 Pola Naik : {res['naik']}</p>
                <hr style="border-color:#1f2c47;">
                <p class="stat-text">🎯 Fokus Kelas : <span style="color:#00ffcc;">{res['turun']}/{len(df)} Kelas</span></p>
                <p class="stat-text">⭐ <span class="strong-text">KUAT-P : {' / '.join(map(str, res['kuat']))}</span></p>
                <p class="stat-text">🔶 <span class="cad-text">Cadangan : {' / '.join(map(str, res['cad']))}</span></p>
                <p class="stat-text">⚙️ Kekuatan : <span style="color:#ff3366; font-weight:bold;">{res['persen']}%</span></p>
                <p style="color:#00ffcc; font-size:12px;">✔ BET -- Terkonfirmasi</p>
            </div>
            """, unsafe_allow_html=True)
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="AlgoFinder Genius", layout="wide")

st.markdown("""
    <style>
    .reportview-container { background: #0c1020; }
    .main { background-color: #0b0f19; color: #ffffff; }
    div.stButton > button:first-child { background-color: #00cc99; color:white; }
    .position-box {
        background-color: #121826;
        border: 1px solid #1f2c47;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
    }
    .header-pos { color: #00ffcc; font-weight: bold; font-size: 18px; border-bottom: 1px solid #1f2c47; padding-bottom: 5px; }
    .stat-text { color: #8fa0c4; font-size: 14px; }
    .strong-text { color: #00ffaa; font-weight: bold; }
    .cad-text { color: #ffcc00; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ ALGOFINDER GENIUS CLONE")
st.subheader("Ringkasan Prediksi - 4 Posisi Berbasis Algoritma Pola")

st.sidebar.header("Input Data Historis")
paito_input = st.sidebar.text_area("Masukkan Data 4D (Satu per baris):", 
"""4326
3980
3452
7541
4852
9173""")

try:
    lines = [line.strip() for line in paito_input.split("\n") if len(line.strip()) == 4]
    if len(lines) < 2:
        lines = ["4326", "3980", "3452", "7541", "4852", "9173"]
    df = pd.DataFrame([[int(c) for c in num] for num in lines], columns=['AS', 'KOP', 'KEPALA', 'EKOR'])
except:
    df = pd.DataFrame(columns=['AS', 'KOP', 'KEPALA', 'EKOR'])

def hitung_algoritma_posisi(series):
    if len(series) < 2:
        return {"datar": 0, "turun": 0, "naik": 0, "kuat": [0], "cad": [1], "persen": 50}
    selisih = np.diff(series[::-1])
    datar = int(np.sum(selisih == 0))
    turun = int(np.sum(selisih < 0))
    naik = int(np.sum(selisih > 0))
    counts = series.value_counts()
    angka_tersering = list(counts.index[:2])
    angka_kuat = [angka_tersering[0]] if len(angka_tersering) > 0 else [0]
    angka_cad = [angka_tersering[1]] if len(angka_tersering) > 1 else [1]
    total_pergerakan = datar + turun + naik
    dominan = max(datar, turun, naik)
    persen_kekuatan = int((dominan / total_pergerakan) * 100) if total_pergerakan > 0 else 50
    return {"datar": datar, "turun": turun, "naik": naik, "kuat": angka_kuat, "cad": angka_cad, "persen": persen_kekuatan}

if not df.empty:
    col1, col2 = st.columns(2)
    posisi_list = ['AS', 'KOP', 'KEPALA', 'EKOR']
    for idx, pos in enumerate(posisi_list):
        target_col = col1 if idx % 2 == 0 else col2
        res = hitung_algoritma_posisi(df[pos])
        with target_col:
            st.markdown(f"""
            <div class="position-box">
                <div class="header-pos">{pos}</div>
                <p class="stat-text">📊 Pola Datar : {res['datar']}</p>
                <p class="stat-text">📉 Pola Turun : {res['turun']}</p>
                <p class="stat-text">📈 Pola Naik : {res['naik']}</p>
                <hr style="border-color:#1f2c47;">
                <p class="stat-text">🎯 Fokus Kelas : <span style="color:#00ffcc;">{res['turun']}/{len(df)} Kelas</span></p>
                <p class="stat-text">⭐ <span class="strong-text">KUAT-P : {' / '.join(map(str, res['kuat']))}</span></p>
                <p class="stat-text">🔶 <span class="cad-text">Cadangan : {' / '.join(map(str, res['cad']))}</span></p>
                <p class="stat-text">⚙️ Kekuatan : <span style="color:#ff3366; font-weight:bold;">{res['persen']}%</span></p>
                <p style="color:#00ffcc; font-size:12px;">✔ BET -- Terkonfirmasi</p>
            </div>
            """, unsafe_allow_html=True)
