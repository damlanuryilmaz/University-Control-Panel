from django import forms
from .models import *


class GradeForm(forms.ModelForm):
    
    class Meta:
        model = Grade
        fields = ['grade']
        widgets = {
            'grade': forms.Select(choices=Grade.GRADE_TYPE),

        }



        
    
        
        
        
