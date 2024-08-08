from django.db import models
from django.contrib.auth.models import AbstractUser
from baseapp.models import Department, Lesson

# Create your models here.


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
    department_of_student = models.ForeignKey(
        Department, on_delete=models.CASCADE, blank=True, null=True)
    student_ects = models.IntegerField(default=0)
    student_lessons = models.ManyToManyField(Lesson, blank=True,)

    def __str__(self):
        return self.user.username


class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    lesson_of_teacher = models.ManyToManyField(Lesson, blank=True,)

    def __str__(self):
        return self.user.username


class Contact(models.Model):
    message = models.TextField(max_length=500)
    message_of_teacher = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    message_of_student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name
