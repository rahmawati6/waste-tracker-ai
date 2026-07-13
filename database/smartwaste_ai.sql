CREATE DATABASE IF NOT EXISTS smartwaste_ai
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE smartwaste_ai;

DROP TABLE IF EXISTS laporan;
DROP TABLE IF EXISTS notifikasi;
DROP TABLE IF EXISTS hasil_ai;
DROP TABLE IF EXISTS jadwal_pengumpulan;
DROP TABLE IF EXISTS sensor_data;
DROP TABLE IF EXISTS tempat_sampah;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nama VARCHAR(120) NOT NULL,
  email VARCHAR(150) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  role VARCHAR(20) NOT NULL DEFAULT 'petugas',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tempat_sampah (
  id INT AUTO_INCREMENT PRIMARY KEY,
  kode_bin VARCHAR(30) NOT NULL UNIQUE,
  nama_lokasi VARCHAR(150) NOT NULL,
  alamat VARCHAR(255) NOT NULL,
  latitude DOUBLE NOT NULL,
  longitude DOUBLE NOT NULL,
  kapasitas DOUBLE NOT NULL DEFAULT 120,
  status VARCHAR(30) NOT NULL DEFAULT 'kosong',
  persentase_isi INT NOT NULL DEFAULT 0,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sensor_data (
  id INT AUTO_INCREMENT PRIMARY KEY,
  tempat_sampah_id INT NOT NULL,
  berat_sampah DOUBLE NOT NULL DEFAULT 0,
  suhu DOUBLE NOT NULL DEFAULT 28,
  kelembaban DOUBLE NOT NULL DEFAULT 70,
  waktu DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_sensor_tempat_sampah
    FOREIGN KEY (tempat_sampah_id) REFERENCES tempat_sampah(id)
    ON DELETE CASCADE
);

CREATE TABLE jadwal_pengumpulan (
  id INT AUTO_INCREMENT PRIMARY KEY,
  tempat_sampah_id INT NOT NULL,
  nama_petugas VARCHAR(120) NOT NULL,
  tanggal DATE NOT NULL,
  jam TIME NOT NULL,
  status VARCHAR(30) NOT NULL DEFAULT 'terjadwal',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_jadwal_tempat_sampah
    FOREIGN KEY (tempat_sampah_id) REFERENCES tempat_sampah(id)
    ON DELETE CASCADE
);

CREATE TABLE hasil_ai (
  id INT AUTO_INCREMENT PRIMARY KEY,
  filename VARCHAR(255) NOT NULL,
  prediksi VARCHAR(30) NOT NULL,
  akurasi DOUBLE NOT NULL,
  rekomendasi VARCHAR(255) NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE notifikasi (
  id INT AUTO_INCREMENT PRIMARY KEY,
  judul VARCHAR(150) NOT NULL,
  pesan VARCHAR(255) NOT NULL,
  tipe VARCHAR(30) NOT NULL DEFAULT 'info',
  sudah_dibaca BOOLEAN NOT NULL DEFAULT FALSE,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE laporan (
  id INT AUTO_INCREMENT PRIMARY KEY,
  tanggal DATE NOT NULL,
  total_sampah DOUBLE NOT NULL DEFAULT 0,
  jumlah_pengambilan INT NOT NULL DEFAULT 0,
  keterangan VARCHAR(255) NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (nama, email, password, role, created_at) VALUES
('Administrator SmartWaste', 'admin@smartwaste.com', 'pbkdf2:sha256:260000$smartwaste2026$8eabc47ed5d61433d10eea390b922e94931bc80befb16590e650537c7503f529', 'admin', NOW()),
('Petugas Lapangan', 'petugas@smartwaste.com', 'pbkdf2:sha256:260000$smartwastepetugas$ad6367eb6bd17b8cc8aaa665253c08c75c1283c48f310c6ab4d385c41ec98d06', 'petugas', NOW());

INSERT INTO tempat_sampah (kode_bin, nama_lokasi, alamat, latitude, longitude, kapasitas, status, persentase_isi) VALUES
('BIN-001', 'Balai Kota', 'Jl. Medan Merdeka Selatan, Jakarta Pusat', -6.180511, 106.828383, 150, 'sedang', 48),
('BIN-002', 'Taman Menteng', 'Jl. HOS Cokroaminoto, Jakarta Pusat', -6.196006, 106.829144, 120, 'hampir penuh', 82),
('BIN-003', 'Stasiun MRT Dukuh Atas', 'Jl. Tanjung Karang, Jakarta Pusat', -6.200603, 106.822276, 180, 'penuh', 96),
('BIN-004', 'Kawasan Kota Tua', 'Jl. Kali Besar Timur, Jakarta Barat', -6.135200, 106.813301, 130, 'kosong', 18),
('BIN-005', 'Pasar Santa', 'Jl. Cipaku I, Jakarta Selatan', -6.242436, 106.801940, 140, 'sedang', 61);

INSERT INTO sensor_data (tempat_sampah_id, berat_sampah, suhu, kelembaban, waktu) VALUES
(1, 46.5, 29.4, 72, NOW()),
(2, 93.2, 31.1, 68, NOW()),
(3, 145.8, 32.5, 75, NOW()),
(4, 19.4, 28.2, 70, NOW()),
(5, 70.6, 30.0, 66, NOW());

INSERT INTO jadwal_pengumpulan (tempat_sampah_id, nama_petugas, tanggal, jam, status) VALUES
(3, 'Petugas Lapangan', CURDATE(), '13:30:00', 'diproses'),
(2, 'Rina Operasional', DATE_ADD(CURDATE(), INTERVAL 1 DAY), '09:00:00', 'terjadwal'),
(5, 'Budi Armada', DATE_ADD(CURDATE(), INTERVAL 2 DAY), '10:15:00', 'terjadwal');

INSERT INTO hasil_ai (filename, prediksi, akurasi, rekomendasi, created_at) VALUES
('sample_penuh.jpg', 'penuh', 92, 'Prioritas pengangkutan', NOW()),
('sample_sedang.jpg', 'sedang', 86, 'Pantau secara berkala', NOW());

INSERT INTO notifikasi (judul, pesan, tipe, sudah_dibaca, created_at) VALUES
('Tempat sampah penuh', 'BIN-003 membutuhkan pengangkutan prioritas.', 'darurat', FALSE, NOW()),
('Tempat sampah hampir penuh', 'BIN-002 mencapai kapasitas 82%.', 'peringatan', FALSE, NOW()),
('Jadwal pengambilan berhasil', 'Jadwal BIN-002 untuk besok sudah dibuat.', 'info', TRUE, NOW()),
('Prediksi AI selesai', 'sample_penuh.jpg diprediksi penuh.', 'info', TRUE, NOW());

INSERT INTO laporan (tanggal, total_sampah, jumlah_pengambilan, keterangan) VALUES
(CURDATE(), 376.4, 3, 'Operasional berjalan normal dengan satu prioritas penuh.'),
(DATE_SUB(CURDATE(), INTERVAL 1 DAY), 341.2, 4, 'Area pusat kota selesai dikumpulkan.'),
(DATE_SUB(CURDATE(), INTERVAL 2 DAY), 298.6, 3, 'Kepadatan sampah sedang.');
