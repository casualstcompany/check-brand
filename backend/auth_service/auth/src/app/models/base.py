from extension import db
from sqlalchemy import func


class DateTimeMixin:
    created = db.Column(db.DateTime, default=func.now())
    updated = db.Column(db.DateTime, default=func.now(), onupdate=func.now())
