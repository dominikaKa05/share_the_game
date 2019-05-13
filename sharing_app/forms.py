from django import forms
from .models import Profile
from django.forms import ModelForm

class LoginForm(forms.Form):
	login = forms.CharField(max_length=164, label= 'Nazwa użytkownika')
	password = forms.PasswordInput


class RegistrationForm(ModelForm):
	class Meta:
		model = Profile
		fields = '__all__'
