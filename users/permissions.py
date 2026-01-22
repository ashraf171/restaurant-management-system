from rest_framework.permissions import BasePermission

class IsAdminUserCustom(BasePermission):
    message = "You must be an admin to perform this action."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and getattr(request.user, "role", None) == 'admin')

    def has_object_permission(self, request, view, obj):

        return self.has_permission(request, view)
