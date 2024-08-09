# Import the render and redirect functions from django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View  # Import the View class from django
# Import the Lesson model from the models.py file
from .models import *
from teacherapp.models import CustomUser, Student, Teacher

# Create class-based view of index page


class IndexView(LoginRequiredMixin, View):
    def get(self, request):

        user = CustomUser.objects.get(username=request.user.username)

        try:
            teacher = Teacher.objects.get(user__username=request.user.username)
        except:
            teacher = None

        try:
            student = Student.objects.get(user__username=request.user.username)
        except:
            student = None

        context = {
            'user': user,
            'student': student,
            'teacher': teacher,
            'lessons': teacher.lesson_of_teacher.all() if teacher else None,
        }

        return render(request, 'baseapp/index.html', context)


class DepartmentView(LoginRequiredMixin, View):
    def get(self, request):
        context = {
            'departments': Department.objects.all(),
        }
        return render(request, 'baseapp/department.html', context)

    def post(self, request,):

        slug = request.POST.get('slug')
        return redirect('lesson', slug=slug)


class LessonView(LoginRequiredMixin, View):
    def get(self, request, slug):
        context = {
            'lessons': Lesson.objects.filter(category__slug=slug),
            'all_lessons': Lesson.objects.all(),
            'departments': Department.objects.get(slug=slug),
        }
        return render(request, 'baseapp/lesson.html', context)

