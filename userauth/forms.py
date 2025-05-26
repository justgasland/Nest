from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauth.models import User

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username"}))
    email = forms.EmailField(widget=forms.TextInput(attrs={"placeholder": "Enter your email"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Enter Your Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm Your Password"}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
