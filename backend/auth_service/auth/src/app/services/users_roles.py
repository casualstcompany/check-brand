from http import HTTPStatus

from api.v1.response_code import get_error_response as error_response
from config.config import config as settings
from config.utils import session_scope
from models import Profile, ResourceAccess, Role, RolesPermissions, RolesUsers
from psycopg2.errors import UniqueViolation
from schemes import BaseFilterModel, SortByUsersRolesEnum
from schemes.role import CreateRolesUsersSchema, UpdateRolesUsersSchema
from services.user import user_service
from sqlalchemy import func, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import aliased


class UsersRolesService:
    model: RolesUsers = RolesUsers

    def get_user_permissions_and_access(self, public_address):
        with session_scope() as session:
            access_account = aliased(ResourceAccess, name="access_account")
            access_collection = aliased(
                ResourceAccess, name="access_collection"
            )
            access_pack = aliased(ResourceAccess, name="access_pack")

            user_permissions_and_access = (
                session.query(
                    self.model.public_address,
                    func.jsonb_build_object(
                        "accounts",
                        func.array_agg(access_account.resource_id.distinct()),
                        "collections",
                        func.array_agg(
                            access_collection.sub_resource_id.distinct()
                        ),
                        "packs",
                        func.array_agg(
                            access_pack.sub_sub_resource_id.distinct()
                        ),
                    ).label("access"),
                    func.array_agg(
                        RolesPermissions.permission_name.distinct()
                    ).label("permissions"),
                )
                .outerjoin(
                    access_account,
                    (self.model.id == access_account.role_user_id)
                    & (
                        self.model.role_number.in_(
                            settings.ROLES_ACCESS.ACCOUNT
                        )
                    ),
                )
                .outerjoin(
                    access_collection,
                    (self.model.id == access_collection.role_user_id)
                    & (
                        self.model.role_number.in_(
                            settings.ROLES_ACCESS.COLLECTION
                        )
                    ),
                )
                .outerjoin(
                    access_pack,
                    (self.model.id == access_pack.role_user_id)
                    & (self.model.role_number.in_(settings.ROLES_ACCESS.PACK)),
                )
                .outerjoin(
                    RolesPermissions,
                    self.model.role_number == RolesPermissions.role_number,
                )
                .filter(self.model.public_address == public_address)
                .group_by(self.model.public_address)
                .first()
            )

            return user_permissions_and_access

    def _get_users_roles_by_role_number_and_public_address(
        self, role_number, public_address
    ):
        role = self.model.query.filter_by(
            role_number=role_number, public_address=public_address
        ).first()
        return role

    def _get_order_by(self, sort: SortByUsersRolesEnum):
        if sort == SortByUsersRolesEnum.desc_updated:
            order_by = self.model.updated.desc()
        elif sort == SortByUsersRolesEnum.asc_updated:
            order_by = self.model.updated.asc()
        elif sort == SortByUsersRolesEnum.desc_created:
            order_by = self.model.created.desc()
        else:
            order_by = self.model.created.asc()
        return order_by

    def _add_filters_order_by_pagination(
        self, query, query_params: BaseFilterModel
    ):
        if query_params.q:
            user_profile = aliased(Profile, name="user_profile")
            creator_profile = aliased(Profile, name="creator_profile")

            query = (
                query.outerjoin(
                    user_profile,
                    self.model.public_address == user_profile.public_address,
                )
                .outerjoin(
                    creator_profile,
                    self.model.creator == creator_profile.public_address,
                )
                .filter(
                    or_(
                        user_profile.username.ilike(f"%{query_params.q}%"),
                        creator_profile.username.ilike(f"%{query_params.q}%"),
                    )
                )
            )

        if query_params.role_names:
            query = query.outerjoin(self.model.role).filter(
                Role.name.in_(query_params.role_names)
            )

        if (
            query_params.account_ids
            or query_params.collection_ids
            or query_params.pack_ids
        ):
            query = query.outerjoin(self.model.access)

            if query_params.account_ids:
                query = query.filter(
                    ResourceAccess.resource_id.in_(query_params.account_ids)
                )

            if query_params.collection_ids:
                query = query.filter(
                    ResourceAccess.sub_resource_id.in_(
                        query_params.collection_ids
                    )
                )

            if query_params.pack_ids:
                query = query.filter(
                    ResourceAccess.sub_sub_resource_id.in_(
                        query_params.pack_ids
                    )
                )

        if query_params.wallets:
            query = query.filter(
                or_(
                    self.model.public_address.in_(query_params.wallets),
                    self.model.creator.in_(query_params.wallets),
                )
            )
        query = query.order_by(self._get_order_by(query_params.sort_by))

        return query

    def get_list_users_roles(self, query_params: BaseFilterModel):
        with session_scope() as session:
            query = session.query(self.model)
            query = self._add_filters_order_by_pagination(
                query=query, query_params=query_params
            )
            query = query.paginate(
                page=query_params.page,
                per_page=query_params.page_size,
                count=True,
                error_out=False,
            )
            return query

    @staticmethod
    def get_list_resource_access_by_roles_users_id_and_list_id(
        roles_users_id, list_id
    ):
        with session_scope() as session:
            list_remove_access = (
                session.query(ResourceAccess)
                .filter(
                    ResourceAccess.role_user_id == roles_users_id,
                    ResourceAccess.id.in_(list_id),
                )
                .all()
            )
            return list_remove_access

    def create_users_roles(self, body: CreateRolesUsersSchema, creator_wallet):
        """
        Создаёт Связь между ролью и пользователем
        ВАЖНО: для отмены дублирования поиска роли по её номеру,
        проверку существования роли вынес в декоратор(permissions)
        """

        if not user_service.get_by_public_address(
            public_address=body.public_address
        ):
            return error_response.fail(
                "User with this public_address not found",
                status_code=HTTPStatus.BAD_REQUEST,
            )

        if self._get_users_roles_by_role_number_and_public_address(
            role_number=body.role_number, public_address=body.public_address
        ):
            return error_response.fail(
                "The user already has a defined role",
                status_code=HTTPStatus.BAD_REQUEST,
            )

        try:
            with session_scope() as session:
                roles_users = self.model(
                    creator=creator_wallet, **body.dict(exclude={"access"})
                )

                for access in body.access:
                    new_access = ResourceAccess(**access.dict())
                    roles_users.access.append(new_access)

                session.add(roles_users)

                return roles_users
        except IntegrityError as e:
            assert isinstance(e.orig, UniqueViolation)
            return error_response.fail(
                "Access resources are not unique",
                status_code=HTTPStatus.BAD_REQUEST,
            )

    def update_users_roles(
        self, body: UpdateRolesUsersSchema, users_roles_id, creator_wallet
    ):
        try:
            with session_scope() as session:
                roles_users = (
                    session.query(self.model)
                    .filter(self.model.id == users_roles_id)
                    .first()
                )

                if not roles_users:
                    return error_response.fail(
                        "Role not found", status_code=HTTPStatus.BAD_REQUEST
                    )

                if body.description:
                    roles_users.description = body.description

                for access in body.access:
                    new_access = ResourceAccess(**access.dict())
                    roles_users.access.append(new_access)

                if body.remove_access:
                    list_remove_access = session.query(ResourceAccess).filter(
                        ResourceAccess.role_user_id == roles_users.id,
                        ResourceAccess.id.in_(body.remove_access),
                    )

                    for remove_access in list_remove_access:
                        roles_users.access.remove(remove_access)
                        session.delete(remove_access)

                roles_users.creator = creator_wallet

                return roles_users
        except IntegrityError as e:
            assert isinstance(e.orig, UniqueViolation)
            return error_response.fail(
                "Access resources are not unique",
                status_code=HTTPStatus.BAD_REQUEST,
            )

    def delete_users_roles(self, users_roles_id):
        with session_scope() as session:
            roles_users = (
                session.query(self.model)
                .filter(self.model.id == users_roles_id)
                .first()
            )

            if not roles_users:
                return error_response.fail(
                    "Role not found", status_code=HTTPStatus.BAD_REQUEST
                )
            session.delete(roles_users)

            return roles_users

    def get_users_roles(self, users_roles_id):
        with session_scope() as session:
            roles_users = (
                session.query(self.model)
                .filter(self.model.id == users_roles_id)
                .first()
            )

            if not roles_users:
                return error_response.fail(
                    "Role not found", status_code=HTTPStatus.BAD_REQUEST
                )

            return roles_users


users_roles_service = UsersRolesService()
