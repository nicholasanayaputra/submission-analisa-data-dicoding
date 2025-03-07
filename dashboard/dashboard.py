import streamlit as st
import pandas as pd

# Judul Dashboard
st.title("Dashboard Analisis Data")

df = pd.read_csv("dashboard/day_hour_df.csv")

st.write("### Dataset")
st.dataframe(df.head())

st.write("### Tren Transaksi Harian")
st.line_chart(df[['dteday', 'cnt_y']].set_index('dteday'))

st.write("### Distribusi Status Ramai/Sepi")
status_counts = df['status'].value_counts()
st.bar_chart(status_counts)
