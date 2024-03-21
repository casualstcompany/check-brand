from contextlib import contextmanager
from random import randint

from extension import db, ma
from flask import Flask
from flask_migrate import Migrate

from .config import config


def init_db(app: Flask):
    """TODO: не понятно какого рака это делает в utils? Перенести!"""
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"postgresql://{config.POSTGRES.USER}:{config.POSTGRES.PASSWORD}@{config.POSTGRES.HOST}:{config.POSTGRES.PORT}/{config.POSTGRES.NAME}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # app.config['SQLALCHEMY_ECHO'] = True
    db.init_app(app)
    Migrate(app, db)


@contextmanager
def session_scope():
    try:
        yield db.session
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise


def init_ma(app: Flask):
    ma.init_app(app)


def create_nonce() -> int:
    return randint(10000, 100000)

def create_otp() -> int:
    return randint(100000, 999999)