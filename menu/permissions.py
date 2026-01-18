from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS



class CategoryPermission(permissions.BasePermission):
    def has_permission(self, request, view):

      
        if not request.user or not request.user.is_authenticated:
            return False

      
        if request.user.role == 'staff':
            return request.method in SAFE_METHODS

        return request.user.role in ['admin', 'manager']


class ProductPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.role in ['admin', 'manager']:
            return True

        if request.user.role == 'staff':
            return request.method in SAFE_METHODS

        return False
