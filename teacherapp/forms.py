from accountapp.models import Student
from baseapp.models import Lesson
from django import forms


class StudentLessonForm(forms.ModelForm):
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
        if not student_lessons:
            raise forms.ValidationError(
                'You have to select at least one lesson.')

        for lesson in student_lessons:
            if lesson.capacity == 0:
                raise forms.ValidationError(
                    f'Course capacity is full: {lesson.title}')

    def course_hour_check(self, student_lessons):  # Course hour check
        course_hour_set = set()
        for lesson in student_lessons:
            if lesson.course_hour in course_hour_set:
                raise forms.ValidationError(
                    f'Course hour conflict: {lesson.course_hour}')
            course_hour_set.add(lesson.course_hour)

    def clean(self):
        cleaned_data = super().clean()
        student_lessons = self.cleaned_data.get('student_lessons')
        self.ects_check(student_lessons)
        self.capacity_check(student_lessons)
        self.course_hour_check(student_lessons)

        return cleaned_data
