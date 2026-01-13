
from .models import Customer
from .serializer import CustomerSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from restaurant_management_system.permissions import IsAdmin, IsManagerOrAdmin
# Create your views here.


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all().order_by('-registration_date')
    serializer_class = CustomerSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['email']
    search_fields = ['first_name', 'last_name', 'email', 'phone']

    def get_permissions(self):
        # GET for admin , manager
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            permission_classes = [IsAuthenticated, IsManagerOrAdmin]
        else:
            # POST, PUT, PATCH, DELETE  for Admin
            permission_classes = [IsAuthenticated, IsAdmin]

        return [permission() for permission in permission_classes]
    
    def perform_destroy(self, instance):
        if instance.orders.exists():
            raise ValidationError("Cannot delete customer with existing orders.")
        instance.delete()
