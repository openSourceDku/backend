from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, students_api
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

router = DefaultRouter()
router.register('students', StudentViewSet)

urlpatterns = [
    path('', students_api, name='students_api'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls
