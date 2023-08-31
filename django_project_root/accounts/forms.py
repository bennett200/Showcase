from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ['email',]
        widgets = {
            'username': forms.TextInput(attrs={'id': 'username', 'class': 'lf--input', }),
            'password': forms.PasswordInput(attrs={'id': 'password', 'class': 'lf--input'})
        }
        
class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = User
        fields = '__all__'