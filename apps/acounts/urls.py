# user/urls.py
from django.urls import path
from .views import RegisterView, CustomTokenObtainPairView, LogoutView
from rest_framework_simplejwt.views import TokenRefreshView

app_name = "acounts"
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),                     #계정 등록
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
]