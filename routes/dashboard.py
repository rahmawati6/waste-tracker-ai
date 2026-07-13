from datetime import date

from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user, login_required
from sqlalchemy import func

from extensions import db
from models.database_model import JadwalPengumpulan, Notifikasi, SensorData, TempatSampah
from routes.auth import role_required

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard"))
    return redirect(url_for("auth.login"))


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    bins = TempatSampah.query.order_by(TempatSampah.kode_bin.asc()).all()
    total_bins = TempatSampah.query.count()
    avg_fill = db.session.query(func.avg(TempatSampah.persentase_isi)).scalar() or 0
    today_waste = (
        db.session.query(func.sum(SensorData.berat_sampah))
        .filter(func.date(SensorData.waktu) == date.today())
        .scalar()
        or 0
    )
    warnings = TempatSampah.query.filter(TempatSampah.status.in_(["hampir penuh", "penuh"])).count()
    status_counts = dict(
        db.session.query(TempatSampah.status, func.count(TempatSampah.id))
        .group_by(TempatSampah.status)
        .all()
    )
    next_schedules = (
        JadwalPengumpulan.query.order_by(JadwalPengumpulan.tanggal.asc(), JadwalPengumpulan.jam.asc())
        .limit(5)
        .all()
    )
    notifications = Notifikasi.query.order_by(Notifikasi.created_at.desc()).limit(5).all()
    pins = [
        {
            "kode_bin": item.kode_bin,
            "nama_lokasi": item.nama_lokasi,
            "alamat": item.alamat,
            "latitude": item.latitude,
            "longitude": item.longitude,
            "status": item.status,
            "persentase_isi": item.persentase_isi,
        }
        for item in bins
    ]
    chart_series = [
        {"tanggal": "Sen", "total": 112},
        {"tanggal": "Sel", "total": 128},
        {"tanggal": "Rab", "total": 96},
        {"tanggal": "Kam", "total": 151},
        {"tanggal": "Jum", "total": 138},
        {"tanggal": "Sab", "total": 109},
        {"tanggal": "Min", "total": 121},
    ]

    return render_template(
        "dashboard.html",
        bins=bins,
        pins=pins,
        total_bins=total_bins,
        avg_fill=round(avg_fill, 1),
        today_waste=round(today_waste, 1),
        warnings=warnings,
        status_counts=status_counts,
        next_schedules=next_schedules,
        notifications=notifications,
        chart_series=chart_series,
    )


@dashboard_bp.route("/monitoring")
@login_required
def monitoring():
    bins = TempatSampah.query.order_by(TempatSampah.persentase_isi.desc()).all()
    return render_template("monitoring.html", bins=bins)


@dashboard_bp.route("/peta-rute")
@login_required
def peta_rute():
    bins = TempatSampah.query.order_by(TempatSampah.kode_bin.asc()).all()
    pins = [
        {
            "kode_bin": item.kode_bin,
            "nama_lokasi": item.nama_lokasi,
            "alamat": item.alamat,
            "latitude": item.latitude,
            "longitude": item.longitude,
            "status": item.status,
            "persentase_isi": item.persentase_isi,
        }
        for item in bins
    ]
    return render_template("peta_rute.html", bins=pins)


@dashboard_bp.route("/pengaturan")
@role_required("admin")
def pengaturan():
    return render_template("pengaturan.html")
