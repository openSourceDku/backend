from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from .models import Teacher
from .serializers import TeacherSerializer

# Create your views here.

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