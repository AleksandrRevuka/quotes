from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth import password_validation

from .models import Profile


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"}),
    )

    email = forms.EmailField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Email"}),
    )

    password1 = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}),
    )
    password2 = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}),
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "form-control", "placeholder": "Username"})
        self.fields["password"].widget.attrs.update({"class": "form-control", "placeholder": "Password"})


class ProfileForm(forms.ModelForm):
    avatar = forms.ImageField(
        widget=forms.FileInput(attrs={"class": "form-control border border-info"}),
    )

    class Meta:
        model = Profile
        fields = ["avatar"]


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=100,
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"}),
    )


class CastomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "New password"}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        max_length=50,
        required=True,
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "New password confirmation"}),
    )
