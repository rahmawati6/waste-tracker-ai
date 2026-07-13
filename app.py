from flask import Flask, redirect, render_template, url_for
from flask_login import current_user
from werkzeug.security import generate_password_hash

from config import Config
from extensions import db, login_manager
login_manager.login_view = "auth.login"
login_manager.login_message = "Silakan login terlebih dahulu."
login_manager.login_message_category = "warning"


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    from models.database_model import User
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.sampah import sampah_bp
    from routes.pengumpulan import pengumpulan_bp
    from routes.ai import ai_bp
    from routes.laporan import laporan_bp
    from routes.notifikasi import notifikasi_bp
    from routes.pengguna import pengguna_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(sampah_bp)
    app.register_blueprint(pengumpulan_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(laporan_bp)
    app.register_blueprint(notifikasi_bp)
    app.register_blueprint(pengguna_bp)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.context_processor
    def inject_layout_helpers():
        def is_admin():
            return current_user.is_authenticated and current_user.role == "admin"

        latest_notifications = []
        unread_notifications = 0
        if current_user.is_authenticated:
            try:
                from models.database_model import Notifikasi

                latest_notifications = (
                    Notifikasi.query.order_by(Notifikasi.created_at.desc()).limit(5).all()
                )
                unread_notifications = Notifikasi.query.filter_by(sudah_dibaca=False).count()
            except Exception:
                latest_notifications = []
                unread_notifications = 0

        return {
            "is_admin": is_admin,
            "latest_notifications": latest_notifications,
            "unread_notifications": unread_notifications,
        }

    @app.errorhandler(403)
    def forbidden(_error):
        return render_template("403.html"), 403

    @app.errorhandler(404)
    def not_found(_error):
        if current_user.is_authenticated:
            return render_template("404.html"), 404
        return redirect(url_for("auth.login"))

    @app.errorhandler(500)
    def server_error(_error):
        return render_template("500.html"), 500

    with app.app_context():
        try:
            db.create_all()
            seed_default_admin()
        except Exception as exc:
            app.logger.warning("Database belum siap: %s", exc)

    return app


def seed_default_admin():
    from models.database_model import User

    admin_email = "admin@smartwaste.com"
    existing_admin = User.query.filter_by(email=admin_email).first()
    if existing_admin:
        return

    admin = User(
        nama="Administrator SmartWaste",
        email=admin_email,
        password=generate_password_hash("admin123"),
        role="admin",
    )
    db.session.add(admin)
    db.session.commit()


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
