from accountapp.models import CustomUser, Student, Teacher, StudentLesson
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Contact, Grade
from baseapp.models import Lesson
from .forms import AddLessonForm
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


# class LessonSelectionView(LoginRequiredMixin, View):
#     # For students to select lessons
#     template_name = "teacherapp/lesson_select.html"

#     def get(self, request):
#         student = Student.objects.get(user=request.user)
#         lessons = Lesson.objects.filter(
    # category=student.department_of_student)
#         selected_lessons = (
#             StudentLesson.objects
#             .filter(students=student)
#             .select_related('lessons')
#         )

#         context = {
#             'lessons': lessons,
#             'selected_lessons': selected_lessons,
#             'addlessonform': AddLessonForm(),
#         }

#         return render(request, self.template_name, context)

#     def post(self, request):
#         student = Student.objects.get(user=request.user)
#         form = AddLessonForm(request.POST)

#         if form.is_valid():
#             lesson = form.cleaned_data['lesson']
#             StudentLesson.objects.create(student=student, lesson=lesson)

#             if not StudentLesson.objects.filter(
#                 student=student,
#                 lesson=lesson
#             ).exists():
#                 StudentLesson.objects.create(student=student, lesson=lesson)
#                 return JsonResponse(
#                     {'success': True, 'message':
# 'Lesson added successfully.'})
#             else:
#                 return JsonResponse(
#                     {'success': False, 'message': 'Lesson already added.'})

#         return JsonResponse({
#             'success': False,
#             'message': 'Invalid data submitted.'
#         })


# class RemoveLessonView(LoginRequiredMixin, View):
#     # Delete unchecked lessons
#     def post(self, request):
#         lesson_id = request.POST.get('lesson_id')
#         student = Student.objects.get(user=request.user)

#         lesson = Lesson.objects.get(id=lesson_id)
#         StudentLesson.objects.filter(students=student,
# lessons=lesson).delete()

#         return JsonResponse({
#             'success': True,
#             'message': 'Lesson removed successfully.'
#         })


# class SubmitLessonsView(View):
#     template_name = 'submit_lessons.html'

#     def get(self, request):
#         form = SubmitLessonForm()

#         context = {
#             'form': form,
#         }

#         return render(request, self.template_name, context)

#     def post(self, request):
#         form = SubmitLessonForm(request.POST)

#         if form.is_valid() and form.cleaned_data['confirm']:
#             student = Student.objects.get(user=request.user)
#             student.department_request = True
#             student.save()

#             return redirect('index')

#         context = {
#             'form': form,
#         }

#         return render(request, self.template_name, context)


# For students to select lessons
class LessonSelectionView(LoginRequiredMixin, View):
    def get(self, request):

        student = Student.objects.get(user=request.user)
        form = AddLessonForm(user=request.user)

        if student.department_of_student:
            department_capacity = student.department_of_student.capacity
            selected_lessons = student.student_lessons.all()

            context = {
                'form': form,
                'student': student,
                'department_capacity': department_capacity,
                'selected_lessons': selected_lessons,
            }

            return render(request, "teacherapp/lesson_select.html", context)

        else:
            context = {
                'form': form,
                'student': student,
            }

            return render(request, "teacherapp/lesson_select.html", context)

    def post(self, request, *args, **kwargs):

        form = AddLessonForm(request.POST, user=request.user)

        if form.is_valid():
            student = Student.objects.get(user=request.user)

            lessons = form.cleaned_data['student_lessons']
            student.student_ects = form.total_ects
            # Assign total ECTS to student
            student.save()

            new_lessons = set(lessons.values_list('id', flat=True))
            existing_lessons = set(StudentLesson.objects.filter(
                students=student).values_list('lessons_id', flat=True))

            to_add = new_lessons - existing_lessons
            to_remove = existing_lessons - new_lessons

            for lesson_id in to_add:
                lesson = Lesson.objects.get(id=lesson_id)
                StudentLesson.objects.create(
                    students=student, lessons=lesson)

            for lesson_id in to_remove:
                StudentLesson.objects.filter(
                    students=student, lessons_id=lesson_id).delete()

            selected_lesson_names = [
                lesson.title for lesson in lessons]

            return JsonResponse({'status': 'success',
                                 'selected_lessons': selected_lesson_names})

        return JsonResponse(
            {'status': 'error', 'errors': form.errors}, status=400)

        # context = {
        #     'form': form,
        #     'student': student,
        #     'department_capacity': student.department_of_student.capacity,
        # }

        # return render(request, "teacherapp/lesson_select.html", context)

    # def handle_lesson_selection(self, request):
    #     # Using JS to add and delete lesson
    #     student = Student.objects.get(user=request.user)
    #     lesson_id = request.POST.get('lesson_id')
    #     action = request.POST.get('action')

    #     if lesson_id and action:
    #         lesson = Lesson.objects.get(id=lesson_id)

    #         if action == 'add':
    #             student.student_lessons.add(lesson)
    #             lesson.capacity -= 1
    #             lesson.save()
    #         elif action == 'remove':
    #             student.student_lessons.remove(lesson)
    #             lesson.capacity += 1
    #             lesson.save()

    #         student.save()

    #         return JsonResponse({'status': 'success'})
    #     return JsonResponse({'status': 'error'}, status=400)


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
