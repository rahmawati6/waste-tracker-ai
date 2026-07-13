# SmartWaste AI Smart City

SmartWaste AI Smart City adalah aplikasi web Flask untuk memantau tempat sampah pintar, jadwal pengumpulan, notifikasi operasional, peta rute, laporan, dan analisis AI sederhana.

## Fitur

- Login email dan password dengan Flask Login.
- Password hash memakai `werkzeug.security`.
- Role `admin` dan `petugas`.
- Admin bisa mengakses semua halaman.
- Petugas hanya bisa membuka Dashboard, Monitoring Sampah, Tempat Sampah, Pengumpulan, Peta & Rute, Notifikasi, dan Logout.
- Halaman 403 untuk akses terlarang.
- Dashboard dengan statistik, chart, peta Leaflet, jadwal, dan notifikasi.
- CRUD tempat sampah untuk admin.
- Jadwal pengumpulan dan perubahan status.
- Analisis AI dengan upload gambar dan fallback prediksi.
- Laporan dengan filter, cetak, dan export CSV.
- CRUD pengguna untuk admin.

## Teknologi

- Python, Flask, Flask SQLAlchemy, Flask Login
- MySQL dan PyMySQL
- Bootstrap, Chart.js, Leaflet.js
- TensorFlow/Keras-ready, NumPy, Pillow, OpenCV

## Instalasi

Gunakan Python 3.10 atau Python 3.13.

- Python 3.10: bisa memakai dependency utama dan optional TensorFlow.
- Python 3.13: gunakan dependency utama. Analisis AI tetap berjalan memakai fallback karena TensorFlow versi lama tidak mendukung Python 3.13.

1. Masuk ke folder aplikasi:

```bash
cd C:\laragon\www\SmartWaste_AI
```

2. Install dependency:

```bash
pip install -r requirements.txt
```

Jika memakai Python 3.10 dan ingin memasang TensorFlow/Keras:

```bash
pip install -r requirements-ai-py310.txt
```

Jika hanya ingin library gambar tanpa TensorFlow:

```bash
pip install -r requirements-vision.txt
```

3. Buat database MySQL melalui phpMyAdmin atau terminal, lalu import:

```sql
database/smartwaste_ai.sql
```

Default koneksi database:

```text
mysql+pymysql://root:@localhost/smartwaste_ai
```

Jika konfigurasi MySQL berbeda, set environment variable `DATABASE_URL`.

## Menjalankan Aplikasi

```bash
python app.py
```

Buka:

```text
http://127.0.0.1:5000
```

## Akun Default

```text
Email: admin@smartwaste.com
Password: admin123
Role: admin
```

Contoh akun petugas dari SQL dummy:

```text
Email: petugas@smartwaste.com
Password: petugas123
Role: petugas
```

## Catatan AI

File `models/ai_model.h5` masih placeholder. Jika model Keras asli atau TensorFlow belum tersedia, aplikasi tetap berjalan memakai fallback prediksi berdasarkan nama file atau pilihan acak.
