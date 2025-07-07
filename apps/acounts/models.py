from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

class CustomUserManager(BaseUserManager):
    '''
    teacher와 admin 계정을 생성하는 로직을 작성합니다. 
    '''
    def create_user(self, username, role, password=None):
        if not username:
            raise ValueError("Users must have a username")
        if role not in ["teacher", "admin"]:
            raise ValueError("Role must be 'teacher' or 'admin'")

        user = self.model(username=username, role=role)
        user.set_password(password)
        user.save(using=self._db)

        #role이 admin일 경우 manager테이블에 자동 추가
        if role == 'admin':
            from apps.managers.models import Manager
            Manager.objects.create(
                manager_id=user,
                name=username,  # 이름을 username으로 기본 설정
                position='관리자'  # position 기본값, 원하면 수정 가능
            )
            
        return user

    def create_superuser(self, username, role="admin", password=None):
        user = self.create_user(username=username, role=role, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    '''
    실제 유저 모델입니다.
    필드 값은 다음과 같습니다.
        username : integer
        role : charField

    password는 RegisterSerializer에서 등록합니다.
    '''

    ROLE_CHOICES = (
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    )

    username = models.CharField(max_length=100, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # 관리자 여부

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['role']  # createsuperuser 시 입력 필드

    def __str__(self):
        return self.username