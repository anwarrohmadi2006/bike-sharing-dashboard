# 🚲 Bike Sharing Dashboard

Proyek analisis data dataset peminjaman sepeda menggunakan Streamlit.

## 🔗 Live Demo
Aplikasi dapat diakses melalui tautan berikut:
**[Bike Sharing Dashboard - Streamlit Cloud](https://anwarrohmadi2006-bike-sharing-dashboard-dashboard-anrpad.streamlit.app/)**

---

## 📂 Struktur Repository

```
bike-sharing-dashboard/
├── dashboard.py       # File utama aplikasi Streamlit
├── main_data.csv      # Dataset harian yang telah dibersihkan
├── hour_data.csv      # Dataset per jam yang telah dibersihkan
├── requirements.txt   # Daftar dependensi Python
└── README.md          # Dokumentasi proyek
```

---

## ⚙️ Cara Menjalankan di Lokal

### 1. Clone Repository
```bash
git clone https://github.com/anwarrohmadi2006/bike-sharing-dashboard.git
cd bike-sharing-dashboard
```

### 2. Install Dependencies
Pastikan Anda memiliki Python terinstal, lalu jalankan:
```bash
pip install -r requirements.txt
```

### 3. Jalankan Dashboard
```bash
streamlit run dashboard.py
```

---

## 📊 Deskripsi Proyek
Dashboard ini memberikan wawasan tentang:
- Pengaruh musim terhadap jumlah peminjaman sepeda.
- Pola peminjaman berdasarkan jam (Hari Kerja vs Hari Libur).
- Hubungan suhu dengan intensitas peminjaman.
- Clustering level permintaan (Rendah, Sedang, Tinggi, Sangat Tinggi).

**Author:** Anwar Rohmadi
