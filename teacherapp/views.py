from accountapp.models import CustomUser, Student, Teacher
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from .forms import StudentLessonForm
from .models import Contact, Grade
from baseapp.models import Lesson
from django.views import View


class GradeView(LoginRequiredMixin, View):  # For teachers to assign grades
    def get(self, request):

        teacher = Teacher.objects.get(user__username=request.user.username)
        lessons = teacher.lesson_of_teacher.all()
        grade_types = Grade.GRADE_TYPE
        students = Student.objects.all()
        grades = Grade.objects.all()

        context = {
            "students": students,
            "lessons": lessons,
            "grade_types": grade_types,
            "grades": grades,
        }

        return render(request, "teacherapp/grade.html", context)

    def post(self, request):

        lesson_id = request.POST.get('lesson')
        student_id = request.POST.get('student')
        grade_value = request.POST.get('grade')
        student = Student.objects.get(id=student_id)
        lesson = Lesson.objects.get(id=lesson_id)
        Grade.objects.update_or_create(student=student, lesson=lesson,
                                       defaults={'grade': grade_value})
        # Update_or_create cus it's possible to change the grade

        return redirect('grade')


class SyllabusView(LoginRequiredMixin, View):
    def get(self, request):
        student = Student.objects.get(user=request.user)
        form = StudentLessonForm(user=request.user)
        grades = Grade.objects.filter(student=student)

        try:
            department_capacity = student.department_of_student.capacity
        except AttributeError:
            department_capacity = None  # If student has no department

        context = {
            'form': form,
            'student': student,
            'department_capacity': department_capacity,
            'grades': grades,
        }
        return render(request, "teacherapp/syllabus.html", context)

    def post(self, request):

        student = Student.objects.get(user=request.user)
        form = StudentLessonForm(request.POST, user=request.user)

        if form.is_valid():
            student.student_ects = form.total_ects
            # Assign total ECTS to student
            student.save()

            for lesson in form.cleaned_data['student_lessons']:
                student.student_lessons.add(lesson)
                # Add selected lessons to student
                lesson.capacity -= 1
                # Decrease the capacity of the lesson
                lesson.save()

            return redirect('syllabus')

        context = {
            'form': form,
            'student': student,
        }

        return render(request, "teacherapp/syllabus.html", context)


class ContactView(LoginRequiredMixin, View):
    # Send the message to the teacher
    def get(self, request):

        context = {
            "teachers": CustomUser.objects.filter(status="Teacher"),
        }
        return render(request, "teacherapp/contact.html", context)

    def post(self, request):

        message_of_student = Student.objects.get(
            user__username=request.user.username)
        teacher_username = request.POST.get("teacher_select")
        message = request.POST.get("message")

        if not message:
            # Check if the message box is empty
            context = {
                "teachers": CustomUser.objects.filter(status="Teacher"),
                "error": "Please enter a message.",
            }
            return render(request, "teacherapp/contact.html", context)

        Contact.objects.create(
            message=message,
            message_of_student=message_of_student,
            message_of_teacher=CustomUser.objects.get(
                username=teacher_username),
        )

        return redirect("index")


class MessageView(LoginRequiredMixin, View):
    # Show the messages that the teacher received
    def get(self, request):

        context = {
            "messages": Contact.objects.filter(
                message_of_teacher=request.user.id),
            "user": CustomUser.objects.get(username=request.user.username),
        }

        return render(request, "teacherapp/message.html", context)


class DeleteMessageView(LoginRequiredMixin, View):
    def post(self, request, id):
        message = Contact.objects.get(id=id)
        message.delete()
        return redirect("message")
