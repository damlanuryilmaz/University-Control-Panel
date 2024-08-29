from accountapp.models import CustomUser, Student, Teacher
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from .models import Department, Lesson
from .forms import PhotoUploadForm
from django.views import View


class IndexView(LoginRequiredMixin, View):  # Main page
    def get(self, request):

        user = CustomUser.objects.get(username=request.user.username)

        if user.status == 'Student':
            student = Student.objects.get(user=request.user)
            students_without_department = Student.objects.filter(
                department_request=True)
            form = PhotoUploadForm()

            context = {
                'user': user,
                'form': form,
                'student': student,
                'students_without_department': students_without_department,
            }
            return render(request, 'baseapp/index.html', context)

        elif user.status == 'Teacher':
            teacher = Teacher.objects.get(user=request.user)
            context = {
                'user': user,
                'teacher': teacher,
                'lessons': teacher.lessons.all(),
            }
            return render(request, 'baseapp/index.html', context)

        elif user.status == 'Admin':
            context = {
                'user': user,
            }
            return render(request, 'baseapp/index.html', context)

        return render(request, 'accountapp/login.html')


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
            'lessons': Lesson.objects.filter(department__slug=slug),
            # Get the lessons of the department with the slug
            'all_lessons': Lesson.objects.all(),
            'departments': Department.objects.get(slug=slug),
        }
        return render(request, 'baseapp/department_lessons.html', context)


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
            student = Student.objects.get(user=request.user)
            student.profile_photo = form.cleaned_data['profile_photo']
            student.save()
            return redirect('index')

        return render(request, 'baseapp/upload_photo.html')
