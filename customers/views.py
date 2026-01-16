from rest_framework import viewsets, permissions
from .models import Customer
from .serializers import CustomerSerializer
from .permissions import CustomerPermission



class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [CustomerPermission]






