import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

# Judul Dashboard
st.title("Dashboard Penyewaan Sepeda")

# Load dataset
df = pd.read_csv(os.path.join(os.path.dirname(__file__), "all_data.csv"))
df['dteday_x'] = pd.to_datetime(df['dteday_x'])

# Mapping label musim dan cuaca
season_labels = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
weather_labels = {1: "Cerah", 2: "Berawan", 3: "Hujan Ringan", 4: "Hujan Deras"}
day_labels = {0: "Akhir Pekan", 1: "Hari Kerja"}

# Sidebar untuk filter interaktif
st.sidebar.header("Filter Data")
selected_season_labels = st.sidebar.multiselect("Pilih Musim", options=list(season_labels.values()), default=list(season_labels.values()))
selected_day_labels = st.sidebar.multiselect("Pilih Kondisi Hari", options=list(day_labels.values()), default=list(day_labels.values()))
selected_weather_labels = st.sidebar.multiselect("Pilih Kondisi Cuaca", options=list(weather_labels.values()), default=list(weather_labels.values()))
start_date = st.sidebar.date_input("Pilih Tanggal Awal", df["dteday_x"].min())
end_date = st.sidebar.date_input("Pilih Tanggal Akhir", df["dteday_x"].max())

# Konversi tanggal
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filter dataset
df_filtered = df[(df["dteday_x"] >= start_date) & (df["dteday_x"] <= end_date)]
df_filtered['Musim'] = df_filtered['season_x'].map(season_labels)
df_filtered['Hari'] = df_filtered['workingday_x'].map(day_labels)
df_filtered['Cuaca'] = df_filtered['weathersit_x'].map(weather_labels)
df_filtered = df_filtered[df_filtered['Musim'].isin(selected_season_labels)]
df_filtered = df_filtered[df_filtered['Hari'].isin(selected_day_labels)]
df_filtered = df_filtered[df_filtered['Cuaca'].isin(selected_weather_labels)]


# === VISUALISASI 1: Penyewaa Sepeda Berdasarkan Musim ===
df_season_avg = df_filtered.groupby('Musim', as_index=False)['cnt_x'].mean().reset_index()
df_season_avg = df_season_avg.sort_values(by="cnt_x", ascending=True)
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='Musim', y='cnt_x', data=df_season_avg, palette=sns.color_palette("Blues", len(df_season_avg)), ax=ax)
ax.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Musim")
ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah Penyewaa")
st.pyplot(fig)

# VISUALISASI 2: Penyewaan Sepeda Berdasarkan Hari
df_day_avg = df_filtered.groupby("Hari", as_index=False)["cnt_x"].mean().reset_index()
df_day_avg = df_day_avg.sort_values(by="cnt_x", ascending=True)
fig2, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x="Hari", y="cnt_x", data=df_day_avg, palette=sns.color_palette("Blues", len(df_day_avg)), ax=ax)
ax.set_title("Rata-rata Penyewaan Sepeda pada Hari Kerja vs Akhir Pekan")
ax.set_xlabel("Jenis Hari")
ax.set_ylabel("Rata-rata Penyewaan")
st.pyplot(fig2)


# === VISUALISASI 3: Penyewaan Sepeda Berdasarkan Kondisi Cuaca ===
df_cuaca_avg = df_filtered.groupby("Cuaca")['cnt_x'].mean().reset_index()
df_cuaca_avg = df_cuaca_avg.sort_values(by="cnt_x", ascending=True)
fig3, ax2 = plt.subplots(figsize=(10, 6))
sns.barplot(x="Cuaca", y="cnt_x", data=df_cuaca_avg, palette=sns.color_palette("Blues", len(df_cuaca_avg)), ax=ax2)
ax2.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca")
ax2.set_xlabel("Cuaca")
ax2.set_ylabel("Jumlah Penyewaa")
st.pyplot(fig3)

# === VISUALISASI 4: Tren Penyewaan Sepeda ===
df_filtered["year"] = df_filtered["dteday_x"].dt.year
df_filtered["month"] = df_filtered["dteday_x"].dt.month
sewa_bulan = df_filtered.groupby(["year", "month"])["cnt_y"].sum().reset_index()

fig4, ax = plt.subplots(figsize=(10, 5))
for year in sewa_bulan["year"].unique():
    subset = sewa_bulan[sewa_bulan["year"] == year]
    ax.plot(subset["month"], subset["cnt_y"], marker="o", label=str(year))

