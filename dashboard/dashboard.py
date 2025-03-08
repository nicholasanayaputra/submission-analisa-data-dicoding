import streamlit as st
import pandas as pd

# Judul Dashboard
st.title("Dashboard Analisis Data - Bike Sharing")

# Load dataset
df = pd.read_csv("dashboard/day_hour_df.csv")

# Menampilkan dataset
st.write("### Dataset")
st.dataframe(df.head())

# Pastikan kolom yang digunakan ada dalam dataset
if "mnth_hour" not in df.columns or "dteday" not in df.columns or "cnt_hour" not in df.columns:
    st.error("Kolom yang dibutuhkan tidak ditemukan dalam dataset. Periksa kembali dataset yang digunakan.")
else:
    # Pilihan bulan untuk filter
    bulan = st.selectbox("Pilih Bulan", df['mnth_hour'].unique())
    df_filtered = df[df['mnth_hour'] == bulan]

    # Pastikan df_filtered tidak kosong
    if df_filtered.empty:
        st.warning("Tidak ada data untuk bulan yang dipilih.")
    else:
        # Tren penggunaan sepeda harian
        st.write("### Tren Penggunaan Sepeda Harian")
        st.line_chart(df_filtered[['dteday', 'cnt_hour']].set_index('dteday'))

        # Perbedaan peminjaman sepeda antara hari kerja dan akhir pekan
        if "weekday_day" in df_filtered.columns:
            st.write("### Perbedaan Peminjaman Sepeda antara Hari Kerja dan Akhir Pekan")
            st.bar_chart(df_filtered.groupby('weekday_day')['cnt_hour'].sum())
        else:
            st.error("Kolom 'weekday_day' tidak ditemukan dalam dataset.")
