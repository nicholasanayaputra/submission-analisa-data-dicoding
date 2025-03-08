import streamlit as st
import pandas as pd

st.title("Dashboard Analisis Data - Bike Sharing")

df = pd.read_csv("dashboard/day_hour_df.csv")

st.write("### Dataset")
st.dataframe(df.head())

bulan = st.selectbox("Pilih Bulan", df['mnth_hour'].unique())
df_filtered = df[df['mnth_hour'] == bulan]

st.write("### Tren Penggunaan Sepeda Harian")
st.line_chart(df_filtered[['dteday', 'cnt_hour']].set_index('dteday'))

st.write("### Perbedaan Peminjaman Sepeda antara Hari Kerja dan Akhir Pekan")
st.bar_chart(df_filtered.groupby('weekday_day')['cnt_hour'].sum())
