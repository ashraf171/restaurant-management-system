from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

class CategoryPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return getattr(request.user, "is_admin", False) or getattr(request.user, "is_manager", False)


class ProductPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if getattr(request.user, "is_admin", False) or getattr(request.user, "is_manager", False):
            return True
        if getattr(request.user, "is_staff", False) and view.action in ['list', 'retrieve']:
            return True
        return False



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [CategoryPermission]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'price']
    search_fields = ['name', 'description']
    permission_classes = [ProductPermission]

    def get_queryset(self):
        user=self.request.user
        if user.role == 'staff':
            return Product.objects.filter(is_available=True)
        return Product.objects.all()