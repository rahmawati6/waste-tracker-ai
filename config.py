import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "smartwaste-ai-secret-key-2026")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "mysql+pymysql://root:@localhost/smartwaste_ai",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "static", "uploads")
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024
