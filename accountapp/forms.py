from django import forms
from accountapp.models import CustomUser
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    # Initilize the form with deficient parts
    first_name = forms.CharField(
        max_length=100, required=True)
    last_name = forms.CharField(
        max_length=100, required=True)
    usable_password = None

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email',
                  'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].required = True
        self.fields['password2'].required = True
        self.fields['email'].required = True
        self.fields['username'].help_text = ''
        self.fields['email'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

    def clean(self):  # Clean the data cus validation!
        cleaned_data = super().clean()
        email = cleaned_data.get('email')

        if CustomUser.objects.filter(email=email).exists():
            self.add_error(
                'email', "A user with that email address already exists.")
            # Add same type error the field as others

        return cleaned_data

    def save(self, commit=True):  # Override the save method
        user = super().save(commit=False)
        # Commit is False cus add more data w/o saving
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:  # If commit is True, save the user
            # if we dont write this, we need to call save in the views
            user.save()
        return user
