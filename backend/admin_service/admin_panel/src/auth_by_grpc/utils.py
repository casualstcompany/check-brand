from auth_by_grpc.constants import ADMIN_ROLES


def validate_is_admin(user):
    admin_allowed_roles = ADMIN_ROLES
    for allowed_role in admin_allowed_roles:
        if user and allowed_role in user.user_role:
            return True
    return False
