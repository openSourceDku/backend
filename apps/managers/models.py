from django.db import models

# Create your models here.

class Manager(models.Model) :
    manager_id = models.IntegerField()
    passwd = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.manager_id} {self.name}"
