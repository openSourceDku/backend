from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Fixture
from .serializers import FixtureSerializer
from django.http import HttpResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from apps.teachers.models import Teacher
from apps.teachers.serializers import TeacherSerializer
from apps.students.models import Student
from apps.students.serializers import StudentSerializer
from apps.classes.models import Class
from apps.classes.serializers import ClassSerializer
from apps.acounts.models import CustomUser

# Create your views here.

def index(request) :
    return HttpResponse("hello manager apps")

class FixtureCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]  #Authentication required

    def post(self, request):
        user = request.user
        if not user.is_authenticated or getattr(user, 'role', None) != 'admin':
            return Response({"detail": "You do not have permission to perform this action"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = FixtureSerializer(data=request.data)
        if serializer.is_valid():
            fixture = serializer.save()
            return Response({
                "itemId": fixture.id,
                "name": fixture.name,
                "price": fixture.price,
                "count": fixture.count
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FixtureUpdateView(APIView):    
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, itemId):
        user = request.user
        if not user.is_authenticated or getattr(user, 'role', None) != 'admin':
            return Response({"detail": "You do not have permission to perform this action"}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            fixture = Fixture.objects.get(id=itemId)
        except Fixture.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = FixtureSerializer(fixture, data=request.data, partial=True)
        if serializer.is_valid():
            fixture = serializer.save()
            return Response({
                "itemId": fixture.id,
                "name": fixture.name,
                "price": fixture.price,
                "count": fixture.count
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class FixtureDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, itemId):
        user = request.user
        if not user.is_authenticated or getattr(user, 'role', None) != 'admin':
            return Response({"detail": "You do not have permission to perform this action"}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            fixture = Fixture.objects.get(id=itemId)
        except Fixture.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        fixture.delete()
        return Response({}, status=status.HTTP_400_BAD_REQUEST)
    
class FixtureListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        page = int(request.GET.get('page',1))   #Retrieve query parameters(page, size)
        size = int(request.GET.get('size',10))
        #Get all data quryset
        queryset = Fixture.objects.all().order_by('id')
        total_count = queryset.count()
        total_page = (total_count + size - 1) // size

        #Apply pagination
        start = (page - 1) * size
        end = start + size
        fixtures = queryset[start:end]

        #Serialize data and convert id to itemId
        data = [
            {
                "itemId":obj.id,
                "name": obj.name,
                "price": obj.price,
                "count": obj.count
            }
            for obj in fixtures
        ]
        return Response({
            "page": page,
            "size": size,
            "totalPage": total_page,
            "totalCount": total_count,
            "data": data
        }, status=status.HTTP_200_OK)
    
class TeacherAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user # CustomUser 인식

        if not hasattr(user, 'role') or user.role != 'admin':
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            teachers = Teacher.objects.all()
            serializer = TeacherSerializer(teachers, many=True)
            teachers_data = []
            for teacher in serializer.data:
                teachers_data.append({
                    "teacher_id": teacher['teacher_id'],
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
    
    def post(self, request):
        user = request.user
        if not hasattr(user, 'role') or user.role != 'admin':
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            data = request.data.copy()
            
            # 1️⃣ CustomUser 생성
            teacher_username = data.get('teacher_id')
            teacher_password = data.get('passwd')
            
            if not teacher_username or not teacher_password:
                return Response({
                    'message': 'teacher_id와 passwd는 필수입니다.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if CustomUser.objects.filter(username=teacher_username).exists():
                return Response({
                    'message': '이미 존재하는 사용자입니다.'
                }, status=status.HTTP_400_BAD_REQUEST)

            new_user = CustomUser.objects.create_user(
                username=teacher_username,
                role='teacher',
                password=teacher_password
            )

            # 2️⃣ Teacher 모델 등록
            teacher_data = {
                'teacher_id': new_user.id,
                'teacher_name': data.get('teacher_name'),
                'age': data.get('age'),
                'position': data.get('position'),
                'sex': data.get('sex'),
            }

            serializer = TeacherSerializer(data=teacher_data)
            if serializer.is_valid():
                teacher = serializer.save()
                return Response({
                    'message': '교사가 성공적으로 등록되었습니다.',
                    'teacher': TeacherSerializer(teacher).data
                }, status=status.HTTP_201_CREATED)
            else:
                # 유저는 생성했지만 교사 정보 유효성 실패 -> 유저 삭제
                new_user.delete()
                return Response({
                    'message': '교사 정보가 유효하지 않습니다.',
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

        # def post(self, request):
        #     # TODO: customer테의블의 id값이 teacher_id의 값으로 설정함.
        #     user = request.user # CustomUser 인식
        #     if not hasattr(user, 'role') or user.role != 'admin':
        #         return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_403_FORBIDDEN)
            
        #     try:
        #         data = request.data.copy() # User데이터 가져오기
        #         data['teacher_id'] = user.id 
        #         serializer = TeacherSerializer(data=data)
        #         if serializer.is_valid():
        #             teacher = serializer.save()

        #             return Response({
        #                 'message': '교사가 성공적으로 등록되었습니다.',
        #                 'teacher': TeacherSerializer(teacher).data
        #             }, status=status.HTTP_201_CREATED)
        #         else:
        #             return Response({
        #                 'message': '잘못된 요청입니다.',
        #                 'errors': serializer.errors
        #             }, status=status.HTTP_400_BAD_REQUEST)
        #     except ValidationError as e:
        #         return Response({
        #             'message': '잘못된 요청입니다.',
        #             'errors': str(e)
        #         }, status=status.HTTP_400_BAD_REQUEST)
        #     except Exception as e:
        #         return Response({
        #             'message': '서버 내부 오류가 발생했습니다.',
        #             'error': str(e)
        #         }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request):
        user = request.user
        if not hasattr(user, 'role') or user.role != 'admin':
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_403_FORBIDDEN)
        try:
            teacher_id = request.data.get('teacher_id')
            if not teacher_id:
                return Response({
                    'message': '잘못된 요청입니다.',
                    'errors': 'teacher_id가 필요합니다.'
                }, status=status.HTTP_400_BAD_REQUEST)
            teacher = get_object_or_404(Teacher, teacher_id=teacher_id)
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
    def delete(self, request):
        user = request.user
        if not hasattr(user, 'role') or user.role != 'admin':
            return Response({'detail': 'You do not have permission to perform this action'}, status=status.HTTP_403_FORBIDDEN)
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
    
    
#테스트코드용
def home(request):
    return HttpResponse("Welcome")