from datetime import datetime

from flask_login import UserMixin

from extensions import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True, index=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="petugas")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class TempatSampah(db.Model):
    __tablename__ = "tempat_sampah"

    id = db.Column(db.Integer, primary_key=True)
    kode_bin = db.Column(db.String(30), nullable=False, unique=True)
    nama_lokasi = db.Column(db.String(150), nullable=False)
    alamat = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    kapasitas = db.Column(db.Float, nullable=False, default=120)
    status = db.Column(db.String(30), nullable=False, default="kosong")
    persentase_isi = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    sensor_data = db.relationship(
        "SensorData",
        backref="tempat_sampah",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    @property
    def latest_sensor(self):
        return self.sensor_data.order_by(SensorData.waktu.desc()).first()


class SensorData(db.Model):
    __tablename__ = "sensor_data"

    id = db.Column(db.Integer, primary_key=True)
    tempat_sampah_id = db.Column(
        db.Integer,
        db.ForeignKey("tempat_sampah.id"),
        nullable=False,
    )
    berat_sampah = db.Column(db.Float, nullable=False, default=0)
    suhu = db.Column(db.Float, nullable=False, default=28)
    kelembaban = db.Column(db.Float, nullable=False, default=70)
    waktu = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class JadwalPengumpulan(db.Model):
    __tablename__ = "jadwal_pengumpulan"

    id = db.Column(db.Integer, primary_key=True)
    tempat_sampah_id = db.Column(db.Integer, db.ForeignKey("tempat_sampah.id"), nullable=False)
    nama_petugas = db.Column(db.String(120), nullable=False)
    tanggal = db.Column(db.Date, nullable=False)
    jam = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(30), nullable=False, default="terjadwal")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    tempat_sampah = db.relationship("TempatSampah", backref="jadwal_pengumpulan")


class HasilAI(db.Model):
    __tablename__ = "hasil_ai"

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    prediksi = db.Column(db.String(30), nullable=False)
    akurasi = db.Column(db.Float, nullable=False)
    rekomendasi = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class Notifikasi(db.Model):
    __tablename__ = "notifikasi"

    id = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.String(150), nullable=False)
    pesan = db.Column(db.String(255), nullable=False)
    tipe = db.Column(db.String(30), nullable=False, default="info")
    sudah_dibaca = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class Laporan(db.Model):
    __tablename__ = "laporan"

    id = db.Column(db.Integer, primary_key=True)
    tanggal = db.Column(db.Date, nullable=False)
    total_sampah = db.Column(db.Float, nullable=False, default=0)
    jumlah_pengambilan = db.Column(db.Integer, nullable=False, default=0)
    keterangan = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
