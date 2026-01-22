from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiTypes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .models import User
from .serializers import UserSerializer
from .permissions import IsAdminUserCustom


@extend_schema_view(
    list=extend_schema(
        summary="List all users",
        description="Returns a list of all users. Admin only.",
        responses=UserSerializer(many=True)
    ),
    retrieve=extend_schema(
        summary="Retrieve a user",
        description="Returns the details of a single user by ID. Admin only.",
        responses=UserSerializer
    ),
    create=extend_schema(
        summary="Create a new user",
        description="Admin only. Can create user with role: admin, manager, or staff.",
        request=UserSerializer,
        responses=UserSerializer
    ),
    update=extend_schema(
        summary="Update a user",
        description="Admin only. Update user details including role.",
        request=UserSerializer,
        responses=UserSerializer
    ),
    partial_update=extend_schema(
        summary="Partially update a user",
        description="Admin only. Update only provided fields.",
        request=UserSerializer,
        responses=UserSerializer
    ),
    destroy=extend_schema(
        summary="Delete a user",
        description="Admin only. Delete a user by ID.",
        responses={204: None}
    )
)
class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUserCustom]


class LogoutView(APIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Logout user",
        description="Blacklists the provided refresh token to logout the user.",
        request={
            "refresh": OpenApiTypes.STR
        },
        responses={
            200: OpenApiTypes.STR,
            400: OpenApiTypes.STR
        }
    )
    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"detail": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful"}, status=status.HTTP_200_OK)
        except TokenError:
            return Response({"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
