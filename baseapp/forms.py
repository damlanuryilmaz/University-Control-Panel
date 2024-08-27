from django import forms


class PhotoUploadForm(forms.Form):
    photo = forms.ImageField()
