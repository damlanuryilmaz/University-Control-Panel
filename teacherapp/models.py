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
    department_request = models.BooleanField(default=False)

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
    message_of_student = models.ForeignKey(
        Student, on_delete=models.CASCADE, blank=True, null=True)


class Grade(models.Model):
    GRADE_TYPE = (
        (4.0, 'AA'),
        (3.5, 'BA'),
        (3.0, 'BB'),
        (2.5, 'CB'),
        (2.0, 'CC'),
        (1.5, 'DC'),
        (1.0, 'DD'),
        (0.5, 'FD'),
        (0.0, 'FF'),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    grade = models.FloatField(choices=GRADE_TYPE)

    def __str__(self):
        return f'{self.student} - {self.lesson} - {self.grade}'
