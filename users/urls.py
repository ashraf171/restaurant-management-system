from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from django.urls import path
from .views import LogoutView

router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path("logout/", LogoutView.as_view(), name="logout"),
]

urlpatterns+= router.urls