from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Order
from rest_framework.viewsets import ModelViewSet
from restaurant-management-system import IsAdmin,IsManagerOrAdmin,IsStaffOrManagerOrAdmin
from  .serializers import OrderSerializer

# Create your views here.
class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    def get_permissions(self):
        if self.action in ['create', 'list', 'retrieve']:
            permission_classes = [IsStaffOrManagerOrAdmin]


        elif self.action == 'update_status':
            permission_classes = [IsManagerOrAdmin]


        else:
            permission_classes = [IsManagerOrAdmin]

        return [permission() for permission in permission_classes]