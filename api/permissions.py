from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    """
    Allows any user to read data, but only
    the administrator can create, delete and post.
    """
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_staff
            or request.user.role == 'admin'
        )


class IsAuthorAdminModeratorOrReadOnly(BasePermission):
    """
    Allow anonynous user to read data, but Author, Admin and Moderator
    can change data.
    """
    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or (request.user.is_authenticated and request.method == 'POST')
            or (
                request.method in ['PATCH', 'DELETE']
                and (
                    request.user == obj.author
                    or request.user.is_admin
                    or request.user.is_moderator
                )
            )
        )
