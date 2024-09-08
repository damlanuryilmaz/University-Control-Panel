from crispy_forms.layout import Layout, Field, HTML
from teacherapp.models import FieldArea, Grade
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

    age = forms.IntegerField(label='How old are you?')
    gender = forms.ChoiceField(label='What is your gender?', choices=[
                               ('Male', 'Male'), ('Female', 'Female')])
    field = forms.ModelChoiceField(
        queryset=FieldArea.objects.all(),
        label='Education Field',
        empty_label="Select your field of study",
    )
    cgpa = forms.FloatField(label='What is your CGPA?',
                            help_text='Enter your CGPA out of 10.')
    internships = forms.IntegerField(
        label='How many internships have you done?')
    is_in_dorm = forms.BooleanField(label='I stay in the dormitory.',
                                    required=False)
    history_of_backlogs = forms.BooleanField(
        label='I have a history of backlogs.', required=False)

    def clean(self):
        cleaned_data = super().clean()
        age = cleaned_data.get('age')
        cgpa = cleaned_data.get('cgpa')
        internships = cleaned_data.get('internships')

        if age < 18 or age > 100:
            self.add_error(
                'age', "Age must be between 18 and 100.")

        if cgpa < 0 or cgpa > 10:
            self.add_error(
                'cgpa', "CGPA must be between 0 and 10.")

        if internships < 0:
            self.add_error(
                'internships', "Internships must be a positive number.")

        return cleaned_data
