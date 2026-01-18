from rest_framework.permissions import BasePermission

class IsManagerOrAdmin(BasePermission):
    """
    Admin: full CRUD
    Manager: full CRUD (update_status)
    Staff: read-only
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.role == 'admin':
            return True

        if request.user.role == 'manager':
            return True

        if request.user.role == 'staff':
            return view.action in ['list', 'retrieve']  # staff read-only

        return False
