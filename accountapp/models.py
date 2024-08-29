from django.contrib.auth.models import AbstractUser
from baseapp.models import Department, Lesson
from django.db import models


class CustomUser(AbstractUser):
    STATUS = (
        ('Teacher', 'Teacher'),
        ('Student', 'Student'),
        ('Admin', 'Admin'),
    )

    status = models.CharField(
        max_length=100, choices=STATUS, default='Student',)

    def __str__(self):
        return self.username


class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, blank=True, null=True)
    acts = models.IntegerField(default=0)
    lessons = models.ManyToManyField(Lesson, blank=True,
                                     through='StudentLesson')
    department_request = models.BooleanField(default=False)
    adviser = models.ForeignKey(
        'Teacher', on_delete=models.CASCADE, blank=True, null=True)
    is_submitted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class StudentLesson(models.Model):
    students = models.ForeignKey(Student, on_delete=models.CASCADE)
    lessons = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.students} - {self.lessons}'


class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    lessons = models.ManyToManyField(Lesson, blank=True,)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
