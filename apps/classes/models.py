from django.db import models

class ClassRoom(models.Model):
    id = models.AutoField(primary_key=True)
    classroom = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.classroom} ({self.id})"

class Class(models.Model):
    id = models.AutoField(primary_key=True)
    class_name = models.CharField(max_length=100)
    class_time = models.CharField(max_length=100)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='classes')
    teacher = models.ForeignKey('teachers.Teacher', on_delete=models.CASCADE, related_name='classes')
    # students = models.ManyToManyField('students.Student', related_name='classes')

    def __str__(self):
        return self.class_name 
    
class Schedule(models.Model) :
    schedule_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    todo = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.schedule_id} = {self.name} : {self.date}"
    