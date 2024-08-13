from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from .models import Student, Teacher, Contact, Grade
from baseapp.models import Lesson, Department
from teacherapp.models import CustomUser


class GradeView(LoginRequiredMixin, View):
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

        return redirect('grade')


class SyllabusView(LoginRequiredMixin, View):
    def get(self, request):

        try:
            student = Student.objects.get(user__username=request.user.username)
            department_ects = Department.objects.get(
                title=student.department_of_student
            ).capacity

        except Student.DoesNotExist:
            student = None
            department_ects = None

        user = CustomUser.objects.get(username=request.user.username)
        grades = Grade.objects.filter(student=student) if student else None
        print(grades)

        context = {
            'student': student,
            'user': user,
            'department_ects': department_ects,
            'grades': grades,
        }
        return render(request, "teacherapp/syllabus.html", context)

    def post(request):

        student = Student.objects.get(user__username=request.user.username)
        user = CustomUser.objects.get(username=request.user.username)
        department_ects = Department.objects.get(
            title=student.department_of_student
        ).capacity

        selected_lesson = request.POST.getlist("lesson_selected")

        total_ects = 0

        for lesson in selected_lesson:
            lesson = Lesson.objects.get(title=lesson)
            total_ects += lesson.ects

        if total_ects > department_ects:
            context = {
                "syllabus": Lesson.objects.filter(
                    category=student.department_of_student),
                "student": student,
                "user": user,
                "department_ects": Department.objects.get(
                    title=student.department_of_student
                ).capacity,
                "error": "You have to select lessons according to your department capacity",
            }

            return render(request, "teacherapp/syllabus.html", context)

        for lesson_title in selected_lesson:
            lesson = Lesson.objects.get(title=lesson_title)
            if lesson.capacity == 0:
                failed_lesson = Lesson.objects.filter(
                    category=student.department_of_student
                )
                context = {
                    "syllabus": Lesson.objects.filter(
                        category=student.department_of_student
                    ),
                    "student": student,
                    "user": user,
                    "department_ects": Department.objects.get(
                        title=student.department_of_student
                    ).capacity,
                    "failed_lessons": failed_lesson,
                    "error": "Course capacity is full",
                }

                return render(request, "teacherapp/syllabus.html", context)

        # Save each lesson to the student's lesson list
        for lesson_title in selected_lesson:
            lesson = Lesson.objects.get(title=lesson_title)

            lesson.capacity -= 1
            lesson.save()

            student.student_lessons.add(lesson)
            student.save()

        student.student_ects = total_ects
        student.save()

        return redirect("syllabus")


class ContactView(LoginRequiredMixin, View):
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
