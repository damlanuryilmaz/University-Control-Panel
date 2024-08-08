from django.db import models
from django.utils.text import slugify

# Create your models here.


class Department(models.Model):
    title = models.CharField(max_length=150)
    capacity = models.IntegerField(default=10)
    slug = models.SlugField(db_index=True, unique=True,
                            blank=True, null=False, editable=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Department, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=100)
    ects = models.IntegerField()
    category = models.ManyToManyField(Department)
    capacity = models.IntegerField(default=3)

    def __str__(self):
        return self.title


class Note(models.Model):
    lesson_name = models.CharField(max_length=150)
    ects = models.IntegerField()
    grade = models.CharField(max_length=10)

    def __str__(self):
        return self.title


