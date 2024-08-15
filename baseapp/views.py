from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from .models import Department, Lesson
from accountapp.models import CustomUser, Student, Teacher


class IndexView(LoginRequiredMixin, View):
    def get(self, request):

        user = CustomUser.objects.get(username=request.user.username)
        students_without_department = Student.objects.filter(
            department_request=True)

        try:
            teacher = Teacher.objects.get(user__username=request.user.username)
        except Teacher.DoesNotExist:
            teacher = None

        try:
            student = Student.objects.get(user__username=request.user.username)
        except Student.DoesNotExist:
            student = None

        context = {
                'user': user,
                'student': student,
                'teacher': teacher,
                'students_without_department': students_without_department,
                'departments': Department.objects.all(),
                'lessons': (
                    teacher.lesson_of_teacher.all() if teacher else None
                ),
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


class DepartmentRequestView(LoginRequiredMixin, View):

    def post(self, request):

        student = Student.objects.get(user__username=request.user.username)
        student.department_request = True
        student.save()

        return redirect('index')


class AssignDepartmentView(LoginRequiredMixin, View):

    def post(self, request):

        username = request.POST.get('username')
        department_id = request.POST.get('department')
        department = Department.objects.get(id=department_id)
        student = Student.objects.get(user__username=username)
        student.department_of_student = department
        student.department_request = False
        student.save()

        return redirect('index',)
