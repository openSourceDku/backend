from django.db import migrations

def fill_email(apps, schema_editor):
    Student = apps.get_model('students', 'Student')
    for student in Student.objects.all():
        student.email = 'temp@email.com'
        student.save()

class Migration(migrations.Migration):
    dependencies = [
        ('students', '0004_rename_student_id_student_id'),
    ]

    operations = [
        migrations.RunPython(fill_email),
    ] 