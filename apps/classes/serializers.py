from rest_framework import serializers
from .models import ClassRoom, Class
from apps.teachers.models import Teacher
from apps.students.models import Student

class TeacherSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'teacher_id', 'teacher_name']

class ClassSerializer(serializers.ModelSerializer):
    teacher = TeacherSimpleSerializer(read_only=True)
    class Meta:
        model = Class
        fields = ['id', 'class_name', 'class_time', 'teacher']

class ClassRoomSerializer(serializers.ModelSerializer):
    classes = ClassSerializer(many=True, read_only=True)
    class Meta:
        model = ClassRoom
        fields = ['id', 'classroom', 'classes'] 