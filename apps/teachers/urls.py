from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)


urlpatterns = [
    path("reports/", views.ReportSendView.as_view, name="reports"),
    path("classes/", views.TeacherClassListView.as_view, name="classes"),
    # path("classes/{classId}", ), # 학생 구현 안함 
    # path("reports/todo", ),       
    path("fixures/", views.FixtureListView.as_view, name= "fixures"),
]