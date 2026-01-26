from rest_framework.permissions import BasePermission, SAFE_METHODS


class CategoryPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.role == 'staff':
            return request.method in SAFE_METHODS
        return request.user.role in ['admin', 'manager']


class ProductPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.role == 'staff':
            return request.method in SAFE_METHODS
        return request.user.role in ['admin', 'manager']
