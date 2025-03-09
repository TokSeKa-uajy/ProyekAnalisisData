import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# Membuat fungsi untuk menampilkan total perentalan dalam bulanan
def create_monthly_orders_df(df):
    monthly_orders_df = df.resample(rule='M', on='dteday').agg({
        "cnt": "sum"
    }).reset_index()
    monthly_orders_df = monthly_orders_df.reset_index()
    return monthly_orders_df

# Membuat fungsi untuk membuat dataframe create_byseason_df
def create_byseason_df(df):
    byseason_df = df.groupby(by="season").agg({
        "cnt": "sum"
    }).reset_index()

    return byseason_df

# Membuat fungsi untuk membuat dataframe create_holiday_byHour_df
def create_holiday_byHour_df(df):
    holiday_orders_df = df.groupby(["holiday", "hr"]).agg({
        "cnt": "mean"
    }).reset_index()

    return holiday_orders_df

def create_bywaether_df(df):
    byweather_df = df.groupby(by="weathersit").agg({
        "cnt": "sum"
    }).squeeze()

    return byweather_df

# Membaca dataset
day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")

# Mengubah kolom dteday menjadi datetime
day_df.sort_values(by="dteday", inplace=True)
day_df.reset_index(inplace=True)

hour_df.sort_values(by="dteday", inplace=True)
hour_df.reset_index(inplace=True)

day_df["dteday"] = pd.to_datetime(day_df["dteday"])
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])

# Mengambil nilai min dan max dari kolom dteday
min_date_hour = hour_df["dteday"].min()
max_date_hour = hour_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://st2.depositphotos.com/2830795/9884/v/450/depositphotos_98842806-stock-illustration-bicycle-logo-design-vector-template.jpg")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date_hour,
        max_value=max_date_hour,
        value=[min_date_hour, max_date_hour]
    )
    
main_day_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date))]

main_hour_df = hour_df[(hour_df["dteday"] >= str(start_date)) &
                    (hour_df["dteday"] <= str(end_date))]

# Membuat dataframe berdasarkan fungsi yang telah dibuat
monthly_orders_df = create_monthly_orders_df(main_day_df)
byseason_df = create_byseason_df(main_day_df)
holiday_byHour_df = create_holiday_byHour_df(main_hour_df)
byweather_df = create_bywaether_df(main_hour_df)

# Menampilkan judul
st.header("Dashboard Rental Sepeda")

# Menampilkan grafik total perentalan dalam bulanan
st.subheader('Monthly Orders')
col1= st.columns(1)[0]
with col1:
    # menampilkan total order dalam rentang bulan yang dipilih (cnt)
    total_orders = monthly_orders_df["cnt"].sum()
    st.metric("Total orders", value=total_orders)
    
# Menampilkan grafik total perentalan dalam bulanan
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(
    monthly_orders_df["dteday"],
    monthly_orders_df["cnt"],
    marker='o', 
    linewidth=2,
    color="#90CAF9",
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
ax.set_title("Total Rental per Bulan", loc="center", fontsize=20)
ax.set_ylabel("Total Rental")
st.pyplot(fig)


# Menampikan grafik total rental disetiap season
st.subheader('Seasonly Orders')
fig2, ax2 = plt.subplots(figsize=(12, 6))
colors = ["#D3D3D3", "#D3D3D3", "#72BCD4", "#D3D3D3"]

plt.figure(figsize=(10, 5))
colors = ["#D3D3D3","#D3D3D3", "#72BCD4", "#D3D3D3"]

sns.barplot(
    y="cnt",
    x="season",
    data=byseason_df,
    palette=colors,
    ax=ax2
)

ax2.set_title("Perbandingan cnt setiap Season (per juta)", loc="center", fontsize=15)
ax2.set_ylabel("Total cnt")
ax2.set_xlabel("Season")
ax2.tick_params(axis='x', labelsize=12)

st.pyplot(fig2)

# Menampilkan grafik rata-rata rental disetiap jam pada hari libur dan bukan hari libur
st.subheader('Mean Holiday (1) vs Non-Holiday (0) orders by Hour')
fig3, ax3 = plt.subplots(figsize=(12, 6))
colors = ["#90CAF9", "#D3D3D3"]

sns.lineplot(
    y="cnt",
    x="hr",
    data=holiday_byHour_df,
    palette=["#D3D3D3", "#72BCD4"],
    hue="holiday",
    marker="o",
    linewidth=2,
    ax=ax3
)

ax3.set_title("Mean Holiday (1) vs Non-Holiday (0)", fontsize=15)
ax3.set_ylabel(None)
ax3.set_xlabel("Waktu peminjaman (jam)", fontsize=12)
ax3.tick_params(axis='x', labelsize=12)
ax3.set_xticks(range(0, 24))
st.pyplot(fig3)

# Menampilkan jumlah transaksi berdasarkan cuaca dalam bentuk pie cjart
st.subheader('Orders by Weather Situation')
fig4, ax4 = plt.subplots(figsize=(12, 6))
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
nameLabels=("Clear", "Mist", "Light Snow", "Heavy Rain")
colors = ('#8B4513', '#FFF8DC', '#93C572', '#E67F0D')
ax4.pie(
    labels=nameLabels,
    x=byweather_df,
    colors=colors,
    autopct='%1.1f%%',
)   
ax4.set_title("Jumlah transaksi berdasarkan cuaca", loc="center", fontsize=15)
st.pyplot(fig4)

st.caption('Copyright (c) Tok Se Ka 2025')