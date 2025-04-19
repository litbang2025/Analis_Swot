import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from wordcloud import WordCloud
import streamlit as st

# Styling visual
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12
sns.set(style="whitegrid")

# ===============================
# 1. 📥 BACA DATA
# ===============================
@st.cache_data
def load_data():
    # Mengganti dengan file yang sesuai (misalnya file csv yang sudah ada)
    df = pd.read_csv('analisis_bumi.csv')  # Gantilah dengan file yang sesuai
    return df
df = load_data()
# ===============================
# 📥 Unggah Data CSV
# ===============================
# Upload File
uploaded_file = st.file_uploader("📥 Upload file CSV hasil survei", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File CSV berhasil di-upload dan dibaca.")
else:
    st.info("📁 Menggunakan file default 'analisis_bumi.csv'.")
    df = load_data_from_default()

# Validasi jika gagal
if df is None or df.empty:
    st.error("❌ Gagal memuat data. Pastikan file tidak kosong atau salah format.")
    st.stop()

# Lanjutkan visualisasi setelah data aman
st.subheader("📋 Data Response")
st.dataframe(df.head())
    
# Tampilkan beberapa data awal
st.title("📊 Analisis Survei Terbuka (Professional)")
st.subheader("Data Awal:")
st.write(df.head())
# ===============================
# 2. ℹ️ INFORMASI DASAR
# ===============================
jumlah_responden = df.shape[0]
jumlah_pertanyaan = df.shape[1] - 3  # Dikurangi kolom A-C (timestamp, nama, pendidikan)

st.subheader("Informasi Dasar")
st.write(f"👥 Jumlah responden: {jumlah_responden}")
st.write(f"❓ Jumlah kolom pertanyaan SWOT: {jumlah_pertanyaan}")

# ===============================
# 3. 📊 PERSENTASE PENDIDIKAN
# ===============================
st.subheader("Distribusi Pendidikan Responden")
pendidikan_counts = df['Bagian'].value_counts()
fig_pendidikan = plt.figure(figsize=(8, 5))
sns.barplot(x=pendidikan_counts.index, y=pendidikan_counts.values, palette='viridis')
plt.title('Distribusi Pendidikan Responden')
plt.xlabel('Pendidikan')
plt.ylabel('Jumlah Responden')
st.pyplot(fig_pendidikan)

# ===============================
# 4. 📌 ANALISIS SWOT
# ===============================
swot_labels = ['Permasalahan Utama', 'Ancaman', 'Peluang', 'Kekuatan']
swot_columns = df.columns[3:7]  # Kolom D sampai H

def analisis_swot(judul, jawaban_list, warna='skyblue'):
    st.subheader(f"📘 Analisis: {judul}")
    
    # Gabungkan semua jawaban
    semua_jawaban = " ".join(str(j) for j in jawaban_list if pd.notna(j))
    
    # Pisahkan berdasarkan koma atau baris
    kata_kunci = []
    for baris in jawaban_list:
        if pd.notna(baris):
            potongan = str(baris).replace("\n", ",").split(",")
            kata_kunci.extend([k.strip().lower() for k in potongan if k.strip()])
    
    # Hitung frekuensi
    frekuensi = Counter(kata_kunci)
    df_freq = pd.DataFrame(frekuensi.items(), columns=["Jawaban", "Frekuensi"]).sort_values(by="Frekuensi", ascending=False)

    # Tampilkan tabel
    st.write(df_freq.head(10))  # Top 10
    
    # Visualisasi Bar Chart
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x='Frekuensi', y='Jawaban', data=df_freq.head(10), color=warna, ax=ax)  # Menggunakan color bukan palette
    plt.title(f"🔍 Top Jawaban: {judul}")
    plt.xlabel("Frekuensi")
    plt.ylabel("Jawaban")
    st.pyplot(fig)

    # WordCloud (Opsional)
    wordcloud = WordCloud(width=800, height=300, background_color='white').generate(" ".join(kata_kunci))
    fig_wc = plt.figure(figsize=(10, 3))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.title(f"☁️ Wordcloud: {judul}")
    st.pyplot(fig_wc)

# ===============================
# 5. 🔍 EKSEKUSI SEMUA ANALISIS
# ===============================
for i, col in enumerate(swot_columns):
    analisis_swot(swot_labels[i], df[col])

# ===============================
# 6. 📝 REKOMENDASI
# ===============================
st.subheader("Rekomendasi Berdasarkan Analisis")

# Berdasarkan hasil umum
if jumlah_responden > 50:
    st.write("📝 Rekomendasi Umum: Dengan lebih dari 50 responden, analisis ini dapat memberikan wawasan yang lebih mendalam. Disarankan untuk mengidentifikasi area-area utama yang membutuhkan perhatian lebih dalam perencanaan strategis.")
else:
    st.write("📝 Rekomendasi Umum: Dengan jumlah responden yang terbatas, hasil analisis ini mungkin lebih representatif untuk kelompok kecil. Perlu ada penelitian lebih lanjut.")

# Berdasarkan indikator (Pendidikan, untuk contoh)
pendidikan = st.selectbox("Pilih Tingkat Pendidikan untuk Analisis", pendidikan_counts.index)
st.write(f"📝 Berdasarkan tingkat pendidikan '{pendidikan}', hasil menunjukkan bahwa lebih banyak responden dengan latar belakang pendidikan tersebut memberikan kontribusi pada aspek tertentu dalam analisis SWOT.")

# ===============================
# 7. 🚀 DASHBOARD INTERAKTIF
# ===============================
st.subheader("Dashboard Interaktif")
st.write("Gunakan dashboard ini untuk menyesuaikan parameter analisis dan melihat perbandingan hasil berdasarkan pendidikan atau kategori lainnya.")

# Pilihan kategori atau indikator untuk analisis lebih lanjut (misalnya pendidikan)
indikator = st.selectbox("Pilih Indikator untuk Analisis Lebih Lanjut", ['Permasalahan Utama', 'Ancaman', 'Peluang', 'Kekuatan'])
st.write(f"📊 Analisis {indikator} berdasarkan responden yang dipilih:")

# Tampilkan analisis sesuai pilihan indikator
indikator_col = df[indikator]
analisis_swot(indikator, indikator_col)

