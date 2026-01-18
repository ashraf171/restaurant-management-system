from rest_framework.permissions import BasePermission, SAFE_METHODS

class CustomerPermission(BasePermission):
    """
    Admin: full CRUD
    Manager: read-only
    Staff: read-only (GET/HEAD)
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        # Admin: full CRUD
        if request.user.is_admin:
            return True

        # Manager: can list/retrieve (read-only)
        if request.user.is_manager:
            return view.action in ['list', 'retrieve']

        # Staff: read-only
        if request.user.is_staff_member:
            return request.method in SAFE_METHODS

        return False
