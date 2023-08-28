from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Profile


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        max_length=100, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        )

    password1 = forms.CharField(
        max_length=50, 
        required=True, 
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
        )
    password2 = forms.CharField(
        max_length=50, 
        required=True, 
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
        )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        
        
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})

        
class ProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control border border-info'}))

    class Meta:
        model = Profile
        fields = ['avatar']