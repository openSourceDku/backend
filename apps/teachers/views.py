from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from .models import Teacher
from .serializers import TeacherSerializer

from django.core.mail import send_mail
from django.conf import settings

from apps.students.models import Student
from apps.students.serializers import StudentSerializer

from apps.classes.models import Class, Schedule
from apps.classes.serializers import ClassSerializer

from apps.managers.models import Fixture
from apps.managers.serializers import FixtureSerializer

# Create your views here.

##--------------------------------------------------------------------## 여기서 부터....
# api명세서에는 모든 데이터의 등록은 api/admin/에서 진행합니다.
# 이곳에서 처리되는 모든 함수는 api/teacher/ 에서 진행될 기능들 입니다.
# 해당 기능은 reports, classes, classes/{classId}, todo, fixtures 입니다.

def index(request) :
    return HttpResponse("hello teacher apps")

class ReportSendView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if not hasattr(user, 'role') or user.role not in ['teacher', 'admin']:
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_403_FORBIDDEN)
        data = request.data
        common = data.get('common', {})
        recipients = data.get('recipients', [])
        result_details = []
        sent_common = False
        sent_individual_count = 0
        if 'subject' in common and 'content' in common:
            sent_common = True
        for recipient in recipients:
            student_id = recipient.get('studentId')
            personal_msg = recipient.get('personalMessage')
            if student_id and personal_msg:
                sent_individual_count += 1
                result_details.append({
                    "studentId": student_id,
                    "result": "OK"
                })
            else:
                result_details.append({
                    "studentId": student_id or "unknown",
                    "result": "INVALID_DATA"
                })
        return Response({
            "status": "success",
            "sentCommon": sent_common,
            "sentIndividual": sent_individual_count,
            "details": result_details
        }, status=status.HTTP_200_OK)
    
class FixtureListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not hasattr(user, 'role') or user.role not in ['teacher', 'admin']:
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_403_FORBIDDEN)
        fixtures = Fixture.objects.all()
        serializer = FixtureSerializer(fixtures, many=True)
        formatted_data = [
            {
                "name": item["name"],
                "price": item["price"],
                "quantity": item["count"]
            }
            for item in serializer.data
        ]
        return Response({"fixtures": formatted_data})

class GetClassStudentsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, class_id):
        user = request.user
        if not hasattr(user, 'role') or user.role != 'admin':
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_403_FORBIDDEN)
        try:
            class_obj = Class.objects.get(id=class_id)
        except Class.DoesNotExist:
            return Response({'message': '해당 classId의 수업이 존재하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)
        students = class_obj.students.all()
        serializer = StudentSerializer(students, many=True)
        return Response({'students': serializer.data}, status=status.HTTP_200_OK)

class TeacherClassListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        if not hasattr(user, 'role') or user.role != 'admin':
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_403_FORBIDDEN)
        class_queryset = Class.objects.all()
        serializer = ClassSerializer(class_queryset, many=True)
        return Response({'classes': serializer.data})
    
class TeacherTodoListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user  # JWT 토큰에서 인증된 CustomUser
        try:
            teacher = Teacher.objects.get(teacher_id=user)
        except Teacher.DoesNotExist:
            return Response({"detail": "해당 교사 정보가 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        # teacher가 맡은 수업들
        classes = Class.objects.filter(teacher=teacher)

        # 각 수업에 해당하는 스케줄들 조회
        schedules = Schedule.objects.filter(schedule_id__in=classes)

        # 응답 포맷 구성
        todos = []
        for s in schedules:
            todos.append({
                "todoTitle": s.name,
                "description": s.todo,
                "date": s.date
            })

        return Response({"todos": todos}, status=status.HTTP_200_OK)