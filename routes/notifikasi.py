from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required

from extensions import db
from models.database_model import Notifikasi

notifikasi_bp = Blueprint("notifikasi", __name__)


@notifikasi_bp.route("/notifikasi")
@login_required
def notifikasi():
    notifications = Notifikasi.query.order_by(Notifikasi.created_at.desc()).all()
    return render_template("notifikasi.html", notifications=notifications)


@notifikasi_bp.route("/notifikasi/<int:notification_id>/baca", methods=["POST"])
@login_required
def tandai_dibaca(notification_id):
    notification = Notifikasi.query.get_or_404(notification_id)
    notification.sudah_dibaca = True
    db.session.commit()
    flash("Notifikasi ditandai sudah dibaca.", "success")
    return redirect(url_for("notifikasi.notifikasi"))