ax.set_xticks(range(1, 13))
ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"])
ax.set_title("Tren Penyewaan Sepeda 2011-2012")
ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah Penyewaa")
ax.legend()
ax.grid(True)
st.pyplot(fig4)

### === VISUALISASI 5: Korelasi Temperatur, Kelembaban, dan Penyewaan ===
korelasi = df[['temp_x', 'hum_x', 'cnt_x']].corr()
fig5, ax = plt.subplots(nrows=1, ncols=3, figsize=(15, 5))

# Plot 1: Hubungan Temperatur dengan Jumlah Penyewaan Sepeda
sns.scatterplot(x=df["temp_x"], y=df["cnt_x"], alpha=0.6, color="red", label="Data", ax=ax[0]) 
sns.regplot(x=df["temp_x"], y=df["cnt_x"], line_kws={"color": "darkred"}, scatter=False, label="Regresi", ax=ax[0])
ax[0].set_title("Temperatur vs Penyewaan", fontsize=14)
ax[0].set_xlabel("Temperatur", fontsize=12)
ax[0].set_ylabel("Jumlah Penyewaa", fontsize=12)
ax[0].tick_params(axis='x', rotation=45)
ax[0].grid(True, linestyle="--", alpha=0.7)
ax[0].legend()

# Plot 2: Hubungan Kelembaban dengan Jumlah Penyewaan Sepeda
sns.scatterplot(x=df["hum_x"], y=df["cnt_x"], alpha=0.6, color="blue", label="Data", ax=ax[1])
sns.regplot(x=df["hum_x"], y=df["cnt_x"], line_kws={"color": "darkblue"}, scatter=False, label="Regresi", ax=ax[1])
ax[1].set_title("Kelembaban vs Penyewaan", fontsize=14)
ax[1].set_xlabel("Kelembaban", fontsize=12)
ax[1].set_ylabel("Jumlah Penyewaa", fontsize=12)
ax[1].tick_params(axis='x', rotation=45)
ax[1].grid(True, linestyle="--", alpha=0.7)
ax[1].legend()

# Plot 3: Hubungan Temperatur dengan Kelembaban
sns.scatterplot(x=df["temp_x"], y=df["hum_x"], alpha=0.6, color="green", marker="o", label="Data", ax=ax[2])
sns.regplot(x=df["temp_x"], y=df["hum_x"], line_kws={"color": "darkgreen"}, scatter=False, label="Regresi", ax=ax[2])
ax[2].set_title("Temperatur vs Kelembaban", fontsize=14)
ax[2].set_xlabel("Temperatur", fontsize=12)
ax[2].set_ylabel("Kelembaban", fontsize=12)
ax[2].tick_params(axis='x', rotation=45)
ax[2].grid(True, linestyle="--", alpha=0.7)
ax[2].legend()

plt.suptitle("Korelasi Temperatur, Kelembaban, dan Penyewaan", fontsize=20)
st.pyplot(fig5)


### === VISUALISASI 5: Analisis Lanjutan : Clusterring ===

# Fungsi kategorisasi waktu
def categorize_time(hour):
    if 6 <= hour < 10:
        return "Pagi"
    elif 10 <= hour < 14:
        return "Siang"
    elif 14 <= hour < 18:
        return "Sore"
    else:
        return "Malam"

df["Waktu"] = df["hr"].apply(categorize_time)

ratarata_kategori_waktu= df.groupby("Waktu")["cnt_y"].mean()

ratarata_kategori_waktu = ratarata_kategori_waktu.reset_index()
ratarata_kategori_waktu = ratarata_kategori_waktu.sort_values(by="cnt_y", ascending=True)
num_colors = len(ratarata_kategori_waktu)
color_palette = sns.color_palette("Blues", num_colors + 2)[1:]  
colors = dict(zip(ratarata_kategori_waktu["Waktu"], color_palette))

# Membuat figure
fig6, ax = plt.subplots(figsize=(5, 3))

# Membuat barplot
sns.barplot(
    x="Waktu", 
    y="cnt_y", 
    hue="Waktu",
    data=ratarata_kategori_waktu, 
    palette=colors, 
    legend=False,
    ax=ax
)

# Mengatur tampilan plot
ax.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Kategori Waktu", fontsize=10)
ax.set_xlabel("Kategori Waktu", fontsize=8)
ax.set_ylabel("Rata-rata Jumlah Penyewaan", fontsize=8)

# Menampilkan plot di Streamlit
st.pyplot(fig6)