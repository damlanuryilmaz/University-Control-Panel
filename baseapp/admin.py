from django.contrib import admin
from .models import Lesson, Department, CourseHour

# Register your models here.


class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'ects', 'course_hour']
    list_filter = ['category']
    search_fields = ['title']


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'capacity',]
    search_fields = ['title']


admin.site.register(Lesson, LessonAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(CourseHour)
