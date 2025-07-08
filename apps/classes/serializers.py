from rest_framework import serializers
from .models import ClassRoom, Class
from apps.teachers.models import Teacher
from apps.students.models import Student
from .models import Schedule

class TeacherSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'teacher_id', 'teacher_name']

class ClassSerializer(serializers.ModelSerializer):
    classId = serializers.IntegerField(source='id')
    className = serializers.CharField(source='class_name')
    time = serializers.IntegerField(source='class_time')
    content = serializers.CharField(source='class_name')  # content를 위한 필드가 모델에 없으므로 class_name 임시 사용
    classroom = serializers.IntegerField(source='classroom.id')

    class Meta:
        model = Class
        fields = ['classId', 'className', 'time', 'content', 'classroom']

class ClassRoomSerializer(serializers.ModelSerializer):
    classes = ClassSerializer(many=True, read_only=True)
    class Meta:
        model = ClassRoom
        fields = ['id', 'classroom', 'classes'] 

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['schedule_id', 'name', 'date', 'todo']