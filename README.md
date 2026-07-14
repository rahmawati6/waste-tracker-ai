<p align="center">
  <img src="static/img/logo-smartwaste.png" alt="SmartWaste AI Logo" width="140">
</p>

<h1 align="center">SmartWaste AI Smart City</h1>

<p align="center">
  Aplikasi web berbasis Flask untuk monitoring tempat sampah pintar, pengelolaan jadwal pengangkutan, notifikasi operasional, laporan, peta rute, dan analisis AI.
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img alt="Flask" src="https://img.shields.io/badge/Flask-3.x-000000?style=for-the-badge&logo=flask&logoColor=white">
  <img alt="MySQL" src="https://img.shields.io/badge/MySQL-Database-4479A1?style=for-the-badge&logo=mysql&logoColor=white">
  <img alt="License MIT" src="https://img.shields.io/badge/License-MIT-2E7D32?style=for-the-badge">
</p>

## Preview Aplikasi

![SmartWaste AI Application Preview](docs/screenshot-login.png)

## Tentang Proyek

SmartWaste AI Smart City dirancang sebagai dashboard operasional untuk membantu pemantauan sampah kota secara lebih cepat, terukur, dan mudah dianalisis. Sistem ini menggabungkan data tempat sampah, jadwal pengumpulan, status kapasitas, notifikasi, laporan, serta modul AI sederhana untuk mendukung pengambilan keputusan.

## Fitur Utama

- Autentikasi login menggunakan email dan password.
- Manajemen role `admin` dan `petugas`.
- Dashboard monitoring dengan ringkasan statistik, grafik, peta, jadwal, dan notifikasi.
- CRUD data tempat sampah untuk administrator.
- Pengelolaan jadwal pengumpulan dan perubahan status.
- Peta dan rute monitoring berbasis Leaflet.
- Analisis AI dengan upload gambar dan fallback prediksi.
- Laporan dengan filter, cetak, dan export CSV.
- Manajemen pengguna untuk administrator.
- Halaman error `403`, `404`, dan `500` yang konsisten dengan tampilan aplikasi.

## Teknologi

- **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-Login
- **Database:** MySQL, PyMySQL
- **Frontend:** HTML, CSS, Bootstrap, Bootstrap Icons
- **Visualisasi:** Chart.js, ApexCharts, Leaflet.js
- **AI-ready:** TensorFlow/Keras, NumPy, Pillow, OpenCV

## Struktur Proyek

```text
SmartWaste_AI/
├── ai/                         # Modul preprocessing, training, dan prediksi AI
├── database/                   # File SQL database awal
├── docs/                       # Aset dokumentasi README
├── models/                     # Model database dan placeholder model AI
├── routes/                     # Blueprint Flask
├── static/                     # CSS, JavaScript, logo, dan gambar
├── templates/                  # Template halaman aplikasi
├── app.py                      # Entry point aplikasi Flask
├── config.py                   # Konfigurasi aplikasi
├── extensions.py               # Inisialisasi ekstensi Flask
├── requirements.txt            # Dependency utama
├── requirements-ai-py310.txt   # Dependency opsional TensorFlow untuk Python 3.10
└── requirements-vision.txt     # Dependency opsional pemrosesan gambar
```

## Instalasi

Gunakan Python 3.10 atau Python 3.13.

```bash
cd C:\laragon\www\SmartWaste_AI
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Jika menggunakan Python 3.10 dan ingin mengaktifkan dukungan TensorFlow/Keras:

```bash
pip install -r requirements-ai-py310.txt
```

Jika hanya membutuhkan library pengolahan gambar tanpa TensorFlow:

```bash
pip install -r requirements-vision.txt
```

## Konfigurasi Database

Buat database MySQL bernama `smartwaste_ai`, lalu import file SQL berikut melalui phpMyAdmin atau terminal:

```text
database/smartwaste_ai.sql
```

Koneksi default:

```text
mysql+pymysql://root:@localhost/smartwaste_ai
```

Jika konfigurasi MySQL berbeda, set environment variable `DATABASE_URL`.

Contoh:

```bash
set DATABASE_URL=mysql+pymysql://user:password@localhost/smartwaste_ai
```

## Menjalankan Aplikasi

```bash
python app.py
```

Buka aplikasi di browser:

```text
http://127.0.0.1:5000
```

## Akun Default

Administrator:

```text
Email    : admin@smartwaste.com
Password : admin123
Role     : admin
```

Petugas:

```text
Email    : petugas@smartwaste.com
Password : petugas123
Role     : petugas
```

## Catatan AI

File `models/ai_model.h5` masih berupa placeholder. Jika model Keras asli atau TensorFlow belum tersedia, aplikasi tetap berjalan menggunakan fallback prediksi berdasarkan nama file atau pilihan acak.

## Lisensi

Proyek ini menggunakan lisensi **MIT**. Detail lisensi tersedia pada file [LICENSE](LICENSE).
