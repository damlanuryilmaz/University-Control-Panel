from accountapp.models import CustomUser, Student, StudentLesson, Teacher
from sklearn.preprocessing import OrdinalEncoder, LabelEncoder
from .forms import AddLessonForm, GradeForm, FutureCareerForm
from django.contrib.auth.mixins import LoginRequiredMixin
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from .models import Contact, Grade, CareerSuggestion
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from sklearn.metrics import accuracy_score
from django.http import JsonResponse
from django.contrib import messages
from baseapp.models import Lesson
from django.views import View
import pandas as pd
import joblib


class GradeView(LoginRequiredMixin, View):  # For teachers to assign grades
    def get(self, request, slug):

        lesson = Lesson.objects.get(slug=slug)

        studentlessons = StudentLesson.objects.filter(lessons=lesson)
        students_list = []
        grade = None
        for studentlesson in studentlessons:
            student = studentlesson.students
            grade = Grade.objects.filter(
                student=student, lesson=lesson).first()
            student.grade = grade.grade if grade else None
            students_list.append(student)

        students_list.sort(key=lambda student: student.user.first_name)

        paginator = Paginator(students_list, 10)
        page_number = request.GET.get('page')
        students = paginator.get_page(page_number)
        form = GradeForm()

        context = {
            'students': students,
            'lesson': lesson,
            'form': form,
            'grade': grade,
        }

        return render(request, 'teacherapp/teacher_grading.html', context)

    def post(self, request, slug):
        student_id = request.POST.get('student')
        lesson_id = request.POST.get('lesson')
        grade_value = request.POST.get('grade')

        try:
            grade, created = Grade.objects.update_or_create(
                student_id=student_id,
                lesson_id=lesson_id,
                defaults={'grade': grade_value}
            )
            if created:
                message = "Grade assigned successfully."
            else:
                message = "Grade updated successfully."

            return JsonResponse({
                'success': True,
                'message': message,
                'updated_grade': grade_value})

        except Exception as e:
            return JsonResponse(
                {'success': False, 'error': str(e)}, status=400)


# For students to select lessons
class LessonSelectionView(LoginRequiredMixin, View):
    def get(self, request):

        student = Student.objects.get(user=request.user)
        form = AddLessonForm(user=request.user)

        if student.department:
            department_capacity = student.department.capacity
            selected_lessons = student.lessons.all()

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

    def post(self, request):

        form = AddLessonForm(request.POST, user=request.user)

        if form.is_valid():
            student = Student.objects.get(user=request.user)

            lessons = form.cleaned_data['lessons']
            student.acts = form.total_acts

            # Assign total ECTS to student
            student.save()

            new_lessons = set(lessons.values_list('id', flat=True))
            existing_lessons = set(StudentLesson.objects.filter(
                students=student).values_list('lessons_id', flat=True))

            to_add = new_lessons - existing_lessons
            to_remove = existing_lessons - new_lessons

            updated_lessons = []
            for lesson_id in to_add:
                lesson = Lesson.objects.get(id=lesson_id)
                if lesson.capacity > 0:
                    lesson.capacity -= 1
                    lesson.save()
                    StudentLesson.objects.create(
                        students=student,
                        lessons=lesson)
                else:
                    return JsonResponse({
                        'success': False,
                        'message': f'Course capacity is full: {lesson.title}'
                    }, status=400)
                updated_lessons.append({
                    'id': lesson.id,
                    'title': lesson.title,
                    'capacity': lesson.capacity
                })

            for lesson_id in to_remove:
                lesson = Lesson.objects.get(id=lesson_id)
                lesson.capacity += 1
                lesson.save()
                StudentLesson.objects.filter(
                    students=student, lessons_id=lesson_id).delete()
                updated_lessons.append({
                    'id': lesson.id,
                    'title': lesson.title,
                    'capacity': lesson.capacity})

            selected_lessons = [{
                'id': lesson.id,
                'title': lesson.title,
                'day_of_week': lesson.day_of_week,
                'start_time': lesson.start_time.strftime('%H:%M')
            } for lesson in lessons]

            context = {'success': True,
                       'selected_lessons': selected_lessons,
                       'updated_lessons': updated_lessons,
                       }

            return JsonResponse(context)

        return JsonResponse(
            {'success': False, 'errors': form.errors}, status=400)


class UpdateCapacityView(LoginRequiredMixin, View):
    def get(self, request):
        student = Student.objects.get(user=request.user)
        lessons = Lesson.objects.filter(department=student.department)

        updated_lessons = [
            {"id": lesson.id, "capacity": lesson.capacity}
            for lesson in lessons
        ]
        return JsonResponse({"updated_lessons": updated_lessons})


