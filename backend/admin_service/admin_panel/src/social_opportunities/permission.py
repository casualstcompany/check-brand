import logging

from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions

from auth_by_grpc.constants import ADMIN_ROLES

logger = logging.getLogger(__name__)


class OwnerCompanyOrAdminGRPCPermission(permissions.IsAuthenticated):
    admin_allowed_roles = ADMIN_ROLES

    def admin_has_permission(self, request):
        for allowed_role in self.admin_allowed_roles:
            if request.user and allowed_role in request.user.user_role:
                return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user == AnonymousUser():
            return False
        if request.user.user_wallet == obj.company.owner:
            return True
        return self.admin_has_permission(request)


class OwnerCompanyServiceOrAdminGRPCPermission(permissions.IsAuthenticated):
    admin_allowed_roles = ADMIN_ROLES

    def admin_has_permission(self, request):
        for allowed_role in self.admin_allowed_roles:
            if request.user and allowed_role in request.user.user_role:
                return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user == AnonymousUser():
            return False
        if request.user.user_wallet == obj.service.company.owner:
            return True
        return self.admin_has_permission(request)
