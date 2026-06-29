DASHBOARD VERSION
import streamlit as st
import pandas as pd
import requests

st.set_page_config(
    page_title="Paito Analytics Pro",
    layout="wide"
)

st.title("📊 Paito Analytics Pro Dashboard")

# =========================
# SIDEBAR CONTROL
# =========================
st.sidebar.header("⚙️ Control Panel")

mode = st.sidebar.radio(
    "Pilih Sumber Data",
    ["Upload File", "Input Link"]
)

df = None

# =========================
# LOAD DATA
# =========================
if mode == "Upload File":
    file = st.sidebar.file_uploader("Upload CSV / TXT", type=["csv", "txt"])

    if file:
        try:
            df = pd.read_csv(file) if file.name.endswith("csv") else pd.read_csv(file, header=None)
        except Exception as e:
            st.error(f"Error file: {e}")

elif mode == "Input Link":
    url = st.sidebar.text_input("Masukkan URL")

    if url:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            r = requests.get(url, headers=headers, timeout=10)

            try:
                df = pd.read_csv(url)
            except:
                df = pd.read_html(r.text)[0]

        except Exception as e:
            st.error("Gagal load link")
            st.write(e)

# =========================
# MAIN DASHBOARD
# =========================
if df is not None:

    tab1, tab2, tab3 = st.tabs([
        "📄 Data",
        "📊 Statistik",
        "🔥 Analisis Pola"
    ])

    # =========================
    # TAB 1 - DATA
    # =========================
    with tab1:
        st.subheader("Data Mentah")
        st.dataframe(df, use_container_width=True)

        data = df.iloc[:, 0].astype(str).tolist()
        data = [x.zfill(4) for x in data]

        st.subheader("Data Bersih")
        st.write(data)

    # =========================
    # TAB 2 - STATISTIK
    # =========================
    with tab2:
        st.subheader("Statistik Digit")

        all_digits = "".join(data)

        freq = {}
        for d in all_digits:
            freq[d] = freq.get(d, 0) + 1

        freq_df = pd.DataFrame(
            list(freq.items()),
            columns=["Digit", "Frekuensi"]
        ).sort_values("Frekuensi", ascending=False)

        col1, col2 = st.columns(2)

        with col1:
            st.bar_chart(freq_df.set_index("Digit"))

        with col2:
            st.dataframe(freq_df, use_container_width=True)

    # =========================
    # TAB 3 - POLA
    # =========================
    with tab3:
        st.subheader("Pola Naik / Turun / Datar")

        angka = []
        for x in data:
            try:
                angka.append(int(x))
            except:
                pass

        trend = []
        for i in range(1, len(angka)):
            if angka[i] > angka[i - 1]:
                trend.append(1)
            elif angka[i] < angka[i - 1]:
                trend.append(-1)
            else:
                trend.append(0)

        st.line_chart(trend)

        col1, col2, col3 = st.columns(3)

        col1.metric("Naik", trend.count(1))
        col2.metric("Turun", trend.count(-1))
        col3.metric("Datar", trend.count(0))

        st.subheader("Insight")
        if trend.count(1) > trend.count(-1):
            st.success("Trend dominan: NAIK 📈")
        elif trend.count(-1) > trend.count(1):
            st.warning("Trend dominan: TURUN 📉")
        else:
            st.info("Trend stabil / datar ⚖️")

else:
    st.info("Silakan upload file atau masukkan link data dari sidebar
