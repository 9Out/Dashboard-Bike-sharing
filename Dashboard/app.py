import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

# Mengatur tampilan halaman Streamlit
st.set_page_config(page_title="Bike Sharing Dashboard", page_icon="🚲", layout="wide")

# ==============================
# 1. LOAD DATA & CACHE
# ==============================
@st.cache_data
def load_data():
    # Load dataset
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DAY_PATH = os.path.join(BASE_DIR, "..", "Dashboard", "day_clean.csv")
    HOUR_DATA_PATH = os.path.join(BASE_DIR, "..", "Dashboard", "hour_clean.csv")

    day_df = pd.read_csv(DAY_PATH)
    hour_df = pd.read_csv(HOUR_DATA_PATH)
    
    # Ubah tipe data dteday menjadi datetime
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    
    # Mapping nama musim
    season_mapping = {1: 'Springer', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    day_df['season_name'] = day_df['season'].map(season_mapping)
    
    # Fungsi Clustering (Binning) Jam
    def categorize_time(hour):
        if 6 <= hour < 12: return 'Morning'
        elif 12 <= hour < 17: return 'Afternoon'
        elif 17 <= hour < 21: return 'Evening'
        else: return 'Night'
    
    hour_df['time_category'] = hour_df['hr'].apply(categorize_time)
    
    return day_df, hour_df

day_df, hour_df = load_data()

# ==============================
# 2. SIDEBAR (FILTER)
# ==============================
st.sidebar.title("🚲 Bike Sharing Analytics")
st.sidebar.image("https://raw.githubusercontent.com/dicodingacademy/assets/main/logo.png", width=200) # Logo opsional

# Filter Rentang Waktu
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:
    st.subheader("Filter Data")
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Terapkan filter ke dataframe utama
main_day_df = day_df[(day_df["dteday"] >= str(start_date)) & (day_df["dteday"] <= str(end_date))]
main_hour_df = hour_df[(hour_df["dteday"] >= str(start_date)) & (hour_df["dteday"] <= str(end_date))]

# ==============================
# 3. MAIN CONTENT (DASHBOARD)
# ==============================
st.title("🚲 Dashboard Analisis Data Bike Sharing")
st.markdown("Dashboard ini menampilkan hasil analisis penyewaan sepeda berdasarkan berbagai faktor seperti jam, musim, performa bisnis, dan segmentasi pelanggan.")
st.markdown("---")

# --- METRIK KPI ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Penyewaan (Semua)", f"{main_day_df['cnt'].sum():,}")
with col2:
    st.metric("Total Registered User", f"{main_day_df['registered'].sum():,}")
with col3:
    st.metric("Total Casual User", f"{main_day_df['casual'].sum():,}")

st.markdown("---")

# --- VISUALISASI 1: PENYEWAAN BERDASARKAN JAM ---
st.subheader("1. Pola Penyewaan Sepeda Berdasarkan Jam")

sum_order_items_df = main_hour_df.groupby("hr").cnt.sum().reset_index()
top_5_hours = sum_order_items_df.sort_values(by="cnt", ascending=False).head(5)
bottom_5_hours = sum_order_items_df.sort_values(by="cnt", ascending=True).head(5)

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))
colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="hr", y="cnt", data=top_5_hours, palette=colors, ax=ax[0], order=top_5_hours["hr"])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Jam (hr)", fontsize=12)
ax[0].set_title("Jam Penyewaan Sepeda Terbanyak", loc="center", fontsize=15)
ax[0].tick_params(axis='y', labelsize=12)

sns.barplot(x="hr", y="cnt", data=bottom_5_hours, palette=colors, ax=ax[1], order=bottom_5_hours["hr"])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Jam (hr)", fontsize=12)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Jam Penyewaan Sepeda Tersedikit", loc="center", fontsize=15)
ax[1].tick_params(axis='y', labelsize=12)

st.pyplot(fig)

with st.expander("Lihat Penjelasan"):
    st.write(
        """Terlihat jelas bahwa puncak penyewaan terjadi pada pukul **17:00**, 
        yang selaras dengan jam sibuk pulang kerja/sekolah. 
        Sebaliknya, penyewaan sangat sepi pada dini hari (pukul 04:00)."""
    )

# --- VISUALISASI 2 & 5: MUSIM DAN CLUSTERING ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("2. Penyewaan Berdasarkan Musim")
    season_rentals = main_day_df.groupby('season_name')['cnt'].sum().reset_index()
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    colors_season = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"] 
    sns.barplot(x="season_name", y="cnt", data=season_rentals.sort_values(by="cnt", ascending=False), palette=colors_season, ax=ax2)
    ax2.set_xlabel("Musim", fontsize=12)
    ax2.set_ylabel("Total Penyewaan", fontsize=12)
    st.pyplot(fig2)

