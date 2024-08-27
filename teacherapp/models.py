from accountapp.models import CustomUser, Student
from baseapp.models import Lesson
from django.db import models


class Contact(models.Model):
    message = models.TextField(max_length=500)
    teacher = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    student = models.ForeignKey(
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
