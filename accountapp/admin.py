from django.contrib import admin
from .models import CustomUser, Student, Teacher, StudentLesson


class StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'department', 'acts', 'adviser']


admin.site.register(CustomUser)
admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher)
admin.site.register(StudentLesson)
