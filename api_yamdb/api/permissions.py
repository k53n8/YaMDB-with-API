from rest_framework import permissions

      
class IsAuthorOrReadOnly(permissions.BasePermission):
    '''Прверка смертных'''
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)


class IsModer(permissions.BasePermission):
    '''Определение прав модератора:
       Права для рдактирования комментариев и отзывов.
    '''
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                and request.user.is_moderator
                )


class IsAdmin(permissions.BasePermission):
    '''Определение прав администратора/суперюзера:
       Права на редактирование/удаление контента,
       Создание или удаление жанров и категорий,
       Назначение ролей.
    '''
    def has_objects_permissions(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                and request.user.is_admin or request.user.is_superuser
                )

# class AdminOrReadOnly(permissions.BasePermission):
#     """Разрешение для админа или любого GET-запроса."""

#     def has_permission(self, request, view):
#         if request.user.is_authenticated:
#             return (
#                 request.method in permissions.SAFE_METHODS
#                 or request.user.is_admin
#             )
#         else:
#             return request.method in permissions.SAFE_METHODS

#     def has_object_permission(self, request, view, obj):
#         if request.user.is_authenticated:
#             return (
#                 request.method in permissions.SAFE_METHODS
#                 or request.user.is_admin
#             )
#         else:
#             return request.method in permissions.SAFE_METHODS


# class IsAdminModeratorOwnerOrReadOnly(permissions.BasePermission):
#     """Разрешение для автора, модератора, админа или суперюзера."""

#     def has_permission(self, request, view):
#         return (
#             request.method in permissions.SAFE_METHODS
#             or request.user.is_authenticated
#         )

#     def has_object_permission(self, request, view, obj):

#         return (
#             request.method in permissions.SAFE_METHODS
#             or request.user.is_admin
#             or request.user.is_moderator
#             or obj.author == request.user)


# class IsAdmin(permissions.BasePermission):
#     """Разрешение для админа или суперюзера."""
#     def has_permission(self, request, view):
#         return request.user.is_authenticated and (
#             request.user.is_admin or request.user.is_superuser)
