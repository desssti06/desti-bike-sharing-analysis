import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

# Judul Dashboard
st.title("Dashboard Penyewaan Sepeda")

df = pd.read_csv(os.path.join(os.path.dirname(__file__), "all_data.csv"))
# Load dataset

col1, col2 = st.columns(2)

### === VISUALISASI 1: Penyewaan Sepeda Berdasarkan Musim ===
with col1:
    season_labels = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    df['season_label'] = df['season_x'].map(season_labels)
    df_season_avg = df.groupby('season_label')['cnt_y'].mean().reset_index()

    custom_palette_season = {
        'Spring': '#77DD77',  
        'Summer': '#FFD700',  
        'Fall': '#FF8C00',    
        'Winter': '#1E90FF'  
    }

    fig, ax1 = plt.subplots(figsize=(10, 8))
    sns.barplot(
        x='season_label', 
        y='cnt_y', 
        hue='season_label', 
        data=df_season_avg, 
        palette=custom_palette_season, 
        legend=False, 
        ax=ax1
    )

    ax1.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Musim" ,fontsize=15)
    ax1.set_xlabel("Musim", fontsize=10)
    ax1.set_ylabel("Rata-rata Penyewaan Sepeda", fontsize=10)

    st.pyplot(fig)


### === VISUALISASI 2: Penyewaan Sepeda Berdasarkan Kondisi Cuaca ===
with col2:
    weather_labels = {
        1: "Cerah",
        2: "Berawan",
        3: "Hujan Ringan",
        4: "Hujan Deras"
    }

    custom_palette_weather = {
        "Cerah": "#F1C40F",        # Kuning
        "Berawan": "#BDC3C7",      # Abu-abu
        "Hujan Ringan": "#3498DB", # Biru
        "Hujan Deras": "#2C3E50"   # Biru Tua
    }

    df["Cuaca"] = df["weathersit_x"].map(weather_labels)

    df_cuaca_avg = df.groupby("Cuaca")["cnt_x"].mean().reset_index()

    fig2, ax = plt.subplots(figsize=(10, 8))
    sns.barplot(
        x="Cuaca", 
        y="cnt_x", 
        hue="Cuaca",  
        data=df_cuaca_avg, 
        palette=custom_palette_weather, 
        legend=False, 
        ax=ax
    )

    ax.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca", fontsize=15)
    ax.set_xlabel("Kondisi Cuaca", fontsize=10)
    ax.set_ylabel("Rata-rata Jumlah Penyewaan", fontsize=10)
    ax.grid(axis="y", linestyle="--", alpha=0.7)

    st.pyplot(fig2)
    
### === VISUALISASI 3: Penyewaan Sepeda pada Hari Kerja vs Akhir Pekan ===
day_labels = {0: 'Akhir Pekan', 1: 'Hari Kerja'}
df['workingday_label'] = df['workingday_x'].map(day_labels)
df_day_avg = df.groupby('workingday_label')['cnt_x'].mean().reset_index()

custom_palette_day = {
    'Hari Kerja': '#3498db',  
    'Akhir Pekan': '#e74c3c'  
}

fig1, ax2 = plt.subplots(figsize=(10, 5))
sns.barplot(
    x='workingday_label', 
    y='cnt_x', 
    hue='workingday_label', 
    data=df_day_avg, 
    palette=custom_palette_day, 
    legend=False, 
    ax=ax2
)



### === VISUALISASI 4: Korelasi Temperatur, Kelembaban, dan Penyewaan ===
korelasi = df[['temp_x', 'hum_x', 'cnt_x']].corr()
fig3, ax3 = plt.subplots(nrows=1, ncols=3, figsize=(15, 5))

# Plot 1: Hubungan Temperatur dengan Jumlah Penyewaan Sepeda
sns.scatterplot(x=df["temp_x"], y=df["cnt_x"], alpha=0.6, color="red", label="Data", ax=ax3[0]) 
sns.regplot(x=df["temp_x"], y=df["cnt_x"], line_kws={"color": "darkred"}, scatter=False, label="Regresi", ax=ax3[0])
ax3[0].set_title("Temperatur vs Penyewaan", fontsize=14)
ax3[0].set_xlabel("Temperatur", fontsize=12)
ax3[0].set_ylabel("Jumlah Penyewaan", fontsize=12)
ax3[0].tick_params(axis='x', rotation=45)
ax3[0].grid(True, linestyle="--", alpha=0.7)
ax3[0].legend()

