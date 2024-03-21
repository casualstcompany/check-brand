import logging

from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions

from auth_by_grpc import message as msg
from auth_by_grpc.constants import ALL_ROLES, ADMIN_ROLES

logger = logging.getLogger(__name__)

ALLOWED_METHODS = ("GET", "POST", "PUT", "PATCH", "DELETE")


class OnlyAdminGRPCPermission(permissions.BasePermission):
    """Only admin or super admin"""

    message = msg.ERROR_403_NO_ENOUGH_RIGHTS
    admin_allowed_roles = ADMIN_ROLES

    def admin_has_permission(self, request):
        for allowed_role in self.admin_allowed_roles:
            if request.user and allowed_role in request.user.user_role:
                return True
        return False

    def has_permission(self, request, view):
        if request.method in ALLOWED_METHODS:
            logger.debug("%s has permission", request.user)
            if request.user == AnonymousUser():
                return False
            if self.admin_has_permission(request):
                return True
        return False


class RoleCheckGRPCPermissionMixin:
    all_roles = ALL_ROLES

    def any_authorized_has_permission(self, request):
        for allowed_role in self.all_roles:
            logger.debug("allowed_role: %s" % allowed_role)
            if request.user and allowed_role in request.user.user_role:
                logger.debug("return True")
                return True
        return False


class AdminOrUserGetGRPCPermission(OnlyAdminGRPCPermission):
    """
    POST, PUT, PATCH, DELETE - Admin, superadmin has permission
    GET - all users
    """

    http_method = "GET"

    def has_permission(self, request, view):
        logger.debug("%s has permission", request.user)

        if request.method in ALLOWED_METHODS:
            if request.method == self.http_method:
                logger.debug("method GET")
                return True
            else:
                if request.user == AnonymousUser():
                    return False
                if self.admin_has_permission(request):
                    return True
            return False


class OnlyAuthorizedUserGRPCPermission(
    OnlyAdminGRPCPermission, RoleCheckGRPCPermissionMixin
):
    """
    POST, PUT, PATCH, DELETE, GET - any authorized has permission
    """

    def has_permission(self, request, view):
        logger.debug("%s has permission", request.user)

        if request.method in ALLOWED_METHODS:
            if request.user == AnonymousUser():
                return False
            if self.any_authorized_has_permission(request):
                return True
        return False


class OwnerOrAdminGRPCPermission(permissions.IsAuthenticated):
    admin_allowed_roles = ADMIN_ROLES

    def admin_has_permission(self, request):
        for allowed_role in self.admin_allowed_roles:
            if request.user and allowed_role in request.user.user_role:
                return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user == AnonymousUser():
            return False
        if request.user.user_wallet == obj.owner:
            return True
        return self.admin_has_permission(request)
