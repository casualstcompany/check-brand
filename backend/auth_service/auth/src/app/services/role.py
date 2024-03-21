from http import HTTPStatus

from api.v1.response_code import get_error_response as error_response
from components.datastore import datastore
from config.utils import session_scope
from models import Role
from services.user import user_service


class RoleService:
    def __init__(self):
        self.model = Role

    def get_role_by_name(self, role_name: str):
        role = self.model.query.filter_by(name=role_name).first()
        return role

    def get_role_by_number(self, role_number: int):
        role = self.model.query.filter_by(number=role_number).first()
        return role

    def _get_role_by_name_or_bad_request(self, role_name: str):
        role = self.get_role_by_name(role_name)
        if not role:
            return error_response.fail(
                "Role with this name not found",
                status_code=HTTPStatus.BAD_REQUEST,
            )
        return role

    @staticmethod
    def _get_user_by_public_address_or_bad_request(public_address: str):
        user = user_service.get_by_public_address(
            public_address=public_address
        )
        if not user:
            return error_response.fail(
                "User with this public_address not found",
                status_code=HTTPStatus.BAD_REQUEST,
            )
        return user

    def add_role_to_user(self, public_address: str, role_name: str):
        public_address = public_address.lower()
        user = self._get_user_by_public_address_or_bad_request(
            public_address=public_address
        )
        role = self._get_role_by_name_or_bad_request(role_name=role_name)

        if user.has_role(role):
            return error_response.fail(
                "User already has this role",
                status_code=HTTPStatus.BAD_REQUEST,
            )

        with session_scope():
            datastore.add_role_to_user(user, role)


role_service: RoleService = RoleService()
