
from .models import Customer
from .serializer import CustomerSerializer

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from restaurant_management_system.permissions import IsAdmin, IsManagerOrAdmin
# Create your views here.

class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_permissions(self):
        # GET for admin , manager
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            permission_classes = [IsAuthenticated, IsManagerOrAdmin]
        else:
            # POST, PUT, PATCH, DELETE  for Admin
            permission_classes = [IsAuthenticated, IsAdmin]

        return [permission() for permission in permission_classes]
