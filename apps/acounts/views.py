from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import RegisterSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
'''
이 views.py는 프로젝트의 계정관리 기능을 담당하고 있다.
JWT 방식으로 구현되어 있다.

회원가입시 3가지 필드가 필요하다.
    username : charField
    password : charField
    role     : charField (only teacher or admin)

로그인시 위의 3가지 필드가 필요하다.
    리턴하는 응답으로 현 로그인한 계정의 정보를 알 수 있다.

로그아웃시 access 토큰으로 본인인지 확인 후 refresh토큰을 비활성화 시켜 사실상 로그아웃 상태로 만든다.

'''

# Create your views here.
#회원가입, 로그인, 로그아웃, refresh동작

class RegisterView(APIView):
    '''
    계정 등록 뷰이다. admin, teacher 통합 테이블로 오직 id, password, role 필드 값만 존재한다.
    id 값으로 teacher를 찾을 수 있다. 관련 계정 등록은 admin(현 manager)에서 진행한다.
    admin계정은 슈퍼계정 admin/에서 진행한다.
    '''
    def post(self, request):
        '''
        json 형식으로 request를 받고, 올바른 값이면 계정db에 저장한다.
            {
                username : charField
                password : charField
                role     : charField ("teacher" or "admin")
            }
        '''
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

#로그인 뷰
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
#로그아웃 뷰
class LogoutView(APIView):
    '''
    로그아웃 하는 뷰이다.
    JWT 특성상 명시적인 로그아웃 기능은 없다. 
    하지만, 로그인 한 계정의 refresh 토큰을 블랙리스트화 하면 그 계정으로 접근하지 못하므로 로그아웃으로 간주한다.
    '''
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)