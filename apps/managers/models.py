from django.db import models
from apps.acounts.models import CustomUser

# Create your models here.

class Manager(models.Model) :
    '''
    외래키 = CustomUser로 등록, password 는 CustomUser사용
    '''
    manager_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.manager_id.id} {self.name}"

class Fixture(models.Model):
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    count = models.PositiveIntegerField()

    def __str__(self):
        return self.name