from rest_framework.permissions import BasePermission, SAFE_METHODS


class ReadOnly(BasePermission):
    """Only for read."""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS


class RoleIsAdmin(BasePermission):
    """Only administrator or superuser."""

    def has_permission(self, request, view):
        user = request.user
        return (user.is_authenticated
                and (user.is_admin or user.is_superuser))

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (user.is_authenticated
                and (user.is_admin or user.is_superuser))


class RoleIsModerator(BasePermission):
    """Only for moderator."""

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_moderator


class IsAuthorOrReadOnly(BasePermission):
    """Only for author."""

    def has_object_permission(self, request, view, obj):
        return (request.user == obj.author or request.method in SAFE_METHODS)


class IsOwnerAdminModeratorOrReadOnly(BasePermission):
    """
    Must be superuser or administrator or author of the instance
    to edit or delate objects. Other users could only read.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user == obj.author
            or request.user.is_admin
            or request.user.is_superuser
            or request.user.is_moderator
        )
