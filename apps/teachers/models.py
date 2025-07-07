from django.db import models
from apps.acounts.models import CustomUser

# Create your models here.

#id, password 필드 삭제해 주세요 teacher_id = models.CharField(CustomUser, on_delete = models.CASCAD) 로 변경해 주세요
class Teacher(models.Model) :
    id = models.AutoField(primary_key=True)
    teacher_id = models.CharField(max_length=100, unique=True)
    passwd = models.CharField(max_length=100)
    teacher_name = models.CharField(max_length=100)
    age = models.IntegerField()
    position = models.CharField(max_length=100)
    sex = models.CharField(max_length=100)

    def __str__(self):
        return self.teacher_name