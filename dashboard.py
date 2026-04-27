import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ─── Konfigurasi Halaman ────────────────────────────────────────────────────
st.set_page_config(
    page_title='Bike Sharing Dashboard',
    page_icon='🚲',
    layout='wide'
)

# ─── Load Data ───────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    base = os.path.dirname(__file__)
    day_df  = pd.read_csv(os.path.join(base, 'main_data.csv'))
    hour_df = pd.read_csv(os.path.join(base, 'hour_data.csv'))
    day_df['dteday']  = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    return day_df, hour_df

day_df, hour_df = load_data()

# ─── Sidebar ─────────────────────────────────────────────────────────────────
st.sidebar.title('🚲 Filter Data')
st.sidebar.markdown('---')

all_seasons = ['Spring', 'Summer', 'Fall', 'Winter']
selected_seasons = st.sidebar.multiselect(
    '🍂 Pilih Musim:', options=all_seasons, default=all_seasons
)

year_labels = {0: '2011', 1: '2012'}
selected_year = st.sidebar.selectbox(
    '📅 Pilih Tahun:', options=[0, 1], format_func=lambda x: year_labels[x]
)

st.sidebar.markdown('---')
st.sidebar.caption('Proyek Analisis Data · Dicoding')

# ─── Filter Data ─────────────────────────────────────────────────────────────
filtered_day  = day_df[
    (day_df['season_label'].isin(selected_seasons)) &
    (day_df['yr'] == selected_year)
]
filtered_hour = hour_df[hour_df['yr'] == selected_year]

# ─── Header ──────────────────────────────────────────────────────────────────
st.title('🚲 Dashboard Analisis Bike Sharing')
st.markdown(
    f'> **Dataset:** Capital Bikeshare System (2011–2012) — '
    f'Tahun: **{year_labels[selected_year]}** | '
    f'Musim: **{", ".join(selected_seasons) if selected_seasons else "—"}**'
)
st.markdown('---')

if filtered_day.empty:
    st.warning('⚠️ Tidak ada data untuk filter yang dipilih. Silakan ubah filter di sidebar.')
    st.stop()

# ─── Metrik Utama ─────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric('📦 Total Peminjaman',     f"{filtered_day['cnt'].sum():,}")
with col2:
    st.metric('📊 Rata-Rata Harian',     f"{filtered_day['cnt'].mean():.0f}")
with col3:
    st.metric('🔺 Peminjaman Tertinggi', f"{filtered_day['cnt'].max():,}")
with col4:
    st.metric('🔻 Peminjaman Terendah',  f"{filtered_day['cnt'].min():,}")

st.markdown('---')

# ─── Tabs ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    '🍂 Peminjaman per Musim',
    '⏰ Pola per Jam',
    '🗓️ Heatmap Mingguan',
    '📈 Clustering Demand',
])

# ═══ TAB 1 ═══════════════════════════════════════════════════════════════════
with tab1:
    st.subheader('Pertanyaan 1: Bagaimana pengaruh musim terhadap jumlah peminjaman sepeda?')

    season_order = [s for s in ['Spring', 'Summer', 'Fall', 'Winter']
                    if s in filtered_day['season_label'].unique()]
    season_avg   = filtered_day.groupby('season_label')['cnt'].mean().reindex(season_order)
    color_map    = {'Spring': '#4CAF50', 'Summer': '#FF9800',
                    'Fall':   '#F44336', 'Winter': '#2196F3'}
    bar_colors   = [color_map[s] for s in season_order]

    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots(figsize=(7, 5))
        bars = ax.bar(season_avg.index, season_avg.values,
                      color=bar_colors, edgecolor='white', linewidth=0.8, width=0.55)
        for bar, val in zip(bars, season_avg.values):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 40,
                    f'{val:.0f}', ha='center', fontweight='bold', fontsize=10)
        ax.set_title('Rata-Rata Peminjaman per Musim', fontweight='bold')
        ax.set_xlabel('Musim')
        ax.set_ylabel('Rata-Rata Peminjaman Harian')
        ax.set_ylim(0, season_avg.max() * 1.2)
        ax.grid(axis='y', alpha=0.3)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        st.pyplot(fig)
        plt.close()

    with col2:
        weather_avg = (filtered_day.groupby('weather_label')['cnt']
                       .mean().sort_values(ascending=False))
        fig, ax = plt.subplots(figsize=(7, 5))
        sns.barplot(x=weather_avg.values, y=weather_avg.index, ax=ax, palette='viridis_r')
        for i, val in enumerate(weather_avg.values):
            ax.text(val + 30, i, f'{val:.0f}', va='center', fontweight='bold', fontsize=10)
        ax.set_title('Rata-Rata Peminjaman per Kondisi Cuaca', fontweight='bold')
        ax.set_xlabel('Rata-Rata Peminjaman')
        ax.set_ylabel('Kondisi Cuaca')
        ax.grid(axis='x', alpha=0.3)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        st.pyplot(fig)
        plt.close()

    st.info('💡 **Insight:** Musim **Fall (Gugur)** memiliki peminjaman tertinggi. '
            'Cuaca cerah mendorong ≈3× lebih banyak peminjaman dibanding cuaca buruk.')

