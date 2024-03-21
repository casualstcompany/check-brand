import uuid

from extension import db
from flask_security import RoleMixin
from models.base import DateTimeMixin
from schemes import RoleEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.inspection import inspect


class Role(db.Model, RoleMixin):
    __tablename__ = "roles"
    __table_args__ = {"schema": "content"}

    name = db.Column(
        db.Enum(RoleEnum, native_enum=False),
        unique=True,
        nullable=False,
        primary_key=True,
    )
    public_name = db.Column(db.String(50), unique=True, nullable=False)
    number = db.Column(db.Integer(), unique=True, nullable=True)
    permission = db.relationship(
        "Permission",
        secondary="content.roles_permissions",
        backref=db.backref("roles", lazy="dynamic"),
    )

    def serialize(self):
        role = {c: getattr(self, c) for c in inspect(self).attrs.keys()}
        del role["users"]
        return role


class RolesUsers(db.Model, DateTimeMixin):
    __tablename__ = "roles_users"
    __table_args__ = (
        db.UniqueConstraint(
            "public_address", "role_number", name="role_user_inx"
        ),
        {"schema": "content"},
    )

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    public_address = db.Column(
        "public_address",
        db.Text,
        db.ForeignKey("content.users.public_address"),
    )
    user_profile = db.relationship(
        "Profile",
        primaryjoin="and_(Profile.public_address==RolesUsers.public_address)",
        innerjoin=False,
        foreign_keys=[public_address],
        lazy="joined",
    )
    role_number = db.Column(
        "role_number", db.Integer(), db.ForeignKey("content.roles.number")
    )
    role = db.relationship("Role", innerjoin=False, lazy="joined")
    description = db.Column(db.Text, nullable=True)
    access = db.relationship(
        "ResourceAccess",
        innerjoin=False,
        lazy="joined",
        cascade="all, delete",
        passive_deletes=True,
    )
    creator = db.Column("creator", db.Text, nullable=True)
    creator_profile = db.relationship(
        "Profile",
        primaryjoin="and_(Profile.public_address==RolesUsers.creator)",
        innerjoin=False,
        foreign_keys=[creator],
        lazy="joined",
    )


class RolesPermissions(db.Model):
    __tablename__ = "roles_permissions"
    __table_args__ = (
        db.UniqueConstraint(
            "permission_name", "role_number", name="role_permission_inx"
        ),
        {"schema": "content"},
    )

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role_number = db.Column(
        "role_number", db.Integer(), db.ForeignKey("content.roles.number")
    )
    permission_name = db.Column(
        "permission_name",
        db.String(50),
        db.ForeignKey("content.permissions.name"),
    )


class Permission(db.Model):
    __tablename__ = "permissions"
    __table_args__ = {"schema": "content"}
    name = db.Column(
        db.String(50), primary_key=True, unique=True, nullable=False
    )

    def __repr__(self):
        return f"Permission >>> {self.permission}"


class ResourceAccess(db.Model, DateTimeMixin):
    __tablename__ = "resource_access"
    __table_args__ = (
        db.UniqueConstraint(
            "resource_id",
            "sub_resource_id",
            "sub_sub_resource_id",
            "role_user_id",
            name="role_user_resource_inx",
        ),
        {"schema": "content"},
    )

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role_user_id = db.Column(
        "role_user_id",
        UUID(as_uuid=True),
        db.ForeignKey("content.roles_users.id"),
    )
    resource_id = db.Column("resource_id", UUID(as_uuid=True))
    sub_resource_id = db.Column("sub_resource_id", UUID(as_uuid=True))
    sub_sub_resource_id = db.Column("sub_sub_resource_id", UUID(as_uuid=True))
