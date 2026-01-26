from rest_framework.permissions import BasePermission

class IsAdminUserCustom(BasePermission):
    message = "Admin access required."

    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role == request.user.Role.ADMIN
        )
    def has_object_permission(self, request, view, obj):

        return self.has_permission(request, view)
