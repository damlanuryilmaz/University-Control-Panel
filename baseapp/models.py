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
    title = models.CharField(max_length=100)
    ects = models.IntegerField()
    category = models.ManyToManyField(Department)
    capacity = models.IntegerField(default=3)  # Course capacity

    def __str__(self):
        # Return a query string and show in the screen with that format
        return f'{self.title} | {self.ects} ECTS | {self.capacity} Capacity'
