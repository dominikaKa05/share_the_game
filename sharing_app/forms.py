from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.http import request

from django.forms import ModelForm, PasswordInput
from django.contrib.auth.models import User
from .models import Profile


class LoginForm(ModelForm):
	class Meta:
		model = User
		fields = ['username', 'password']
		widgets = {
			'password': forms.PasswordInput(),
		}


class RegisterForm(UserCreationForm):

	city = forms.CharField(label= 'Miasto')

	class Meta:
		model = User
		fields = ('username', 'password1', 'password2', 'email', 'city')
		widgets = {
			'password1': forms.PasswordInput(),
			'password2': forms.PasswordInput()
		}
