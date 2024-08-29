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


class Lesson(models.Model):
    DAY_OF_WEEK = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
    )

    title = models.CharField(max_length=100)
    ects = models.IntegerField()
    department = models.ManyToManyField(Department)
    capacity = models.IntegerField(default=3)  # Course capacity
    day_of_week = models.CharField(
        max_length=9, choices=DAY_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    slug = models.SlugField(db_index=True, unique=True,
                            blank=True, null=True, editable=False)

    def __str__(self):
        # Return a query string and show in the screen with that format
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Lesson, self).save(*args, **kwargs)
