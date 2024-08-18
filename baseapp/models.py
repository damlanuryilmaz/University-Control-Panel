from django.db import models
from django.utils.text import slugify


class Department(models.Model):
    title = models.CharField(max_length=150)
    capacity = models.IntegerField(default=10)
    slug = models.SlugField(db_index=True, unique=True,
                            blank=True, null=False, editable=False)

    def save(self, *args, **kwargs):
        # Create a slug and use it for the url
        self.slug = slugify(self.title)
        super(Department, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class CourseHour(models.Model):
    DAY_OF_WEEK = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    )

    day_of_week = models.CharField(max_length=9, choices=DAY_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f'{self.day_of_week} {self.start_time} - {self.end_time}'


class Lesson(models.Model):
    title = models.CharField(max_length=100)
    ects = models.IntegerField()
    category = models.ManyToManyField(Department)
    capacity = models.IntegerField(default=3)  # Course capacity
    course_hour = models.ForeignKey(
        CourseHour, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        # Return a query string and show in the screen with that format
        return (f'{self.title} | {self.ects} ECTS | {self.capacity} Capacity | '
                f'{self.course_hour}'
                )
