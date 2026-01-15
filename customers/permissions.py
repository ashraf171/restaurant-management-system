from rest_framework.permissions import BasePermission

class CustomerPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_admin:
            return True
        if request.user.is_manager and view.action in ['list', 'retrieve']:
            return True
        return False