# ═══ TAB 2 ═══════════════════════════════════════════════════════════════════
with tab2:
    st.subheader('Pertanyaan 2: Pola jam peminjaman di hari kerja vs hari libur')

    hour_work    = (filtered_hour[filtered_hour['workingday'] == 1]
                    .groupby('hr')['cnt'].mean())
    hour_holiday = (filtered_hour[filtered_hour['workingday'] == 0]
                    .groupby('hr')['cnt'].mean())

    fig, ax = plt.subplots(figsize=(13, 5))
    if not hour_work.empty:
        ax.plot(hour_work.index, hour_work.values, marker='o', linewidth=2.5,
                color='#2196F3', label='Hari Kerja', markersize=4)
        ax.axvline(x=8,  color='#2196F3', alpha=0.2, linewidth=2)
        ax.axvline(x=17, color='#2196F3', alpha=0.2, linewidth=2)
        ax.annotate('Jam 08:00\n(Berangkat Kerja)',
                    xy=(8, hour_work.get(8, 0)), xytext=(9.3, hour_work.get(8, 0) + 25),
                    arrowprops=dict(arrowstyle='->', color='#2196F3'), fontsize=8.5, color='#2196F3')
        ax.annotate('Jam 17:00\n(Pulang Kerja)',
                    xy=(17, hour_work.get(17, 0)), xytext=(14.3, hour_work.get(17, 0) + 25),
                    arrowprops=dict(arrowstyle='->', color='#2196F3'), fontsize=8.5, color='#2196F3')
    if not hour_holiday.empty:
        ax.plot(hour_holiday.index, hour_holiday.values, marker='s', linewidth=2.5,
                color='#FF9800', label='Hari Libur/Weekend', markersize=4, linestyle='--')
        ax.axvline(x=13, color='#FF9800', alpha=0.2, linewidth=2)
        ax.annotate('Jam 13:00\n(Puncak Libur)',
                    xy=(13, hour_holiday.get(13, 0)), xytext=(10, hour_holiday.get(13, 0) + 20),
                    arrowprops=dict(arrowstyle='->', color='#FF9800'), fontsize=8.5, color='#FF9800')

    ax.set_title('Pola Peminjaman Sepeda per Jam: Hari Kerja vs Hari Libur', fontweight='bold')
    ax.set_xlabel('Jam (0–23)')
    ax.set_ylabel('Rata-Rata Peminjaman')
    ax.set_xticks(range(24))
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    st.pyplot(fig)
    plt.close()

    c1, c2 = st.columns(2)
    with c1:
        if not hour_work.empty:
            pk = int(hour_work.idxmax())
            st.metric('🔵 Jam Puncak Hari Kerja', f'Jam {pk:02d}:00',
                      delta=f'≈{hour_work[pk]:.0f} peminjaman')
    with c2:
        if not hour_holiday.empty:
            pk = int(hour_holiday.idxmax())
            st.metric('🟠 Jam Puncak Hari Libur', f'Jam {pk:02d}:00',
                      delta=f'≈{hour_holiday[pk]:.0f} peminjaman')

    st.info('💡 **Insight:** Hari kerja membentuk pola **"M"** (jam 08 & 17 — commuting). '
            'Hari libur membentuk pola **"bell curve"** dengan puncak jam 12–13.')