class UpdateWeekTableView(LoginRequiredMixin, View):
    def get(self, request):
        student = Student.objects.get(user=request.user)
        lessons = student.lessons.all()

        lessons_data = [{
            'id': lesson.id,
            'title': lesson.title,
            'day_of_week': lesson.day_of_week,
            'start_time': lesson.start_time.strftime('%H:%M'),
        }
            for lesson in lessons]

        return JsonResponse({'lessons': lessons_data})


class SubmitLessonsView(View):
    def post(self, request):

        student = Student.objects.get(user=request.user)
        student.is_submitted = True
        student.save()

        return redirect('selected_lessons')


class LessonSelectView(LoginRequiredMixin, View):
    def get(self, request):
        student = Student.objects.get(user=request.user)
        lessons = student.lessons.all()
        grades = Grade.objects.filter(student=student)

        context = {
            'grades': grades,
            'student': student,
            'lessons': lessons,
        }

        return render(request, "teacherapp/selected_lessons.html", context)


class SendMessageView(LoginRequiredMixin, View):
    # Send the message to the teacher
    def get(self, request):

        context = {
            "teachers": CustomUser.objects.filter(status="Teacher"),
        }
        return render(
            request,
            "teacherapp/message_to_teacher.html",
            context
        )

    def post(self, request):

        student = Student.objects.get(
            user__username=request.user.username)
        teacher_username = request.POST.get("teacher_select")
        message = request.POST.get("message")

        if not message:
            # Check if the message box is empty
            context = {
                "teachers": CustomUser.objects.filter(status="Teacher"),
                "error": "Please enter a message.",
            }
            return render(
                request,
                "teacherapp/message_to_teacher.html",
                context
            )

        Contact.objects.create(
            message=message,
            student=student,
            teacher=CustomUser.objects.get(
                username=teacher_username),
        )

        messages.success(request, "Your message has been sent successfully.")
        return redirect("send_message")


class MessageView(LoginRequiredMixin, View):
    # Show the messages that the teacher received
    def get(self, request):
        messages_list = Contact.objects.filter(
            teacher=request.user.id)
        paginator = Paginator(messages_list, 5)
        page_number = request.GET.get('page')
        messages_from_student = paginator.get_page(page_number)

        context = {
            "messages_from_student": messages_from_student,
            "user": CustomUser.objects.get(username=request.user.username),
        }

        return render(request, "teacherapp/teacher_messages.html", context)


class DeleteMessageView(LoginRequiredMixin, View):
    def post(self, request, id):
        message = Contact.objects.get(id=id)
        message.delete()
        messages.success(request, "The message has been deleted successfully.")
        return redirect("message")


class CourseApprovalView(LoginRequiredMixin, View):
    def get(self, request):
        adviser = Teacher.objects.get(user=request.user)
        lesson_list = StudentLesson.objects.all()
        selected_letter = request.GET.get('letter', '')
        students = Student.objects.filter(
            is_submitted=True,
            adviser=adviser,
            user__first_name__istartswith=selected_letter
        ).order_by('user__first_name')

        context = {
            'students': students,
            'lessons': lesson_list,
            'selected_letter': selected_letter,
        }
        return render(request, "teacherapp/course_approval.html", context)

    def post(self, request):
        student_id = request.POST.get('student')
        student = Student.objects.get(id=student_id)
        StudentLesson.objects.delete(students=student)
        student.is_approved = True
        student.acts = 0

        student.save()

        return JsonResponse({'success': True})


class StudentFutureView(View):
    def get(self, request):

        return render(request, 'teacherapp/student_future.html')


# class StudentFutureView(View):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         # Define columns for encoding
#         self.ordinal_columns = ['python', 'java', 'sql']
#         self.one_hot_columns = ['interested_domain', 'project']

#     def get(self, request):
#         df = self.get_student_data()
#         df = self.encode_features(df)

#         accuracy = self.perform_model(df)
#         self.save_model()

#         form = FutureCareerForm()
#         print("Accuracy:", accuracy)

#         context = {
#             'form': form,
#         }

#         return render(request, 'teacherapp/student_future.html', context)

#     def get_student_data(self):
#         data = StudentCareer.objects.all().values()
#         df = pd.DataFrame(data)

#         return df

#     def encode_features(self, df):
#         # Columns to be ordinal encoded
#         categories = (
#             [['Weak', 'Average', 'Strong']] *
#             len(self.ordinal_columns)
#         )

#         # Assign the ordinal columns to the ordinal encoder
#         self.ordinal_encoder = OrdinalEncoder(categories=categories)
#         df[self.ordinal_columns] = self.ordinal_encoder.fit_transform(
#             df[self.ordinal_columns])

#         # One-hot encoding using pd.get_dummies
#         df = pd.get_dummies(df, columns=self.one_hot_columns)

#         # Label encode the target variable
#         self.label_encoder = LabelEncoder()
#         df['future_career'] = self.label_encoder.fit_transform(
#             df['future_career'])

#         return df

#     def perform_model(self, df):
#         X = df.drop('future_career', axis=1)  # Features
#         Y = df['future_career']               # Target variable

