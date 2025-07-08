from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from .views import FixtureCreateView, FixtureUpdateView, FixtureDeleteView, FixtureListView, ClassRoomListAPIView, ClassDetailAPIView
from apps.classes.views import ScheduleCreateView

urlpatterns = [
    path('', views.index, name = 'index'), #동작 확인
    path('fixtures', FixtureCreateView.as_view(), name='fixture-create'), #비품 등록
    path('fixtures/<int:itemId>', FixtureUpdateView.as_view(), name='fixture-undate'), #비품 수정
    path('fixtures/<int:itemId>', FixtureDeleteView.as_view(), name='fixture-delete'), #비품 삭제
    path('fixtures', FixtureListView.as_view(), name='fixture-list'), #비품 리스트 조회
    path('teachers/', views.TeacherAPIView.as_view(), name='teachers_api'), #선생 등록, 수정, 삭제, 조회
    path('classes/classrooms', ClassRoomListAPIView.as_view(), name= "classrooms"), #전체 반 목록 조회
    path('classes/', ScheduleCreateView.as_view(), name="classes"),   #새로운 반 등록
    path('class-list/<int:classId>', ClassDetailAPIView.as_view(), name="classDetail") #반 수정, 삭제
    # path('students/',)
]
