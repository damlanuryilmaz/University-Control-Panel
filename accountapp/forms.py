from accountapp.models import CustomUser
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
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

        if commit:
            user.save()
        return user
