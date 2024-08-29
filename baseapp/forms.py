from django import forms
from .models import Photo


class PhotoUploadForm(forms.Form):
    class Meta:
        model = Photo
        fields = ['image']

