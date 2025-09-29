from rest_framework.permissions import BasePermission


class CustomPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        perms_map = getattr(view, 'perms_map', {})
        required_roles = perms_map.get(request.method, [])
        if not required_roles:
            return True

        return request.user.role in required_roles