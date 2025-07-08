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
    path('fixtures/<int:itemId>', FixtureUpdateView.as_view(), name='fixture-undate'),
    path('fixtures/<int:itemId>', FixtureDeleteView.as_view(), name='fixture-delete'),
    path('fixtures', FixtureListView.as_view(), name='fixture-list'),
    path('teachers/', views.TeacherAPIView.as_view(), name='teachers_api'),
    # path('classes/classrooms', ),
    # path('classes/', ),
    # path('/class-list/<int:classId>',)
    # path('teachers/classes/<int:class_id>', views.GetClassStudentsView.as_view(), name='get_class_students'),
    # path('teachers/classes/', views.TeacherClassListView.as_view(), name='classes'),
]