# Plot 2: Hubungan Kelembaban dengan Jumlah Penyewaan Sepeda
sns.scatterplot(x=df["hum_x"], y=df["cnt_x"], alpha=0.6, color="blue", label="Data", ax=ax3[1])
sns.regplot(x=df["hum_x"], y=df["cnt_x"], line_kws={"color": "darkblue"}, scatter=False, label="Regresi", ax=ax3[1])
ax3[1].set_title("Kelembaban vs Penyewaan", fontsize=14)
ax3[1].set_xlabel("Kelembaban", fontsize=12)
ax3[1].set_ylabel("Jumlah Penyewaan", fontsize=12)
ax3[1].tick_params(axis='x', rotation=45)
ax3[1].grid(True, linestyle="--", alpha=0.7)
ax3[1].legend()

# Plot 3: Hubungan Temperatur dengan Kelembaban
sns.scatterplot(x=df["temp_x"], y=df["hum_x"], alpha=0.6, color="green", marker="o", label="Data", ax=ax3[2])
sns.regplot(x=df["temp_x"], y=df["hum_x"], line_kws={"color": "darkgreen"}, scatter=False, label="Regresi", ax=ax3[2])
ax3[2].set_title("Temperatur vs Kelembaban", fontsize=14)
ax3[2].set_xlabel("Temperatur", fontsize=12)
ax3[2].set_ylabel("Kelembaban", fontsize=12)
ax3[2].tick_params(axis='x', rotation=45)
ax3[2].grid(True, linestyle="--", alpha=0.7)
ax3[2].legend()

plt.suptitle("Tren Penyewaan Sepeda (2011-2012)", fontsize=20)
st.pyplot(fig3)

df["year"] = pd.to_datetime(df["dteday_x"]).dt.year
df["month"] = pd.to_datetime(df["dteday_x"]).dt.month
sewa_bulan = df.groupby(["year", "month"])['cnt_y'].sum().reset_index()


fig4, ax = plt.subplots(figsize=(10, 5))
for year in [2011, 2012]:
    subset = sewa_bulan[sewa_bulan["year"] == year]
    ax.plot(subset["month"], subset["cnt_y"], marker="o", label=str(year))

ax.set_title("Tren Penyewaan Sepeda (2011-2012)")
ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah Penyewaan")
ax.set_xticks(range(1, 13))
ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"])
ax.legend()
ax.grid(True)

st.pyplot(fig4)

df['dteday_x'] = pd.to_datetime(df['dteday_x'])
latest_date = df['dteday_x'].max()

# Hitung RFM berdasarkan tanggal
rfm = df.groupby('dteday_x').agg(
    Recency=('dteday_x', lambda x: (latest_date - x.max()).days),
    Frequency=('cnt_y', 'count'),
    Monetary=('cnt_y', 'sum')
).reset_index()

# Buat figure untuk subplot
fig5, ax = plt.subplots(nrows=1, ncols=3, figsize=(30, 6))
colors = ["#72BCD4"] * 5

# Bar plot untuk Recency
sns.barplot(
    y="Recency", x="dteday_x", hue="dteday_x",
    data=rfm.sort_values(by="Recency", ascending=True).head(5),
    palette=colors, ax=ax[0], legend=False
)
ax[0].set_title("5 Hari Terbaru Sewa Sepeda", fontsize=18)
ax[0].set_xlabel("Tanggal")
ax[0].set_ylabel("Hari Sejak Terakhir Sewa")
ax[0].tick_params(axis='x', labelsize=12, rotation=45)

# Bar plot untuk Frequency
sns.barplot(
    y="Frequency", x="dteday_x", hue="dteday_x",
    data=rfm.sort_values(by="Frequency", ascending=False).head(5),
    palette=colors, ax=ax[1], legend=False
)
ax[1].set_title("5 Hari dengan Sewa Terbanyak", fontsize=18)
ax[1].set_xlabel("Tanggal")
ax[1].set_ylabel("Jumlah Penyewaan per Hari")
ax[1].tick_params(axis='x', labelsize=12, rotation=45)

# Bar plot untuk Monetary
sns.barplot(
    y="Monetary", x="dteday_x", hue="dteday_x",
    data=rfm.sort_values(by="Monetary", ascending=False).head(5),
    palette=colors, ax=ax[2], legend=False
)
ax[2].set_title("5 Hari dengan Pendapatan Tertinggi", fontsize=18)
ax[2].set_xlabel("Tanggal")
ax[2].set_ylabel("Total Penyewaan per Hari")
ax[2].tick_params(axis='x', labelsize=12, rotation=45)

plt.suptitle("Analisis RFM Penyewaan Sepeda", fontsize=25)

st.pyplot(fig5)
