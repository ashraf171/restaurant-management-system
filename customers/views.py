from rest_framework.viewsets import ModelViewSet
from .models import Customer
from .serializer import CustomerSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import CustomerPermission


# Create your views here.

class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated, CustomerPermission]

