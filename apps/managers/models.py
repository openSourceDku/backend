from django.db import models
from apps.acounts.models import CustomUser

# Create your models here.

class Manager(models.Model) :
    '''
    상위 모델인 CustomUser에 만들어진 username으로 manager_id를 검색한다.
    Teacher의 teacher_id은 CustomUser의 username를 외래키로 가지며, 서로를 유일하게 식별한다.
    password, role은 CustomUser에 등록되어 있다.
    '''
    manager_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # passwd = models.CharField(max_length=100) 
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.manager_id.id} : {self.name}"
