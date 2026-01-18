from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Order
from .serializers import OrderSerializer
from .permissions import IsManagerOrAdmin

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsManagerOrAdmin]

    @action(detail=True, methods=['put'])
    def update_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get("status")


        if new_status not in dict(Order.STATUS_CHOICES):
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)


        allowed_transitions = {
            "New": ["Preparing"],
            "Preparing": ["Ready"],
            "Ready": ["Delivered"],
            "Delivered": []
        }

        if new_status not in allowed_transitions[order.status]:
            return Response(
                {"error": f"Cannot change status from {order.status} to {new_status}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = new_status
        order.save()
        return Response({"status": order.status})

