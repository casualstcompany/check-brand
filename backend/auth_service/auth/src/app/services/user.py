import os
from typing import Optional

from components.datastore import datastore
from config.config import config
from config.utils import session_scope
from extension import db
from flask_jwt_extended import get_jwt_identity
from models import Profile, User
from schemes import RoleEnum
from utils import generate


class UserService:
    model_profile = Profile

    def __init__(self):
        return

    def create_user_and_profile(self, public_address: str):
        public_address = public_address.lower()
        with session_scope():
            new_user = datastore.create_user(public_address=public_address)
            datastore.add_role_to_user(new_user, RoleEnum.user.value)
            self._create_profile(public_address)

        return new_user

    def add_image(self, image):
        public_address = get_jwt_identity()
        profile = self.get_profile_by_public_address(public_address)

        extension = image.filename.rsplit(".", 1)[1].lower()
        filename = generate.random_name(5) + "." + extension

        while self.get_profile_by_image(image=filename):
            filename = generate.random_name(5) + "." + extension
        image.save(os.path.join(config.UPLOAD.FOLDER, filename))

        with session_scope():
            profile.image = filename

        return profile

    def get_profile_by_username(self, username):
        profile = self.model_profile.query.filter_by(username=username).first()
        return profile

    def get_profile_by_public_address(self, public_address):
        public_address = public_address.lower()
        profile = self.model_profile.query.filter_by(
            public_address=public_address
        ).first()
        return profile

    def get_profile_by_image(self, image):
        profile = self.model_profile.query.filter_by(image=image).first()
        return profile

    def _create_profile(self, public_address: str):
        username = "qsaefr2q"
        while self.get_profile_by_username(username):
            username = generate.random_name(8).lower()

        profile = self.model_profile(
            public_address=public_address, username=username
        )
        db.session.add(profile)

    @staticmethod
    def get_by_public_address(public_address: str) -> Optional[User]:
        public_address = public_address.lower()
        return datastore.find_user(public_address=public_address)


user_service = UserService()
