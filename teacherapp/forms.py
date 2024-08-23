from accountapp.models import Student
from baseapp.models import Lesson
from django import forms


# class AddLessonForm(forms.ModelForm):
#     class Meta:
#         model = StudentLesson
#         fields = ['lesson']

#     lesson = forms.ModelChoiceField(
#         queryset=Lesson.objects.all(), widget=forms.HiddenInput())


# class SubmitLessonForm(forms.Form):
#     confirm = forms.BooleanField(label='Send Your Adviser', required=True)


class AddLessonForm(forms.ModelForm):
    # Form for students to select lessons
    class Meta:
        # Subclass of ModelForm
        model = Student
        fields = ['student_lessons']
        widgets = {
            'student_lessons': forms.CheckboxSelectMultiple,
        }
        labels = {
            'student_lessons': 'Select Lessons:',
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # Used super() cus py3 allowed

        if self.user:
            student = Student.objects.get(user=self.user)
            self.fields['student_lessons'].queryset = Lesson.objects.filter(
                category=student.department_of_student)
            # Update widget attribute to data attr (lesson name)

    def clean(self):
        cleaned_data = super().clean()
        student_lessons = self.cleaned_data.get('student_lessons')
        self.ects_check(student_lessons)
        self.capacity_check(student_lessons)
        self.course_hour_check(student_lessons)

        return cleaned_data

    def capacity_check(self, student_lessons):  # Department capacity check
        student = Student.objects.get(user=self.user)
        total_ects = 0
        department_capacity = student.department_of_student.capacity

        for lesson in student_lessons:
            total_ects += lesson.ects

        if total_ects > department_capacity:
            raise forms.ValidationError(
                f'You have selected {total_ects} ECTS!')

        self.total_ects = total_ects

    def ects_check(self, student_lessons):  # Course capacity check

        for lesson in student_lessons:
            if lesson.capacity == 0:
                raise forms.ValidationError(
                    f'Course capacity is full: {lesson.title}')

    def course_hour_check(self, student_lessons):  # Course hour check
        course_week_set = set()
        course_hour_set = set()
        for lesson in student_lessons:
            if lesson.day_of_week in course_week_set:
                raise forms.ValidationError(
                    f'Course hour conflict: {lesson.day_of_week} '
                    f'{lesson.start_time} - {lesson.end_time}')
            if lesson.start_time in course_hour_set:
                raise forms.ValidationError(
                    f'Course hour conflict: {lesson.day_of_week} '
                    f'{lesson.start_time} - {lesson.end_time}')
            course_week_set.add(lesson.day_of_week)
            course_hour_set.add(lesson.start_time)
