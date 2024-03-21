import uuid

from config.utils import create_nonce
from extension import db
from flask_security import UserMixin
from models.base import DateTimeMixin
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID


class User(db.Model, UserMixin, DateTimeMixin):
    __tablename__ = "users"
    __table_args__ = {"schema": "content"}

    public_address = db.Column(db.String, primary_key=True, unique=True)
    nonce = db.Column(db.String(64), nullable=False, default=create_nonce)
    fs_uniquifier = db.Column(db.Text, nullable=True)
    active = db.Column(db.Boolean, nullable=False, default=True)
    roles = db.relationship(
        "Role",
        secondary="content.roles_users",
        backref=db.backref("users", lazy="dynamic"),
        overlaps="role",
    )  # TODO: как переделаю подтверждение прав, это поле можно убрать от сюда
    profile = db.relationship("Profile", back_populates="user", innerjoin=True)


class Profile(db.Model, DateTimeMixin):
    __tablename__ = "profiles"
    __table_args__ = (
        db.UniqueConstraint(
            "email", "email_verified", name="profile_email_uniq"
        ),
        {"schema": "content"},
    )

    id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    public_address = db.Column(
        db.Text, db.ForeignKey("content.users.public_address"), unique=True
    )
    username = db.Column(db.String, unique=True, nullable=False)
    phone = db.Column(db.Integer, nullable=True)
    image = db.Column(db.String(), unique=True, nullable=True)
    user = db.relationship("User", back_populates="profile", innerjoin=True)

    email = db.Column(db.String(), nullable=True)
    email_verified = db.Column(db.Boolean, nullable=True)
    telegram = db.Column(db.String())
    whatsapp = db.Column(db.String(), nullable=True)
    instagram = db.Column(db.String(), nullable=True)

    email_otp = db.Column(db.Integer, nullable=True)
    email_otp_exp = db.Column(db.DateTime, default=func.now())


class AuthToken(db.Model):
    __tablename__ = "auth_token"
    __table_args__ = {"schema": "content"}

    id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    public_address = db.Column(
        db.Text, db.ForeignKey("content.users.public_address")
    )
    user_agent = db.Column(db.Text, nullable=False)
    refresh_token = db.Column(db.Text, nullable=False)


# TODO: создать партицированные таблицы
class LoginHistory(db.Model):
    __tablename__ = "login_history"
    __table_args__ = (
        db.PrimaryKeyConstraint("public_address", "datetime"),
        {
            "schema": "content",
            "postgresql_partition_by": "RANGE (datetime)",
        },
    )

    public_address = db.Column(
        db.Text, db.ForeignKey("content.users.public_address")
    )
    datetime = db.Column(db.DateTime, default=func.now())
    user_agent = db.Column(db.Text, nullable=False)
