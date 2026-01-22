from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiTypes
from .models import Order
from .serializers import OrderSerializer
from .permissions import IsManagerOrAdmin

@extend_schema_view(
    list=extend_schema(
        summary="List all orders",
        description="Returns a list of all orders. Admin and Manager only.",
        responses=OrderSerializer(many=True)
    ),
    retrieve=extend_schema(
        summary="Retrieve an order",
        description="Returns the details of a single order by ID.",
        responses=OrderSerializer
    ),
    create=extend_schema(
        summary="Create a new order",
        description="Create a new order with nested items.",
        request=OrderSerializer,
        responses=OrderSerializer
    ),
    update=extend_schema(
        summary="Update an order",
        description="Update order details. Only Admin and Manager can update.",
        request=OrderSerializer,
        responses=OrderSerializer
    ),
    partial_update=extend_schema(
        summary="Partially update an order",
        description="Update only provided fields of an order.",
        request=OrderSerializer,
        responses=OrderSerializer
    ),
    destroy=extend_schema(
        summary="Delete an order",
        description="Delete an order by ID. Admin and Manager only.",
        responses={204: None}
    ),
    update_status=extend_schema(
        summary="Update order status",
        description="""
Allows Admin/Manager to update the status of an order.

Allowed transitions:
- New → Preparing
- Preparing → Ready
- Ready → Delivered
- Delivered → (cannot change)
""",
        request=OpenApiTypes.STR,
        parameters=[
            OpenApiParameter(
                name="status",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description="New status for the order"
            )
        ],
        responses={200: OrderSerializer}
    )
)
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
