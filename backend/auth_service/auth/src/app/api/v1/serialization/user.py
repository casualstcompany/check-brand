import re
from datetime import timedelta, datetime

from marshmallow import post_dump, validates_schema, validates, ValidationError
from sqlalchemy import func

from extension import ma
from config.utils import create_otp
from models import Profile


class UserImageMixin:
    image_url = ma.Hyperlinks(
        ma.URLFor("media.index", dict(image="<image>", _external=True)),
        dump_only=True,
    )


class UserProfileSchema(ma.SQLAlchemySchema, UserImageMixin):
    id = ma.String(dump_only=True)
    public_address = ma.String(dump_only=True)
    email = ma.String()
    email_verified = ma.Boolean(dump_only=True)

    class Meta:
        model = Profile
        fields = (
            "id",
            "public_address",
            "username",
            "email",
            "email_verified",
            "telegram",
            "whatsapp",
            "instagram",
            "image_url",
            "created",
        )
        load_instance = True

    @post_dump
    def dump_email_verified(self, data, **kwargs):
        if data.get("email_verified") is None:
            data["email_verified"] = False
        return data

    @validates("email")
    def validate_email(self, email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValidationError("Некорректный адрес электронной почты")

    @validates_schema
    def load_email(self, data, **kwargs):
        email = data.get("email")
        if email and isinstance(self.instance, Profile):
            email = email.lower()
            if (
                self.instance.email != email
                or self.instance.email_verified is None
            ):
                data["email_verified"] = None
                data["email_otp"] = create_otp()
                data["email_otp_exp"] = func.now() + timedelta(minutes=15)
        return data


class UserImageSchema(ma.SQLAlchemySchema, UserImageMixin):
    class Meta:
        model = Profile
        fields = ("image_url",)


class EmailConfirmProfileSchema(ma.SQLAlchemySchema, UserImageMixin):
    class Meta:
        model = Profile
        fields = (
            "email_verified",
            "email_otp",
        )
        load_instance = True

    @validates("email_otp")
    def validate_email_otp(self, email_otp):
        if email_otp != self.instance.email_otp:
            raise ValidationError("Некорректный код подтверждения")

        if self.instance.email_otp_exp < datetime.now():
            raise ValidationError("Срок кода подтверждения истек")

    @validates_schema
    def load_email_verified(self, data, **kwargs):
        email_verified = data.get("email_verified")
        if email_verified and isinstance(self.instance, Profile):
            data["email_otp"] = None
        return data


user_profile_schema = UserProfileSchema()
user_image_schema = UserImageSchema()

user_email_confirm = EmailConfirmProfileSchema()
