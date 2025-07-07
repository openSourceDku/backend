from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from .models import Teacher
from .serializers import TeacherSerializer

from django.core.mail import send_mail
from django.conf import settings

from apps.students.models import Student
from apps.students.serializers import StudentSerializer

from apps.classes.models import Class
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

@api_view(['POST'])
@permission_classes([AllowAny])  # 실제 운영시에는 인증 필요
def send_report_to_students(request):
    data = request.data
    common = data.get('common', {})
    recipients = data.get('recipients', [])

    subject = common.get('subject', '')
    content = common.get('content', '')

    results = []
    for rec in recipients:
        student_id = rec.get('studentId')
        personal_msg = rec.get('personalMessage', '')
        try:
            student = Student.objects.get(id=student_id)
            full_content = f"{content}\n\n{personal_msg}"
            send_mail(
                subject,
                full_content,
                settings.DEFAULT_FROM_EMAIL,
                [student.email],
                fail_silently=False,
            )
            results.append({
                'studentId': student_id,
                'email': student.email,
                'status': 'sent'
            })
        except Student.DoesNotExist:
            results.append({
                'studentId': student_id,
                'status': 'not_found'
            })
        except Exception as e:
            results.append({
                'studentId': student_id,
                'status': 'error',
                'error': str(e)
            })

    return Response({'results': results}, status=status.HTTP_200_OK)

class ReportSendView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not (request.user and request.user.role == 'admin') :
            return Response({"detail": "You do not have permission to perform this action"}, status=status.HTTP_403_FORBIDDEN)

        data = request.data

        common = data.get('common', {})
        recipients = data.get('recipients', [])

        result_details = []
        sent_common = False
        sent_individual_count = 0

        # 1. 공통 메시지 처리
        if 'subject' in common and 'content' in common:
            # TODO: 공통 메시지 전송 로직 구현 예정
            # 예: 모든 학생의 학부모에게 메시지를 전송
            sent_common = True

        # 2. 개별 메시지 처리
        for recipient in recipients:
            student_id = recipient.get('studentId')
            personal_msg = recipient.get('personalMessage')

            if student_id and personal_msg:
                # TODO: student_id에게 개인 메시지 전송 로직 구현 예정
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


class TeacherClassListView(APIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]  # 필요시 변경

    def get(self, request):
        user = request.user
        # if user.role != 'teacher':
        #     return Response({'detail': '접근 권한이 없습니다.'}, status=403)

        # class_queryset = Class.objects.filter(teacher__user=user)
        class_queryset = Class.objects.all()
        serializer = ClassSerializer(class_queryset, many=True)
        return Response({'classes': serializer.data})
    
class FixtureListView(APIView):
    permission_classes = [IsAuthenticated]  # JWT 인증 필요

    def get(self, request):
        fixtures = Fixture.objects.all()
        serializer = FixtureSerializer(fixtures, many=True)
        # "count" → "quantity" 이름 변경
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
    permission_classes = [AllowAny]

    def get(self, request, class_id):
        try:
            class_obj = Class.objects.get(id=class_id)
        except Class.DoesNotExist:
            return Response({'message': '해당 classId의 수업이 존재하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)
        students = class_obj.students.all()
        serializer = StudentSerializer(students, many=True)
        return Response({'students': serializer.data}, status=status.HTTP_200_OK)