# ═══ TAB 3 ═══════════════════════════════════════════════════════════════════
with tab3:
    st.subheader('Heatmap: Intensitas Peminjaman per Jam dan Hari dalam Seminggu')

    pivot     = filtered_hour.pivot_table(
        values='cnt', index='hr', columns='weekday_label', aggfunc='mean')
    day_order = [d for d in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
                 if d in pivot.columns]
    pivot     = pivot[day_order]

    fig, ax = plt.subplots(figsize=(12, 7))
    sns.heatmap(pivot, cmap='YlOrRd', ax=ax, linewidths=0.4,
                cbar_kws={'label': 'Rata-Rata Peminjaman'})
    ax.set_title('Heatmap Peminjaman: Jam vs Hari dalam Seminggu', fontweight='bold')
    ax.set_xlabel('Hari dalam Seminggu')
    ax.set_ylabel('Jam (0–23)')
    ax.invert_yaxis()
    st.pyplot(fig)
    plt.close()

    st.info('💡 **Insight:** Kotak merah tua muncul di jam 07–09 dan 17–19 pada hari kerja, '
            'mengonfirmasi pola commuting. Sabtu–Minggu lebih merata sepanjang jam 10–18.')

# ═══ TAB 4 ═══════════════════════════════════════════════════════════════════
with tab4:
    st.subheader('Analisis Lanjutan: Clustering Demand Level (Binning)')
    st.markdown('Hari-hari dikelompokkan ke dalam 4 level permintaan menggunakan teknik **binning**.')

    day_plot = filtered_day.copy()
    day_plot['demand_level'] = pd.cut(
        day_plot['cnt'],
        bins=[0, 2000, 4000, 6000, 10000],
        labels=['Rendah', 'Sedang', 'Tinggi', 'Sangat Tinggi']
    )

    c1, c2 = st.columns(2)
    demand_colors_map = {'Rendah': '#2196F3', 'Sedang': '#4CAF50',
                         'Tinggi': '#FF9800', 'Sangat Tinggi': '#F44336'}

    with c1:
        demand_count = day_plot['demand_level'].value_counts().reindex(
            ['Rendah', 'Sedang', 'Tinggi', 'Sangat Tinggi'])
        fig, ax = plt.subplots(figsize=(6, 5))
        bars = ax.bar(demand_count.index, demand_count.values,
                      color=list(demand_colors_map.values()), edgecolor='white')
        for bar, val in zip(bars, demand_count.values):
            if pd.notna(val):
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                        str(int(val)), ha='center', fontweight='bold')
        ax.set_title('Jumlah Hari per Demand Level', fontweight='bold')
        ax.set_xlabel('Demand Level')
        ax.set_ylabel('Jumlah Hari')
        ax.grid(axis='y', alpha=0.3)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        st.pyplot(fig)
        plt.close()

    with c2:
        if 'temp_actual' in day_plot.columns:
            fig, ax = plt.subplots(figsize=(6, 5))
            for level, color in demand_colors_map.items():
                mask = day_plot['demand_level'] == level
                if mask.any():
                    ax.scatter(day_plot[mask]['temp_actual'], day_plot[mask]['cnt'],
                               c=color, label=level, alpha=0.65, s=22)
            ax.set_title('Suhu vs Peminjaman (per Demand Level)', fontweight='bold')
            ax.set_xlabel('Suhu Aktual (°C)')
            ax.set_ylabel('Jumlah Peminjaman')
            ax.legend(title='Level', fontsize=9)
            ax.grid(alpha=0.3)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            st.pyplot(fig)
            plt.close()

    summary = (day_plot.groupby('demand_level', observed=True)['cnt']
               .agg(['count', 'mean', 'min', 'max'])
               .round(0).astype(int))
    summary.columns = ['Jumlah Hari', 'Rata-rata', 'Min', 'Max']
    st.dataframe(summary, use_container_width=True)

    st.info('💡 **Insight:** Demand "Sangat Tinggi" (>6.000/hari) terkonsentrasi di suhu >20°C '
            'dan musim Fall/Summer. Demand "Rendah" (<2.000/hari) dominan di Spring dan cuaca buruk.')

# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown('---')
st.caption('📊 Proyek Analisis Data · Belajar Fundamental Analisis Data · Dicoding')
