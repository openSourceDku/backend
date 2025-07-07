from django.db import models
from apps.acounts.models import CustomUser

# Create your models here.

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