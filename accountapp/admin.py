from django.contrib import admin
from .models import CustomUser, Student, Teacher, StudentLesson

# Register your models here.


class StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'department_of_student', 'student_ects']


admin.site.register(CustomUser)
admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher)
admin.site.register(StudentLesson)
