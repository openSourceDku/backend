from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

router = DefaultRouter()
router.register('students', StudentViewSet)

urlpatterns = []
