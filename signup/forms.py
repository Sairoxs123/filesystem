from django import forms
from django.forms import ModelForm
from core.models import Users

class SignupForm(ModelForm):
    class Meta:
        model = Users
        fields = ('email', 'password')

        widgets = {
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email Address: '}),
            'password' : forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password: '}),
        }
