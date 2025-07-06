from rest_framework import serializers
from .models import Student
from rest_framework_simplejwt.tokens import RefreshToken

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'class_id', 'name', 'birth_date', 'gender']
        read_only_fields = ['id']
    
    def validate_birth_date(self, value):
        """
        birth_date가 8자리 숫자인지 확인
        """
        if not isinstance(value, int) or len(str(value)) != 8:
            raise serializers.ValidationError("생년월일은 8자리 숫자여야 합니다. (예: 20001010)")
        return value
    
    def validate_gender(self, value):
        """
        gender가 'male' 또는 'female'인지 확인
        """
        if value not in ['male', 'female']:
            raise serializers.ValidationError("성별은 'male' 또는 'female'이어야 합니다.")
        return value