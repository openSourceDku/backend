from django.shortcuts import render
from django.http import HttpResponse
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

# Create your views here.

##--------------------------------------------------------------------## 여기서 부터....
# api명세서에는 모든 데이터의 등록은 api/admin/에서 진행합니다.
# 이곳에서 처리되는 모든 함수는 api/teacher/ 에서 진행될 기능들 입니다.
# 해당 기능은 reports, classes, classes/{classId}, todo, fixtures 입니다.

def index(request) :
    return HttpResponse("hello teacher apps")

@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
@permission_classes([AllowAny])  # 테스트용으로 임시 변경
def teachers_api(request):
    """
    교사 API
    GET /api/admin/teachers - 교사 조회
    POST /api/admin/teachers - 교사 등록
    PATCH /api/admin/teachers - 교사 수정
    DELETE /api/admin/teachers - 교사 삭제
    """
    if request.method == 'GET':
        # 교사 조회
        try:
            teachers = Teacher.objects.all()
            serializer = TeacherSerializer(teachers, many=True)
            
            # 응답 형식에 맞게 데이터 변환
            teachers_data = []
            for teacher in serializer.data:
                teachers_data.append({
                    "id": teacher['id'],
                    "teacher_id": teacher['teacher_id'],
                    "passwd": teacher['passwd'],
                    "teacher_name": teacher['teacher_name'],
                    "age": teacher['age'],
                    "position": teacher['position'],
                    "sex": teacher['sex']
                })
            
            return Response({
                "total_counts": len(teachers_data),
                "teachers": teachers_data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'message': '서버 내부 오류가 발생했습니다.',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == 'POST':
        # 교사 등록
        try:
            serializer = TeacherSerializer(data=request.data)
            if serializer.is_valid():
                teacher = serializer.save()
                return Response({
                    'message': '교사가 성공적으로 등록되었습니다.',
                    'teacher': TeacherSerializer(teacher).data
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'message': '잘못된 요청입니다.',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({
                'message': '잘못된 요청입니다.',
                'errors': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'message': '서버 내부 오류가 발생했습니다.',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == 'PATCH':
        # 교사 수정
        try:
            teacher_id = request.data.get('teacher_id')
            if not teacher_id:
                return Response({
                    'message': '잘못된 요청입니다.',
                    'errors': 'teacher_id가 필요합니다.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            teacher = get_object_or_404(Teacher, teacher_id=teacher_id)
            
            # teacher_id를 제외한 데이터만 업데이트
            update_data = {k: v for k, v in request.data.items() if k != 'teacher_id'}
            
            serializer = TeacherSerializer(teacher, data=update_data, partial=True)
            if serializer.is_valid():
                updated_teacher = serializer.save()
                return Response({
                    'message': '교사가 성공적으로 수정되었습니다.',
                    'teacher': TeacherSerializer(updated_teacher).data
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'message': '잘못된 요청입니다.',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except ValidationError as e:
            return Response({
                'message': '잘못된 요청입니다.',
                'errors': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'message': '서버 내부 오류가 발생했습니다.',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == 'DELETE':
        # 교사 삭제
        try:
            teacher_id = request.data.get('teacher_id')
            if not teacher_id:
                return Response({
                    'message': '잘못된 요청입니다.',
                    'errors': 'teacher_id가 필요합니다.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            teacher = get_object_or_404(Teacher, teacher_id=teacher_id)
            teacher.delete()
            
            return Response({
                'message': '교사가 성공적으로 삭제되었습니다.'
            }, status=status.HTTP_204_NO_CONTENT)
            
        except Exception as e:
            return Response({
                'message': '서버 내부 오류가 발생했습니다.',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

@api_view(['GET'])
@permission_classes([AllowAny])
def get_class_students(request, class_id):
    try:
        class_obj = Class.objects.get(id=class_id)
    except Class.DoesNotExist:
        return Response({'message': '해당 classId의 수업이 존재하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)
    students = class_obj.students.all()
    serializer = StudentSerializer(students, many=True)
    return Response({'students': serializer.data}, status=status.HTTP_200_OK)

##--------------------------------------------------------------------## 여기까지 manager view로 옮겨주세요

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
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # if user.role != 'teacher':
        #     return Response({'detail': '접근 권한이 없습니다.'}, status=403)

        class_queryset = Class.objects.filter(teacher__user=user)
        serializer = ClassSerializer(class_queryset, many=True)
        return Response({'classes': serializer.data})