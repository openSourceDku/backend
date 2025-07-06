from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

urlpatterns = [
    path('', views.teachers_api, name='teachers_api'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('reports', views.send_report_to_students, name='send_report_to_students'),
    path('classes/<int:class_id>', views.get_class_students, name='get_class_students'),
]