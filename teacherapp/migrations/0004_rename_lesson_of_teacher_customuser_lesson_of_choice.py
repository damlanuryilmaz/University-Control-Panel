# Generated by Django 5.0.7 on 2024-08-05 07:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teacherapp', '0003_alter_customuser_lesson_of_teacher'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='lesson_of_teacher',
            new_name='lesson_of_choice',
        ),
    ]
