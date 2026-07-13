from functools import wraps

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash

from models.database_model import User

auth_bp = Blueprint("auth", __name__)


def role_required(*roles):
    def decorator(view):
        @wraps(view)
        @login_required
        def wrapped_view(*args, **kwargs):
            if current_user.role not in roles:
                abort(403)
            return view(*args, **kwargs)

        return wrapped_view

    return decorator


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not email:
            flash("Email wajib diisi.", "danger")
            return render_template("login.html", email=email)
        if not password:
            flash("Password wajib diisi.", "danger")
            return render_template("login.html", email=email)

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash("Email atau password salah", "danger")
            return render_template("login.html", email=email)

        login_user(user)
        flash("Login berhasil. Selamat datang di SmartWaste AI.", "success")
        return redirect(url_for("dashboard.dashboard"))

    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Anda berhasil logout.", "info")
    return redirect(url_for("auth.login"))
