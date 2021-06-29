from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdmin(BasePermission):
    """
    Check if User has 'admin' role
    """
    def has_permission(self, request, view):
        return request.user.is_staff or request.user.is_admin


class IsOwner(BasePermission):
    """
    Check if User is object owner
    """
    def has_object_permission(self, request, view, obj):
        return obj.username == request.user.username


class IsModerator(BasePermission):
    """
    Check if User has 'administrator' role
    """
    def has_permission(self, request, view):
        return request.user.is_moderator


class IsAdminOrReadOnly(BasePermission):
    """
    Check if User has 'admin' role or allow read only access
    """
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (
            request.user.is_staff or request.user.is_admin
        )
