from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from .models import Profile

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = User
        fields = ['email', 'password1',
                  'password2', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True
        self.fields["password1"].required = True
        self.fields["password2"].required = True
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True

    def clean_honeypot(self):
        if self.cleaned_data.get('honeypot'):
            raise forms.ValidationError("Spam detected")


class ProfileRegistrationForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['date_of_birth', 'address_line_1',
                  'address_line_2', 'town', 'county', 'post_code', 'email_comms_opt_in']

        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def save(self) -> Profile:
        return super().save(commit=False)


class ResendVerificationEmailForm(forms.Form):
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput)
    email = forms.EmailField(required=True)
