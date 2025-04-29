import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from wordcloud import WordCloud
import streamlit as st

# === TEMA APLIKASI ===
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12
sns.set(style="whitegrid")
st.set_page_config(page_title="Analisis Teks Dinamis", layout="wide")

# === FUNGSI: BACA DATA DEFAULT ===
@st.cache_data
def load_default_data():
    return pd.read_csv('analisis_bumi.csv')

# === SIDEBAR: PENGATURAN ===
st.sidebar.title("⚙️ Pengaturan Analisis")

uploaded_file = st.sidebar.file_uploader("📤 Upload file CSV", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("✅ File berhasil diunggah!")
else:
    st.sidebar.info("📁 Menggunakan data default: analisis_umum.csv")
    df = load_default_data()

# === VALIDASI DATA ===
if df is None or df.empty:
    st.error("❌ Data tidak tersedia atau kosong.")
    st.stop()

# === PILIH KOLUMN UNTUK ANALISIS ===
text_columns = st.sidebar.multiselect("📝 Pilih kolom teks untuk analisis", options=df.columns, default=df.columns[3:7])

# === INPUT LABEL OLEH USER ===
labels = []
for i, col in enumerate(text_columns):
    default_label = col.replace("_", " ").title()
    label = st.sidebar.text_input(f"Label untuk kolom '{col}'", value=default_label)
    labels.append(label)

# === PILIH KATEGORI (OPSIONAL) ===
kategori_col = st.sidebar.selectbox("🔍 Pilih kolom kategori untuk filter (opsional)", options=[None] + list(df.columns))

# === HEADER & INFO UMUM ===
st.title("📊 Aplikasi Analisis Teks Naratif")
st.markdown("Gunakan aplikasi ini untuk menganalisis data berbasis teks naratif dengan grafik, frekuensi kata, dan wordcloud.")

st.subheader("📋 Data Responden")
st.dataframe(df.head(), use_container_width=True)

jumlah_responden = df.shape[0]
st.write(f"👥 Jumlah responden: {jumlah_responden}")
st.write(f"📦 Jumlah kolom analisis: {len(text_columns)}")

# === FUNGSI ANALISIS ===
def analisis_teks(judul, jawaban_list, warna='skyblue'):
    st.markdown(f"---\n### 🔍 Analisis: {judul}")

    semua_jawaban = " ".join(str(j) for j in jawaban_list if pd.notna(j))
    kata_kunci = []
    for baris in jawaban_list:
        if pd.notna(baris):
            potongan = str(baris).replace("\n", ",").split(",")
            kata_kunci.extend([k.strip().lower() for k in potongan if k.strip()])

    frekuensi = Counter(kata_kunci)
    df_freq = pd.DataFrame(frekuensi.items(), columns=["Jawaban", "Frekuensi"]).sort_values(by="Frekuensi", ascending=False)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.write("🗒️ **Top Jawaban**")
        st.dataframe(df_freq.head(10), use_container_width=True)

    with col2:
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(x='Frekuensi', y='Jawaban', data=df_freq.head(10), color=warna, ax=ax)
        plt.title(f"Top Kata Kunci: {judul}")
        plt.xlabel("Frekuensi")
        plt.ylabel("Jawaban")
        st.pyplot(fig, use_container_width=True)

    wc = WordCloud(width=800, height=300, background_color='white').generate(" ".join(kata_kunci))
    st.image(wc.to_array(), caption=f"☁️ Wordcloud: {judul}", use_container_width=True)

# === ANALISIS UMUM ===
st.markdown("## 🔎 Hasil Analisis Umum")
for i, col in enumerate(text_columns):
    analisis_teks(labels[i], df[col])

# === FILTER BERDASARKAN KATEGORI ===
if kategori_col:
    st.markdown("---")
    st.subheader(f"🎯 Analisis Berdasarkan Kategori: `{kategori_col}`")
    pilihan = st.selectbox("Pilih nilai kategori:", df[kategori_col].dropna().unique())
    df_filtered = df[df[kategori_col] == pilihan]
    st.write(f"📌 Jumlah responden pada kategori '{pilihan}': {df_filtered.shape[0]}")

    for i, col in enumerate(text_columns):
        analisis_teks(f"{labels[i]} - {pilihan}", df_filtered[col])
