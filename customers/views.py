from rest_framework.viewsets import ModelViewSet
from .models import Customer
from .serializer import CustomerSerializer


# Create your views here.

class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
