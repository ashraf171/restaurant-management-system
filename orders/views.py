from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend

<<<<<<< HEAD
from .models import Order
from .serializers import OrderSerializer
from restaurant_management_system.permissions import (
    IsManagerOrAdmin,
    IsAdmin,
    IsStaffOrManagerOrAdmin
)
class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all().order_by('-order_date')
    serializer_class = OrderSerializer

    
    http_method_names = ['get', 'post', 'put']

    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['customer', 'status']

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'create']:
            permission_classes = [IsStaffOrManagerOrAdmin]
        elif self.action == 'update_status':
            permission_classes = [IsManagerOrAdmin]
=======
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


>>>>>>> 932d5aee7384e398da1f3c3f9b1def243bdf7457
        else:
            permission_classes = [IsManagerOrAdmin]

        return [permission() for permission in permission_classes]
<<<<<<< HEAD

    
    @action(detail=True, methods=['put'])
    def update_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get('status')

        if not new_status:
            return Response(
                {"error": "Status field is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            if new_status == 'Preparing':
                order.set_preparing()
            elif new_status == 'Ready':
                order.set_ready()
            elif new_status == 'Delivered':
                order.set_delivered()
            else:
                return Response(
                    {"error": "Invalid status value"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"message": f"Order status updated to {order.status}"},
            status=status.HTTP_200_OK
        )
=======
>>>>>>> 932d5aee7384e398da1f3c3f9b1def243bdf7457
