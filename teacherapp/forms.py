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

    # # Fetch unique projects and interested_domain values from the database
    # unique_projects = StudentCareer.objects.values_list(
    #     'project', flat=True).distinct()
    # unique_domains = StudentCareer.objects.values_list(
    #     'interested_domain', flat=True).distinct()

    # # Convert querysets to list of tuples
    # project_choices = [(project, project) for project in unique_projects]
    # domain_choices = [(domain, domain) for domain in unique_domains]

    # interest_domain = forms.MultipleChoiceField(
    #     choices=domain_choices,
    #     widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control'},),
    #     label='Interested Fields',
    #     required=True,
    # )

    # projects = forms.MultipleChoiceField(
    #     choices=project_choices,
    #     widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
    #     required=True,
    # )

    # python = forms.ChoiceField(choices=StudentCareer.COURSE_LEVEL,
    #                            widget=forms.RadioSelect)

    # sql = forms.ChoiceField(choices=StudentCareer.COURSE_LEVEL,
    #                         widget=forms.RadioSelect, label='SQL')

    # java = forms.ChoiceField(choices=StudentCareer.COURSE_LEVEL,
    #                          widget=forms.RadioSelect)
    pass