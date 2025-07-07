from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import ClassRoom, Class
from .serializers import ClassRoomSerializer, ClassSerializer
from apps.teachers.models import Teacher
from apps.students.models import Student
from django.shortcuts import get_object_or_404

@api_view(['GET'])
@permission_classes([AllowAny])
def classroom_list(request):
    rooms = ClassRoom.objects.prefetch_related('classes__teacher').all()
    serializer = ClassRoomSerializer(rooms, many=True)
    return Response({'classes': serializer.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_classroom_and_class(request):
    data = request.data
    classroom_name = data.get('classroom')
    class_name = data.get('class_name')
    class_time = data.get('class_time')
    teacher_id = data.get('teacher_id')
    student_ids = data.get('student_ids', [])

    if not (classroom_name and class_name and class_time and teacher_id):
        return Response({'message': '필수 항목이 누락되었습니다.'}, status=status.HTTP_400_BAD_REQUEST)

    # 1. classroom 생성 또는 조회
    classroom, _ = ClassRoom.objects.get_or_create(classroom=classroom_name)

    # 2. teacher 조회
    try:
        teacher = Teacher.objects.get(id=teacher_id)
    except Teacher.DoesNotExist:
        return Response({'message': '해당 teacher_id가 존재하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)

    # 3. students 조회
    students = Student.objects.filter(id__in=student_ids)

    # 4. class 생성
    new_class = Class.objects.create(
        class_name=class_name,
        class_time=class_time,
        classroom=classroom,
        teacher=teacher
    )
    new_class.students.set(students)
    new_class.save()

    # 5. 응답
    class_data = ClassSerializer(new_class).data
    return Response({'class': class_data}, status=status.HTTP_201_CREATED)

@api_view(['PATCH', 'DELETE'])
@permission_classes([AllowAny])
def class_detail(request, class_id):
    class_obj = get_object_or_404(Class, id=class_id)

    if request.method == 'PATCH':
        data = request.data
        # classroom 변경
        classroom_name = data.get('classroom')
        if classroom_name:
            classroom, _ = ClassRoom.objects.get_or_create(classroom=classroom_name)
            class_obj.classroom = classroom
        # class_name 변경
        if 'class_name' in data:
            class_obj.class_name = data['class_name']
        # class_time 변경
        if 'class_time' in data:
            class_obj.class_time = data['class_time']
        # teacher 변경
        if 'teacher_id' in data:
            try:
                teacher = Teacher.objects.get(id=data['teacher_id'])
                class_obj.teacher = teacher
            except Teacher.DoesNotExist:
                return Response({'message': '해당 teacher_id가 존재하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)
        # students 변경
        if 'student_ids' in data:
            students = Student.objects.filter(id__in=data['student_ids'])
            class_obj.students.set(students)
        class_obj.save()
        class_data = ClassSerializer(class_obj).data
        return Response({'class': class_data}, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        class_obj.delete()
        return Response({'message': '수업이 성공적으로 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT) 