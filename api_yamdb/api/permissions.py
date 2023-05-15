from rest_framework.permissions import BasePermission, SAFE_METHODS


class ReadOnly(BasePermission):
    """Only for read."""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    Must be an authenticated superuser or an admin user
    to delete and/or edit objects.
    Other users may only view a single object or a list of objects.

    """
    message = "Editing or deleting this item is not allowed."

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or (
                request.user.is_authenticated
                and (request.user.is_admin or request.user.is_superuser)
            )
        )


class IsAdminOnly(BasePermission):
    """
    Must be an authenticated superuser or an admin user to perform any actions.

    """
    message = "This action is not allowed."

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.is_admin or request.user.is_superuser))


class RoleIsModerator(BasePermission):
    """Only for moderator."""

    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.is_authenticated and user.is_moderator


class IsAuthorOrReadOnly(BasePermission):
    """Only for author."""

    def has_object_permission(self, request, view, obj):
        return (request.user == obj.author or request.method in SAFE_METHODS)
