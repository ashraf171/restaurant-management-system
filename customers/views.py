from rest_framework import viewsets, permissions
from .models import Customer
from .serializers import CustomerSerializer

class CustomerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_admin:
            return True
        if request.user.is_manager and view.action in ['list', 'retrieve']:
            return True
        return False

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [CustomerPermission]






