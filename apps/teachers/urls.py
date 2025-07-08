from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)


urlpatterns = [
    path("reports/", views.ReportSendView.as_view(), name="reports"), #리포트 전송
    path("classes/", views.TeacherClassListView.as_view(), name="classes"), #반 리스트 불러오기
    # path('classes/<int:class_id>', views.GetClassStudentsView.as_view(), name='get_class_students'), #반 학생 불러오기 => 구현 X
    # path("reports/todo", ), # 할 일 조회       
    path("fixures/", views.FixtureListView.as_view(), name= "fixures"), # 비품 확인
]