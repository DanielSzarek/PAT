from rest_framework.permissions import BasePermission, SAFE_METHODS


class ReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class UserEmailVerify(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.email == request.user.email
