from rest_framework.permissions import BasePermission

class CustomerPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if getattr(request.user, "is_admin", False):
            return True
        if getattr(request.user, "is_manager", False) and view.action in ['list', 'retrieve']:
            return True
        return False