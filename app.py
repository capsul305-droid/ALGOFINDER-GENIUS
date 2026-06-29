import streamlit as st
import pandas as pd

st.set_page_config(page_title="Analisis Paito", layout="wide")

st.title("📊 Aplikasi Analisis Data Paito")

# =========================
# Upload File
# =========================
uploaded_file = st.file_uploader(
    "Upload file (.csv atau .txt)",
    type=["csv", "txt"]
)

if uploaded_file is not None:

    # =========================
    # BACA FILE
    # =========================
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_csv(uploaded_file, header=None)

    st.subheader("📄 Data Mentah")
    st.write(df)

    # Ambil kolom pertama
    data = df.iloc[:, 0].astype(str).tolist()

    # Rapikan jadi angka 4 digit (kalau perlu)
    data = [x.zfill(4) for x in data]

    st.subheader("📌 Data Setelah Dirapikan")
    st.write(data)

    # =========================
    # FREKUENSI ANGKA
    # =========================
    all_digits = "".join(data)

    freq = {}
    for d in all_digits:
        freq[d] = freq.get(d, 0) + 1

    freq_df = pd.DataFrame(
        list(freq.items()),
        columns=["Digit", "Frekuensi"]
    ).sort_values(by="Frekuensi", ascending=False)

    st.subheader("🔥 Frekuensi Digit")
    st.dataframe(freq_df)

    st.bar_chart(freq_df.set_index("Digit"))

    # =========================
    # POLA NAIK / TURUN / DATAR
    # =========================
    st.subheader("📈 Analisis Pola (Naik / Turun / Datar)")

    angka = [int(x) for x in data]

    trend = []
    for i in range(1, len(angka)):
        if angka[i] > angka[i - 1]:
            trend.append(1)   # naik
        elif angka[i] < angka[i - 1]:
            trend.append(-1)  # turun
        else:
            trend.append(0)   # datar

    trend_df = pd.DataFrame(trend, columns=["Pola"])

    st.line_chart(trend_df)

    naik = trend.count(1)
    turun = trend.count(-1)
    datar = trend.count(0)

    st.write({
        "Naik": naik,
        "Turun": turun,
        "Datar": datar
    })

    # =========================
    # STATISTIK DASAR
    # =========================
    st.subheader("📊 Statistik Dasar")

    st.write("Total data:", len(angka))
    st.write("Nilai tertinggi:", max(angka))
    st.write("Nilai terendah:", min(angka))
    st.write("Rata-rata:", sum(angka) / len(angka))

else:
    st.info("Silakan upload file CSV atau TXT terlebih dahulu.")