# Di bawah st.pyplot(fig2) pada col1:
    with st.expander("Lihat Penjelasan"):
        st.write("Musim Gugur (Fall) merupakan musim favorit pelanggan untuk bersepeda, sedangkan Musim Semi (Springer) menjadi yang paling sepi.")

with col2:
    st.subheader("3. Analisis Clustering (Waktu)")
    time_category_df = main_hour_df.groupby('time_category')['cnt'].sum().reset_index()
    time_category_df['time_category'] = pd.Categorical(time_category_df['time_category'], categories=['Morning', 'Afternoon', 'Evening', 'Night'], ordered=True)
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    sns.barplot(x='time_category', y='cnt', data=time_category_df.sort_values('time_category'), palette="viridis", ax=ax3)
    ax3.set_xlabel('Kelompok Waktu', fontsize=12)
    ax3.set_ylabel('Total Penyewaan', fontsize=12)
    st.pyplot(fig3)

# Di bawah st.pyplot(fig3) pada col2:
    with st.expander("Lihat Penjelasan"):
        st.write("Berdasarkan pengelompokan waktu, sore hari (evening) mendominasi jumlah penyewaan terbanyak dibandingkan waktu lainnya.")

# --- VISUALISASI 3: PERFORMA KUARTAL ---
st.subheader("4. Tren Total Penyewaan per Kuartal")
fig4, ax4 = plt.subplots(figsize=(14, 5))
quarterly_counts = main_day_df.set_index('dteday').resample('Qs')['cnt'].sum()
ax4.plot(quarterly_counts.index, quarterly_counts.values, marker='o', linewidth=2, color="#72BCD4")
ax4.set_xlabel('Kuartal (Tahun)', fontsize=12)
ax4.set_ylabel('Total Penyewaan', fontsize=12)
ax4.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig4)

with st.expander("Lihat Penjelasan"):
    st.write(
        """Terdapat **pola musiman yang berulang**, di mana penyewaan selalu naik di pertengahan tahun (Kuartal 2 & 3). Serta penurunan pada akhir tahun (Kuartal 4) yang konsisten terjadi di kedua tahun. 
        Selain itu, grafik ini membuktikan adanya **pertumbuhan bisnis yang sangat pesat** dari tahun 2011 ke 2012."""
    )

# --- VISUALISASI 4: SEGMENTASI PELANGGAN ---
st.subheader("5. Segmentasi Pelanggan (Registered vs Casual)")
col3, col4 = st.columns(2)

with col3:
    user_total = main_hour_df[['registered', 'casual']].sum()
    fig5, ax5 = plt.subplots(figsize=(8, 6))
    ax5.pie(
        user_total, 
        labels=['Registered', 'Casual'], 
        autopct='%1.1f%%', 
        colors=['#72BCD4', '#FFA07A'], 
        explode=(0.1, 0), 
        startangle=90,
        shadow=True,
        textprops={'fontsize': 12}
    )
    ax5.set_title('Persentase Total Pengguna', fontsize=15)
    st.pyplot(fig5)

with col4:
    yearly_users = main_hour_df.groupby('yr').agg({'registered': 'sum', 'casual': 'sum'})
    yearly_users.index = ['2011', '2012']
    
    fig6, ax6 = plt.subplots(figsize=(8, 6))
    yearly_users.plot(kind='bar', color=['#72BCD4', '#FFA07A'], edgecolor='black', width=0.6, ax=ax6)
    ax6.set_title('Pertumbuhan Pengguna (2011 vs 2012)', fontsize=15)
    ax6.set_xlabel('Tahun', fontsize=12)
    ax6.set_ylabel('Total Penyewaan', fontsize=12)
    ax6.tick_params(axis='x', rotation=0)
    ax6.legend(title='Tipe Pengguna')
    st.pyplot(fig6)
    
# Bisa ditaruh di bawah grafik bar chart (fig6)
with st.expander("Lihat Kesimpulan Segmentasi Pelanggan"):
    st.write(
        """Pelanggan tetap (**Registered**) adalah tulang punggung bisnis ini karena menyumbang **81.2%** dari total penyewaan. 
        Hebatnya, baik pengguna *Registered* maupun *Casual* sama-sama mengalami pertumbuhan yang pesat dari tahun ke tahun."""
    )

st.caption("Copyright © Nirot 2026 - Dicoding Data Analysis Project")