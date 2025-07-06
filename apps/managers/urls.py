from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from .views import FixtureCreateView, FixtureUpdateView, FixtureDeleteView, FixtureListView

urlpatterns = [
    path('', views.index, name = 'index'),
    path('api/admin/fixtures', FixtureCreateView.as_view(), name='fixture-create'),
    path('api/admin/fixtures/{itemId}', FixtureUpdateView.as_view(), name='fixture-undate'),
    path('api/admin/fixtures/{itemId}', FixtureDeleteView.as_view(), name='fixture-delete'),
    path('api/admin/fixtures/{itemId}', FixtureListView.as_view(), name='fixture-list'),
]