#         X_train, X_test, y_train, y_test = train_test_split(
#             X, Y, test_size=0.2, random_state=42)

#         # Initializing the model
#         self.model = RandomForestClassifier()
#         self.model.fit(X_train, y_train)

#         # Making predictions on the test set
#         y_pred = self.model.predict(X_test)

#         # Evaluating the model's performance
#         accuracy = accuracy_score(y_test, y_pred)
#         # print(f'Accuracy: {accuracy:.4f}')
#         # print(classification_report(y_test, y_pred, zero_division=0))

#         return accuracy

#     def save_model(self):
#         joblib.dump(self.model, 'random_forest_model.pkl')
#         joblib.dump(self.ordinal_encoder, 'ordinal_encoder.pkl')
#         joblib.dump(self.label_encoder, 'label_encoder.pkl')

#     def post(self, request):
#         # Load the saved model and encoders using joblib
#         model = joblib.load('random_forest_model.pkl')
#         ordinal_encoder = joblib.load('ordinal_encoder.pkl')
#         label_encoder = joblib.load('label_encoder.pkl')

#         form = FutureCareerForm(request.POST)
#         if form.is_valid():

#             # Gettings the form data
#             projects = form.cleaned_data['projects']
#             interest_domain = form.cleaned_data['interest_domain']
#             python = form.cleaned_data['python']
#             sql = form.cleaned_data['sql']
#             java = form.cleaned_data['java']

#             # Prepare the form data for prediction
#             form_data = {
#                 'interested_domain': ','.join(interest_domain),
#                 'project': ','.join(projects),
#                 'python': python,
#                 'sql': sql,
#                 'java': java
#             }

#             df_input = pd.DataFrame([form_data])

#             df_input[self.ordinal_columns] = ordinal_encoder.transform(
#                 df_input[self.ordinal_columns])
#             df_input = pd.get_dummies(df_input, columns=self.one_hot_columns)

#             # Recompute columns based on the training data
#             df_train = self.get_student_data()  # Get training data
#             df_train = self.encode_features(df_train)
#             model_columns = df_train.drop(
#                 'future_career', axis=1).columns.tolist()

#             # Align columns with the training data
#             missing_cols = set(model_columns) - set(df_input.columns)
#             for col in missing_cols:
#                 df_input[col] = 0
#             df_input = df_input[model_columns]

#             # Make prediction
#             prediction = model.predict(df_input)
#             predicted_career = label_encoder.inverse_transform(prediction)[0]
#             print(self.perform_model(df_train))

#             context = {
#                 'form': form,
#                 'predicted_career': predicted_career,
#                 'accuracy': self.perform_model(df_train),
#             }

#             return render(request, 'teacherapp/student_future.html', context)

#         context = {
#             'form': form,
#         }

#         return render(request, 'teacherapp/student_future.html', context)

# class FutureStudentView(View):
#     # Show the students without department
#     def get(self, request):

#         data = StudentCareer.objects.all().values()
#         df = pd.DataFrame(data)

#         # Columns to be ordinal encoded
#         ordinal_columns = ['python', 'java', 'sql']
#         categories = [['Weak', 'Average', 'Strong']] * len(ordinal_columns)

#         # Assign the ordinal columns to the ordinal encoder
#         ordinal_encoder = OrdinalEncoder(categories=categories)
#         df[ordinal_columns] = ordinal_encoder.fit_transform(
#             df[ordinal_columns]
#         )

#         # One-hot encoding using pd.get_dummies
#         one_hot_columns = ['interested_domain', 'project']
#         df = pd.get_dummies(df, columns=one_hot_columns)

#         label_encoder = LabelEncoder()
#         df['future_career'] = label_encoder.fit_transform(df['future_career'])

#         X = df.drop('future_career', axis=1)  # Features
#         Y = df['future_career']               # Target variable

#         X_train, X_test, y_train, y_test = train_test_split(
#             X, Y, test_size=0.20, random_state=42)

#         # Initializing the model
#         model = RandomForestClassifier()
#         model.fit(X_train, y_train)

#         # Making predictions on the test set
#         y_pred = model.predict(X_test)

#         # Evaluating the model's performance
#         print("Accuracy:", accuracy_score(y_test, y_pred))
#         print(classification_report(y_test, y_pred, zero_division=0))

#         joblib.dump(model, 'random_forest_model.pkl')
#         joblib.dump(ordinal_encoder, 'ordinal_encoder.pkl')
#         joblib.dump(label_encoder, 'label_encoder.pkl')

#         # form = FutureCareerForm()

#         context = {

#         }

#         return render(request, 'teacherapp/student_future.html', context)

#     def post(self, request):
#         # Load the saved model and encoders using pickle
#         model = joblib.load('random_forest_model.pkl')
#         ordinal_encoder = joblib.load('ordinal_encoder.pkl')
#         label_encoder = joblib.load('label_encoder.pkl')
