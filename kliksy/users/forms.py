from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

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

    def save(self):
        return super().save(commit=False)


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


class UserLoginForm(forms.Form):

    honeypot = forms.CharField(required=False, widget=forms.HiddenInput)
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)


class ResendVerificationEmailForm(forms.Form):
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput)
    email = forms.EmailField(required=True)


class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)  # From User model
    first_name = forms.CharField(
        max_length=150, required=False)  # From User model
    last_name = forms.CharField(
        max_length=150, required=False)  # From User model

    class Meta:
        model = Profile
        fields = ['bio', 'image', 'address_line_1', 'address_line_2',
                  'town', 'county', 'post_code']  # Fields from Profile model

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate initial values for User fields
        if self.instance and self.instance.user:
            self.fields['email'].initial = self.instance.user.email
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name

    def save(self, commit=True):
        profile = super().save(commit=False)
        # Update User fields
        user = profile.user
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            profile.save()
        return profile
