import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Judul Dashboard
st.title("Dashboard Analisis Data - Bike Sharing")

# Load dataset
df = pd.read_csv("dashboard/day_hour_df.csv")

# Cek apakah dataset memiliki kolom yang dibutuhkan
required_columns = {
    "mnth_hour", "cnt_hour", "season_day", "cnt_day", "yr_day", "mnth_day", "weekday_hour"
}
missing_columns = required_columns - set(df.columns)

if missing_columns:
    st.error(f"Kolom yang dibutuhkan tidak ditemukan dalam dataset: {missing_columns}")
else:
    # ====== Fitur Interaktif di Paling Atas ======
    st.header("Eksplorasi Data Interaktif 📊")

    col1, col2 = st.columns(2)  # Membuat dua kolom untuk tata letak rapi

    # Dropdown untuk memilih tahun
    with col1:
        tahun_pilihan = st.selectbox(
            "Pilih Tahun",
            options=[0, 1],  # 0 = Tahun 2011, 1 = Tahun 2012
            format_func=lambda x: "2011" if x == 0 else "2012"
        )

    # Slider untuk memilih rentang bulan
    with col2:
        bulan_range = st.slider(
            "Pilih Rentang Bulan",
            min_value=1, max_value=12, value=(1, 12)
        )

    # Filter data berdasarkan tahun dan rentang bulan
    df_filtered = df[(df["yr_day"] == tahun_pilihan) & 
                     (df["mnth_day"] >= bulan_range[0]) & 
                     (df["mnth_day"] <= bulan_range[1])]

    # ---- Tren Peminjaman Sepeda Berdasarkan Pilihan ----
    st.subheader(f"Tren Peminjaman Sepeda pada Tahun {'2011' if tahun_pilihan == 0 else '2012'} ({bulan_range[0]} - {bulan_range[1]})")

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.lineplot(x="mnth_day", y="cnt_day", data=df_filtered, ci=None, ax=ax, color="b")
    ax.set_title(f"Tren Peminjaman Sepeda pada Tahun {'2011' if tahun_pilihan == 0 else '2012'}")
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Jumlah Peminjaman")
    ax.set_xticks(range(bulan_range[0], bulan_range[1] + 1))
    st.pyplot(fig)

    # ====== Header untuk Pola Musiman ======
    st.header("Apakah ada pola musiman dalam penggunaan sepeda?")
    
    # ---- Pola Musiman dalam Penggunaan Sepeda ----
    st.subheader("Pola Musiman dalam Penggunaan Sepeda")

    df_monthly = df.groupby("mnth_hour")["cnt_hour"].sum().reset_index()
    month_names = {
        1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "Mei", 6: "Jun",
        7: "Jul", 8: "Agu", 9: "Sep", 10: "Okt", 11: "Nov", 12: "Des"
    }
    df_monthly["Bulan"] = df_monthly["mnth_hour"].map(month_names)

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(x="Bulan", y="cnt_hour", data=df_monthly, marker="o", color="b", linewidth=2, ax=ax)
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Total Peminjaman")
    ax.set_title("Pola Musiman dalam Penggunaan Sepeda")
    ax.grid()
    st.pyplot(fig)

    # ---- Distribusi Peminjaman Sepeda per Musim ----
    st.subheader("Distribusi Peminjaman Sepeda per Musim")

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(x="season_day", y="cnt_day", data=df, ax=ax, color="#3274A1")
    ax.set_title("Distribusi Peminjaman Sepeda per Musim")
    ax.set_xlabel("Musim (1: Semi, 2: Panas, 3: Gugur, 4: Dingin)")
    ax.set_ylabel("Jumlah Peminjaman")
    st.pyplot(fig)

    # ---- Tren Peminjaman Sepeda per Tahun ----
    st.subheader("Tren Peminjaman Sepeda per Tahun")

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.lineplot(x="yr_day", y="cnt_day", data=df, estimator="mean", ax=ax)
    ax.set_title("Tren Peminjaman Sepeda per Tahun")
    ax.set_xlabel("Tahun (0: 2011, 1: 2012)")
    ax.set_ylabel("Jumlah Peminjaman Rata-rata")
    st.pyplot(fig)

    # ---- Tren Peminjaman Sepeda per Bulan ----
    st.subheader("Tren Peminjaman Sepeda per Bulan")

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(x="mnth_day", y="cnt_day", data=df, ci=None, ax=ax)
    ax.set_title("Tren Peminjaman Sepeda per Bulan")
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Jumlah Peminjaman")
    ax.set_xticks(range(1, 13))
    st.pyplot(fig)

    # ====== Header untuk Perbedaan Peminjaman ======
    st.header("Bagaimana perbedaan peminjaman antara hari kerja dan akhir pekan?")
    
    # ---- Perbedaan Peminjaman Sepeda antara Hari Kerja dan Akhir Pekan ----
    st.subheader("Perbedaan Peminjaman Sepeda antara Hari Kerja dan Akhir Pekan")

    df["kategori_hari"] = df["weekday_hour"].apply(lambda x: "Hari Kerja" if x < 5 else "Akhir Pekan")
    df_weekday_vs_weekend = df.groupby("kategori_hari")["cnt_hour"].sum().reset_index()

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x="kategori_hari", y="cnt_hour", data=df_weekday_vs_weekend, palette="coolwarm", ax=ax)
    ax.set_xlabel("Kategori Hari")
    ax.set_ylabel("Total Peminjaman")
    ax.set_title("Perbedaan Peminjaman Sepeda antara Hari Kerja dan Akhir Pekan")
    ax.grid(axis="y")
    st.pyplot(fig)
