from accountapp.models import Student, Teacher
from baseapp.models import Department
from django import forms


class DepartmentRequestForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['department_of_student',]
        widget = {
            'department_of_student': forms.Select,
        }
        labels = {

            'department_of_student': 'Select Department:',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['department_of_student'].queryset = \
            Department.objects.all()
        self.fields['department_of_student'].required = True


class AssignAdviserForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['adviser',]
        widget = {
            'adviser': forms.Select,
        }
        labels = {
            'adviser': 'Select Adviser:',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['adviser'].queryset = \
            Teacher.objects.all()
        self.fields['adviser'].required = True
