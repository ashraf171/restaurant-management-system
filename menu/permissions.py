from rest_framework import permissions

class CategoryPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'manager']

class ProductPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.role in ['admin', 'manager']:
            return True
        if request.user.role == 'staff' and view.action in ['list', 'retrieve']:
            return True
        return False