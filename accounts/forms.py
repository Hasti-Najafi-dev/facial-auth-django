from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django import forms

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'face_image']
        widgets = {
            'password': forms.PasswordInput()
        }