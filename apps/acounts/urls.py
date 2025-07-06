# user/urls.py
from django.urls import path
from .views import RegisterView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

app_name = "acounts"
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # 여기만 바뀜
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]