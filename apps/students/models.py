from django.db import models

class Student(models.Model):
    id = models.AutoField(primary_key=True)
    class_id = models.IntegerField()
    name = models.CharField(max_length=30)
    birth_date = models.IntegerField()
    gender = models.CharField(max_length=10, choices=(('male', 'male'), ('female', 'female')))


