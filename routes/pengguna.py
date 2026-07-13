from flask import Blueprint, flash, redirect, render_template, request, url_for
from werkzeug.security import generate_password_hash

from extensions import db
from models.database_model import User
from routes.auth import role_required

pengguna_bp = Blueprint("pengguna", __name__)


@pengguna_bp.route("/pengguna", methods=["GET", "POST"])
@role_required("admin")
def pengguna():
    if request.method == "POST":
        password = request.form.get("password", "")
        if not password:
            flash("Password pengguna wajib diisi.", "danger")
            return redirect(url_for("pengguna.pengguna"))

        user = User(
            nama=request.form["nama"].strip(),
            email=request.form["email"].strip().lower(),
            password=generate_password_hash(password),
            role=request.form["role"],
        )
        db.session.add(user)
        db.session.commit()
        flash("Pengguna berhasil ditambahkan.", "success")
        return redirect(url_for("pengguna.pengguna"))

    users = User.query.order_by(User.created_at.desc()).all()
    return render_template("pengguna.html", users=users)


@pengguna_bp.route("/pengguna/<int:user_id>/hapus", methods=["POST"])
@role_required("admin")
def hapus_pengguna(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("Pengguna berhasil dihapus.", "info")
    return redirect(url_for("pengguna.pengguna"))
