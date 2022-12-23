from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:  # 'GET', OPTIONS, HEAD
            return True  # Anonymous user

        return bool(request.user and request.user.is_staff)  # Admin user
