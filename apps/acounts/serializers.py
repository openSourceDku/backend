from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from apps.managers.models import Manager
from apps.teachers.models import Teacher

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

        # JWT 토큰 발급
        token_data = super().validate({
            "username": username,
            "password": password,
        })

        # 공통 응답 구조
        response_data = {
            "status": "success",
            "message": "로그인 성공",
            "accessToken": token_data.get("access"),
            "refreshToken": token_data.get("refresh"),
        }

        # 사용자 정보
        user_info = {"id": user.id}

        if role == "teacher":
            try:
                teacher = Teacher.objects.get(teacher_id=user)
                user_info.update({
                    "age": teacher.age,
                    "name": teacher.teacher_name,
                    "position": teacher.position,
                    "sex": teacher.sex,
                })
            except Teacher.DoesNotExist:
                raise serializers.ValidationError("해당 교사 정보가 존재하지 않습니다.")
        
        elif role == "admin":
            try:
                manager = Manager.objects.get(manager_id=user)
                user_info.update({
                    "age": None,  # 관리자에는 age가 없음
                    "name": manager.name,
                    "position": manager.position,
                    "sex": None,  # 관리자에는 성별 없음
                })
            except Manager.DoesNotExist:
                raise serializers.ValidationError("해당 관리자 정보가 존재하지 않습니다.")
        
        else:
            raise serializers.ValidationError("지원하지 않는 Role입니다.")

        response_data["user"] = user_info
        return response_data

# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     # 필드명 수정
#     username = serializers.CharField()
#     role = serializers.CharField()

#     def validate(self, attrs):
#         username = attrs.get("username")
#         password = attrs.get("password")
#         role = attrs.get("role")

#         try:
#             user = CustomUser.objects.get(username=username, role=role)
#         except CustomUser.DoesNotExist:
#             raise serializers.ValidationError("username 또는 Role이 올바르지 않습니다.")

#         if not user.check_password(password):
#             raise serializers.ValidationError("비밀번호가 올바르지 않습니다.")

#         # 정상 인증: JWT 토큰 발급
#         data = super().validate({
#             "username": username,
#             "password": password,
#         })

#         data['role'] = user.role
#         data['id'] = user.username
#         return data