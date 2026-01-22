from rest_framework import viewsets
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import Customer
from .serializers import CustomerSerializer
from .permissions import CustomerPermission

@extend_schema_view(
    list=extend_schema(
        summary="List all customers",
        description="Returns a list of all customers. Staff can only view customers if allowed by permissions.",
        responses=CustomerSerializer(many=True)
    ),
    retrieve=extend_schema(
        summary="Retrieve a customer",
        description="Returns the details of a single customer by ID.",
        responses=CustomerSerializer
    ),
    create=extend_schema(
        summary="Create a new customer",
        description="Create a customer with first_name, last_name, email, phone, and address.",
        request=CustomerSerializer,
        responses=CustomerSerializer
    ),
    update=extend_schema(
        summary="Update a customer",
        description="Update customer details. Partial updates are allowed.",
        request=CustomerSerializer,
        responses=CustomerSerializer
    ),
    partial_update=extend_schema(
        summary="Partially update a customer",
        description="Update only provided fields of a customer.",
        request=CustomerSerializer,
        responses=CustomerSerializer
    ),
    destroy=extend_schema(
        summary="Delete a customer",
        description="Delete a customer by ID.",
        responses={204: None}
    )
)
class CustomerViewSet(viewsets.ModelViewSet):

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [CustomerPermission]
