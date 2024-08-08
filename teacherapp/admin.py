from django.contrib import admin
from .models import *

# Register your models here.


admin.site.register(CustomUser)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Contact)
