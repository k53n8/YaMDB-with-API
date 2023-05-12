from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):
    """Разрешение для админа или любого GET-запроса."""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                request.method in permissions.SAFE_METHODS
                or request.user.is_admin
            )
        else:
            return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (
                request.method in permissions.SAFE_METHODS
                or request.user.is_admin
            )
        else:
            return request.method in permissions.SAFE_METHODS


class IsAdminModeratorOwnerOrReadOnly(permissions.BasePermission):
    """Разрешение для автора, модератора, админа или суперюзера."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):

        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
            or request.user.is_moderator
            or obj.author == request.user)
