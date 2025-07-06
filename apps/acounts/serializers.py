from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'role']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            role=validated_data['role'],
            password=validated_data['password']
        )
        return user
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    # 필드명 수정
    username = serializers.CharField()
    role = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")
        role = attrs.get("role")

        try:
            user = CustomUser.objects.get(username=username, role=role)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("username 또는 Role이 올바르지 않습니다.")

        if not user.check_password(password):
            raise serializers.ValidationError("비밀번호가 올바르지 않습니다.")

        # 정상 인증: JWT 토큰 발급
        data = super().validate({
            "username": username,
            "password": password,
        })

        data['role'] = user.role
        data['id'] = user.username
        return data