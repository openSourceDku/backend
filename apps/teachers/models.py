from django.db import models

# Create your models here.

class Teacher(models.Model) :
    teacher_id = models.IntegerField(primary_key=True)
    passwd = models.CharField(max_length=100)
    age = models.IntegerField()
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    sex = models.CharField(max_length=100)

    def __str__(self):
        return str(self.teacher_id)