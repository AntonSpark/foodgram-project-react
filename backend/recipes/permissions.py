from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsAllowedOrReadOnly(BasePermission):
    """У всех кроме автора и суперюзера есть доступ только к GET."""
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_superuser
        )
