from accountapp.models import Student
from django import forms


class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['profile_photo']
        labels = {
            'profile_photo': '',
        }
