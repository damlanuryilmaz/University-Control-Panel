from .forms import DepartmentRequestForm, AssignAdviserForm
from django.contrib.auth.mixins import LoginRequiredMixin
from accountapp.models import Student, Teacher
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.views import View


class DepartmentRequest(LoginRequiredMixin, View):
    def get(self, request):
        students_list = Student.objects.filter(department_request=True)
        paginator = Paginator(students_list, 10)
        page_number = request.GET.get('page')
        students = paginator.get_page(page_number)
        form = DepartmentRequestForm()

        context = {
            'form': form,
            'students': students,
        }

        return render(
            request,
            "adminapp/department_request.html",
            context
        )

    def post(self, request):

        form = DepartmentRequestForm(request.POST)

        if form.is_valid():
            student_id = request.POST.get('student')
            student = Student.objects.get(id=student_id)
            student.department = form.cleaned_data[
                'department']
            student.department_request = False
            student.save()
            return redirect('department_request')

        else:
            students = Student.objects.filter(department_request=True)

            context = {
                'students': students,
                'form': form
            }
            return render(request,
                          "adminapp/department_request.html",
                          context)


class AssignAdviser(LoginRequiredMixin, View):
    def get(self, request):
        students_wo_adviser_list = Student.objects.filter(adviser=None)
        paginator = Paginator(students_wo_adviser_list, 10)
        page_number = request.GET.get('page')
        students_wo_adviser = paginator.get_page(page_number)
        form = AssignAdviserForm()
        teachers = Teacher.objects.all()

        context = {
            'students_wo_adviser': students_wo_adviser,
            'form': form,
            'teacher': teachers,
        }

        return render(
            request,
            "adminapp/assign_adviser.html",
            context
        )

    def post(self, request):
        form = AssignAdviserForm(request.POST)

        if form.is_valid():
            student_id = request.POST.get('student')
            student = Student.objects.get(id=student_id)
            student.adviser = form.cleaned_data['adviser']
            student.save()

        return redirect('assign_adviser')
