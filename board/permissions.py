from email import message
from rest_framework import permissions


class BasePermission(permissions.BasePermission):
    message = "Not permitted"

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        elif request.user.is_staff:
            return True
        else:
            return False


class UserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_active:
            return True


class OnlyAdminPermission(permissions.BasePermission):
    message = "only permitted of admin"

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        