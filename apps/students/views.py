from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from .models import Student
from .serializers import StudentSerializer

class StudentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
@permission_classes([AllowAny])  # 테스트용으로 임시 변경
def students_api(request):
    """
    학생 API
    GET /api/admin/students - 학생 조회
    POST /api/admin/students - 학생 등록
    PATCH /api/admin/students - 학생 수정
    DELETE /api/admin/students - 학생 삭제
    """
    if request.method == 'GET':
        # 학생 조회
        try:
            students = Student.objects.all()
            serializer = StudentSerializer(students, many=True)
            
            # 응답 형식에 맞게 데이터 변환
            students_data = []
            for student in serializer.data:
                students_data.append({
                    "id": student['id'],  # student_id를 id로 변경
                    "class_id": student['class_id'],
                    "name": student['name'],
                    "birth_date": student['birth_date'],
                    "gender": student['gender']
                })
            
            return Response({
                "total_counts": len(students_data),
                "students": students_data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'message': '서버 내부 오류가 발생했습니다.',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == 'POST':
        # 학생 등록
        try:
            serializer = StudentSerializer(data=request.data)
            if serializer.is_valid():
                student = serializer.save()
                return Response({
                    'message': '학생이 성공적으로 등록되었습니다.',
                    'student': StudentSerializer(student).data
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
        # 학생 수정
        try:
            student_id = request.data.get('id')  # student_id를 id로 변경
            if not student_id:
                return Response({
                    'message': '잘못된 요청입니다.',
                    'errors': 'id가 필요합니다.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            student = get_object_or_404(Student, id=student_id)
            
            # id를 제외한 데이터만 업데이트
            update_data = {k: v for k, v in request.data.items() if k != 'id'}
            
            serializer = StudentSerializer(student, data=update_data, partial=True)
            if serializer.is_valid():
                updated_student = serializer.save()
                return Response({
                    'message': '학생이 성공적으로 수정되었습니다.',
                    'student': StudentSerializer(updated_student).data
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
        # 학생 삭제
        try:
            student_id = request.data.get('id')  # student_id를 id로 변경
            if not student_id:
                return Response({
                    'message': '잘못된 요청입니다.',
                    'errors': 'id가 필요합니다.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            student = get_object_or_404(Student, id=student_id)
            student.delete()
            
            return Response({
                'message': '학생이 성공적으로 삭제되었습니다.'
            }, status=status.HTTP_204_NO_CONTENT)
            
        except Exception as e:
            return Response({
                'message': '서버 내부 오류가 발생했습니다.',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
