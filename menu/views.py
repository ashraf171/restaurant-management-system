from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from .permissions import CategoryPermission, ProductPermission
from django.core.cache import cache

@extend_schema_view(
    list=extend_schema(
        summary="List all categories",
        description="Returns a list of all categories. Accessible by Admin and Manager."
    ),
    retrieve=extend_schema(
        summary="Retrieve a category",
        description="Returns the details of a single category by ID."
    ),
    create=extend_schema(
        summary="Create a new category",
        description="Only Admin and Manager can create a category.",
        request=CategorySerializer,
        responses=CategorySerializer
    ),
    update=extend_schema(
        summary="Update a category",
        description="Only Admin and Manager can update a category.",
        request=CategorySerializer,
        responses=CategorySerializer
    ),
    partial_update=extend_schema(
        summary="Partially update a category",
        description="Update only provided fields of a category.",
        request=CategorySerializer,
        responses=CategorySerializer
    ),
    destroy=extend_schema(
        summary="Delete a category",
        description="Only Admin can delete a category.",
        responses={204: None}
    )
)
class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [CategoryPermission]

    def list(self, request, *args, **kwargs):
        role = request.user.role
        cache_key = f'products_list_{role}'

        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60)
        return response


@extend_schema_view(
    list=extend_schema(
        summary="List products",
        description="""
Returns list of products.

- Admin / Manager: all products
- Staff: only available products
""",
        responses=ProductSerializer(many=True)
    ),
    retrieve=extend_schema(
        summary="Retrieve product",
        description="Get product details by ID.",
        responses=ProductSerializer
    ),
    create=extend_schema(
        summary="Create product",
        description="Admin and Manager only.",
        request=ProductSerializer,
        responses=ProductSerializer
    ),
    update=extend_schema(
        summary="Update product",
        description="Admin and Manager only.",
        request=ProductSerializer,
        responses=ProductSerializer
    ),
    partial_update=extend_schema(
        summary="Partially update product",
        description="Admin and Manager only.",
        request=ProductSerializer,
        responses=ProductSerializer
    ),
    destroy=extend_schema(
        summary="Delete product",
        description="Admin only.",
        responses={204: None}
    ),
    available_products=extend_schema(
        summary="List available products",
        description="Returns all products where `is_available=True`. Staff can only see available products.",
        responses=ProductSerializer(many=True)
    )
)
class ProductViewSet(viewsets.ModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'price']
    search_fields = ['name', 'description']
    permission_classes = [ProductPermission]

    def get_queryset(self):
        user = self.request.user
        qs = Product.objects.select_related('category')
        if user.role == 'staff':
            return qs.filter(is_available=True)
        return qs

    def list(self, request, *args, **kwargs):
        cache_key = 'products_list'
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60)
        return response

    @action(detail=False, methods=["get"], url_path="available")
    def available_products(self, request):
        products = Product.objects.filter(is_available=True)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
