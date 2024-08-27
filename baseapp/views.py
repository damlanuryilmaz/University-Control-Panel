from accountapp.models import CustomUser, Student, Teacher
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from .models import Department, Lesson
from .forms import PhotoUploadForm
from django.views import View


class IndexView(LoginRequiredMixin, View):  # Main page
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
                teacher.lessons.all() if teacher else None
            ),
        }

        return render(request, 'baseapp/index.html', context)


class DepartmentView(LoginRequiredMixin, View):  # Select the department
    def get(self, request):
        context = {
            'departments': Department.objects.all(),
        }
        return render(request, 'baseapp/department.html', context)

    def post(self, request,):

        slug = request.POST.get('slug')
        # Get the slug of the department to send the lesson page
        return redirect('lesson', slug=slug)


class LessonView(LoginRequiredMixin, View):
    # Show the lessons of the department
    def get(self, request, slug):
        context = {
            'lessons': Lesson.objects.filter(category__slug=slug),
            # Get the lessons of the department with the slug
            'all_lessons': Lesson.objects.all(),
            'departments': Department.objects.get(slug=slug),
        }
        return render(request, 'baseapp/lesson.html', context)


class DepartmentRequestView(LoginRequiredMixin, View):
    # Send a request to any teacher

    def post(self, request):
        student = Student.objects.get(user__username=request.user.username)
        student.department_request = True
        student.save()

        return redirect('index')


class UploadPhotoView(LoginRequiredMixin, View):

    def post(self, request):
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            user = CustomUser.objects.get(username=request.user.username)
            user.photo = form.cleaned_data['photo']
            user.save()
            return redirect('index')
        return render(request, 'baseapp/upload_photo.html', {'form': form})
