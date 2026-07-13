from datetime import datetime

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from extensions import db
from models.database_model import JadwalPengumpulan, Notifikasi, TempatSampah
from routes.auth import role_required

pengumpulan_bp = Blueprint("pengumpulan", __name__)


@pengumpulan_bp.route("/pengumpulan", methods=["GET", "POST"])
@login_required
def pengumpulan():
    if request.method == "POST":
        schedule = JadwalPengumpulan(
            tempat_sampah_id=int(request.form["tempat_sampah_id"]),
            nama_petugas=request.form["nama_petugas"].strip(),
            tanggal=datetime.strptime(request.form["tanggal"], "%Y-%m-%d").date(),
            jam=datetime.strptime(request.form["jam"], "%H:%M").time(),
            status=request.form["status"],
        )
        db.session.add(schedule)
        db.session.add(
            Notifikasi(
                judul="Jadwal pengambilan berhasil",
                pesan=f"Jadwal untuk {schedule.nama_petugas} telah dibuat.",
                tipe="info",
            )
        )
        db.session.commit()
        flash("Jadwal pengumpulan berhasil ditambahkan.", "success")
        return redirect(url_for("pengumpulan.pengumpulan"))

    schedules = JadwalPengumpulan.query.order_by(
        JadwalPengumpulan.tanggal.desc(), JadwalPengumpulan.jam.desc()
    ).all()
    bins = TempatSampah.query.order_by(TempatSampah.kode_bin.asc()).all()
    return render_template("pengumpulan.html", schedules=schedules, bins=bins)


@pengumpulan_bp.route("/pengumpulan/<int:schedule_id>/status", methods=["POST"])
@login_required
def ubah_status_pengumpulan(schedule_id):
    schedule = JadwalPengumpulan.query.get_or_404(schedule_id)
    schedule.status = request.form["status"]
    db.session.commit()
    flash("Status pengumpulan berhasil diperbarui.", "success")
    return redirect(url_for("pengumpulan.pengumpulan"))


@pengumpulan_bp.route("/pengumpulan/<int:schedule_id>/hapus", methods=["POST"])
@login_required
def hapus_pengumpulan(schedule_id):
    if current_user.role != "admin":
        abort(403)

    schedule = JadwalPengumpulan.query.get_or_404(schedule_id)
    db.session.delete(schedule)
    db.session.commit()
    flash("Jadwal pengumpulan berhasil dihapus.", "info")
    return redirect(url_for("pengumpulan.pengumpulan"))
