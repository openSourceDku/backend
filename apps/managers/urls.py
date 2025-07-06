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
    path('fixtures', FixtureCreateView.as_view(), name='fixture-create'),
    path('fixtures/{itemId}', FixtureUpdateView.as_view(), name='fixture-undate'),
    path('fixtures/{itemId}', FixtureDeleteView.as_view(), name='fixture-delete'),
    path('fixtures/{itemId}', FixtureListView.as_view(), name='fixture-list'),
]