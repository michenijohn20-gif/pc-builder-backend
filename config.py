import os
from datetime import timedelta


BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key-keep-it-secret")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(BASEDIR, 'instance', 'snoober.db')}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get(
        "JWT_SECRET_KEY",
        "jwt-super-secret-key-for-pc-builder-api",
    )
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)
