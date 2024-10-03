import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Load data dari CSV
season_rental_totals = pd.read_csv('dashboard/season_rental_totals.csv') 
workingday_rental_totals = pd.read_csv('dashboard/workingday_rental_totals.csv') 

# Convert tipe data 'dteday' menjadi datetime
season_rental_totals['dteday'] = pd.to_datetime(season_rental_totals['dteday'])

# Sidebar untuk filter tanggal
st.sidebar.header("Filter Tanggal")
selected_date_range = st.sidebar.date_input("Pilih Rentang Tanggal:", 
                                            [season_rental_totals['dteday'].min(), 
                                             season_rental_totals['dteday'].max()])

# Rentang tanggal dalam format datetime
start_date = pd.to_datetime(selected_date_range[0])
end_date = pd.to_datetime(selected_date_range[1])

# Filter dataframe berdasarkan rentang tanggal yang dipilih
filtered_data = season_rental_totals[(season_rental_totals['dteday'] >= start_date) & 
                                     (season_rental_totals['dteday'] <= end_date)]

# Set up bagian utama dari dashboard
st.title('Dashboard Penyewaan Sepeda :bicyclist:')

# Bar chart untuk season
st.subheader('Total Penyewaan Sepeda Berdasarkan Season')
fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.barplot(x='season', y='cnt', data=filtered_data, palette='Blues_r', ci=None, ax=ax1)
ax1.set_title('Total Penyewaan Sepeda Berdasarkan Season', fontsize=16)
ax1.set_xlabel('Season', fontsize=14)
ax1.set_ylabel('Total Penyewaan', fontsize=14)
st.pyplot(fig1)

# Filter workingday_rental_totals berdasarkan rentang tanggal
# Mengubah kolom 'dteday' ke datetime jika perlu
workingday_rental_totals['dteday'] = pd.to_datetime(workingday_rental_totals['dteday'])

# Mengambil data yang relevan berdasarkan tanggal
workingday_filtered = workingday_rental_totals[
    (workingday_rental_totals['dteday'] >= start_date) & 
    (workingday_rental_totals['dteday'] <= end_date)
]

# Menghitung total penyewaan untuk Hari Kerja dan Hari Libur
total_no = workingday_filtered.loc[workingday_filtered['workingday'] == 'No', 'cnt'].sum()
total_yes = workingday_filtered.loc[workingday_filtered['workingday'] == 'Yes', 'cnt'].sum()

# Menyusun data untuk plotting
categories = ['Hari Libur', 'Hari Kerja']
values = [total_no, total_yes]

# Bar chart untuk hari kerja dan hari libur
st.subheader('Total Penyewaan Sepeda Saat Hari Kerja dan Hari Libur')
fig2, ax2 = plt.subplots(figsize=(8, 5))

# Membuat barplot
sns.barplot(x=categories, y=values, palette='Blues', ax=ax2)

# Menambahkan judul dan label
ax2.set_title('Total Penyewaan Sepeda Saat Hari Kerja dan Hari Libur', fontsize=16)
ax2.set_ylabel('Total Penyewaan', fontsize=14)
ax2.set_xticklabels(categories, rotation=0)

# Menampilkan plot
st.pyplot(fig2)
