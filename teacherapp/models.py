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


class CareerSuggestion(models.Model):
    YES_NO_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    operating_sys_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )

    algorithms_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )

    programming_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )

    software_eng_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )

    computer_network_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )

    electronics_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )

    computer_arc_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )

    math_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )

    communication_skills_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )

    coding_skills = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )

    is_self_learning = models.CharField(
        max_length=3,  # or any length that fits your choices
        choices=YES_NO_CHOICES,
    )

    certificate = models.TextField(max_length=250)
    interested_subject = models.TextField(max_length=100)
    is_in_teams = models.CharField(
        max_length=3,  # or any length that fits your choices
        choices=YES_NO_CHOICES,
    )

    is_introvert = models.CharField(
        max_length=3,  # or any length that fits your choices
        choices=YES_NO_CHOICES,
    )

    suggested_career = models.TextField(max_length=100)

    model_blob = models.BinaryField(blank=True, null=True)

    def __str__(self):
        return self.suggested_career
