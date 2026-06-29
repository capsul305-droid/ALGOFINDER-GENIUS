import streamlit as st
import pandas as pd

st.title("📊 Analisis Paito (File + Link)")

mode = st.radio("Pilih sumber data:", ["Upload File", "Input Link"])

df = None

# =========================
# MODE UPLOAD FILE
# =========================
if mode == "Upload File":
    uploaded_file = st.file_uploader("Upload CSV/TXT", type=["csv", "txt"])

    if uploaded_file is not None:
        if uploaded_file.name.endswith("csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file, header=None)

# =========================
# MODE LINK
# =========================
elif mode == "Input Link":
    url = st.text_input("Masukkan URL data:")

    if url:
        try:
            # coba baca sebagai CSV dari web
            df = pd.read_csv(url)
        except:
            try:
                # kalau tabel HTML
                df = pd.read_html(url)[0]
            except:
                st.error("Link tidak bisa dibaca sebagai CSV atau tabel HTML")

# =========================
# HASIL
# =========================
if df is not None:
    st.subheader("📄 Data Asli")
    st.write(df)

    data = df.iloc[:, 0].astype(str).tolist()
    data = [x.zfill(4) for x in data]

    st.subheader("📌 Data Bersih")
    st.write(data)

    # Frekuensi digit
    all_digits = "".join(data)

    freq = {}
    for d in all_digits:
        freq[d] = freq.get(d, 0) + 1

    freq_df = pd.DataFrame(list(freq.items()), columns=["Digit", "Frekuensi"])
    freq_df = freq_df.sort_values("Frekuensi", ascending=False)

    st.subheader("🔥 Frekuensi")
    st.bar_chart(freq_df.set_index("Digit"))

else:
    st.info("Masukkan file atau link dulu")
