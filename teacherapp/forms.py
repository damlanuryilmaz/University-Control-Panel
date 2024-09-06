from crispy_forms.layout import Layout, Field, HTML
from teacherapp.models import Grade, CareerSuggestion
from crispy_forms.helper import FormHelper
from accountapp.models import Student
from baseapp.models import Lesson
from django import forms


class AddLessonForm(forms.ModelForm):
    # Form for students to select lessons
    class Meta:
        # Subclass of ModelForm
        model = Student
        fields = ['lessons']
        widgets = {
            'lessons': forms.CheckboxSelectMultiple,
        }
        labels = {
            'lessons': 'Select Lessons:',
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # Used super() cus py3 allowed

        if self.user:
            student = Student.objects.get(user=self.user)
            self.fields['lessons'].queryset = Lesson.objects.filter(
                department=student.department)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('lessons', wrapper_class='form-group row',
                  css_class='form-check-input'),
            HTML('<div class="error-message"></div>')
        )

    def clean(self):
        cleaned_data = super().clean()
        lessons = self.cleaned_data.get('lessons')
        self.capacity_check(lessons)
        self.course_hour_check(lessons)

        return cleaned_data

    def capacity_check(self, lessons):  # Department capacity check
        student = Student.objects.get(user=self.user)
        total_acts = 0
        department_capacity = student.department.capacity

        for lesson in lessons:
            total_acts += lesson.ects

        if total_acts > department_capacity:
            raise forms.ValidationError(
                f'You have selected {total_acts} ECTS!')

        self.total_acts = total_acts

    def course_hour_check(self, lessons):  # Course hour check
        course_week_set = set()
        course_hour_set = set()
        for lesson in lessons:
            if lesson.day_of_week in course_week_set:
                if lesson.start_time in course_hour_set:
                    raise forms.ValidationError(
                        f'Course hour conflict: {lesson.day_of_week} '
                        f'{lesson.start_time} - {lesson.end_time}')

            course_week_set.add(lesson.day_of_week)
            course_hour_set.add(lesson.start_time)


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['grade']
        labels = {
            'grade': 'Select Grade:',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('grade', css_class='form-select')
        )
        self.fields['grade'].required = True


class FutureCareerForm(forms.Form):
    # Form for students to select future careers

    operating_sys_percentage = forms.DecimalField(
        max_digits=5, decimal_places=2, label="Operating System Percentage")
    algorithms_percentage = forms.DecimalField(
        max_digits=5, decimal_places=2, label="Algorithms Percentage")
    programming_percentage = forms.DecimalField(
        max_digits=5, decimal_places=2, label="Programming Percentage")
    software_eng_percentage = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        label="Software Engineering Percentage"
    )
    computer_network_percentage = forms.DecimalField(
        max_digits=5, decimal_places=2, label="Computer Network Percentage")
    electronics_percentage = forms.DecimalField(max_digits=5, decimal_places=2,
                                                label="Electronics Percentage")
    computer_arc_percentage = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        label="Computer Architecture Percentage"
    )
    math_percentage = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        label="Math Percentage"
    )
    communication_skills_percentage = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        label="Communication Skills Percentage"
    )
    coding_skills = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        label="Coding Skills"
    )

    def clean(self):
        cleaned_data = super().clean()
        percentage_fields = [
            'operating_sys_percentage',
            'algorithms_percentage',
            'programming_percentage',
            'software_eng_percentage',
            'computer_network_percentage',
            'electronics_percentage',
            'computer_arc_percentage',
            'math_percentage',
            'communication_skills_percentage',
            'coding_skills'
        ]

        for field in percentage_fields:
            value = cleaned_data.get(field)
            if value is not None:
                if value < 0 or value > 100:
                    self.add_error(
                        field,
                        forms.ValidationError(
                            "Number must be between 0 and 100."
                        )
                    )

        return cleaned_data
