from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from extensions import db
from models.database_model import TempatSampah
from routes.auth import role_required

sampah_bp = Blueprint("sampah", __name__)


@sampah_bp.route("/tempat-sampah", methods=["GET", "POST"])
@login_required
def tempat_sampah():
    if request.method == "POST":
        if current_user.role != "admin":
            abort(403)

        item = TempatSampah(
            kode_bin=request.form["kode_bin"].strip().upper(),
            nama_lokasi=request.form["nama_lokasi"].strip(),
            alamat=request.form["alamat"].strip(),
            latitude=float(request.form["latitude"]),
            longitude=float(request.form["longitude"]),
            kapasitas=float(request.form["kapasitas"]),
            status=request.form["status"],
            persentase_isi=int(request.form["persentase_isi"]),
        )
        db.session.add(item)
        db.session.commit()
        flash("Data tempat sampah berhasil ditambahkan.", "success")
        return redirect(url_for("sampah.tempat_sampah"))

    bins = TempatSampah.query.order_by(TempatSampah.kode_bin.asc()).all()
    return render_template("tempat_sampah.html", bins=bins, item=None)


@sampah_bp.route("/tempat-sampah/<int:item_id>/edit", methods=["GET", "POST"])
@role_required("admin")
def edit_tempat_sampah(item_id):
    item = TempatSampah.query.get_or_404(item_id)
    if request.method == "POST":
        item.kode_bin = request.form["kode_bin"].strip().upper()
        item.nama_lokasi = request.form["nama_lokasi"].strip()
        item.alamat = request.form["alamat"].strip()
        item.latitude = float(request.form["latitude"])
        item.longitude = float(request.form["longitude"])
        item.kapasitas = float(request.form["kapasitas"])
        item.status = request.form["status"]
        item.persentase_isi = int(request.form["persentase_isi"])
        db.session.commit()
        flash("Data tempat sampah berhasil diperbarui.", "success")
        return redirect(url_for("sampah.tempat_sampah"))

    bins = TempatSampah.query.order_by(TempatSampah.kode_bin.asc()).all()
    return render_template("tempat_sampah.html", bins=bins, item=item)


@sampah_bp.route("/tempat-sampah/<int:item_id>/hapus", methods=["POST"])
@role_required("admin")
def hapus_tempat_sampah(item_id):
    item = TempatSampah.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash("Data tempat sampah berhasil dihapus.", "info")
    return redirect(url_for("sampah.tempat_sampah"))
