from django import forms
from django.http import request

from .models import Profile
from django.forms import ModelForm, PasswordInput
from django.contrib.auth.models import User


class LoginForm(ModelForm):
	class Meta:
		model = Profile
		fields = ['name', 'password']
		widgets = {
			'password': forms.PasswordInput(),
		}


class RegisterForm(ModelForm):
	class Meta:
		model = Profile
		fields = ['name', 'password', 'password2', 'email', 'city']
		widgets = {
			'password': forms.PasswordInput(),
			'password2': forms.PasswordInput()
		}
		error_messages = {
			'password_mismatch': ("Hasła nie pasują do siebie"),
		}



	def clean_password2(self):

		password1 = self.cleaned_data.get("password")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError(
				self.error_messages['password_mismatch'],
				code='password_mismatch',
				)
		return password2

	def save(self, commit=True):
		# user = super(RegisterForm, self).save(commit=False)
		# user.set_password(self.cleaned_data["password"])
		# if commit:
		# 	user.save()
		# return user
		#
		# if request.method == 'POST':
		# 	register_form = RegisterFormForm(data=request.POST)
		# 	if register_form.is_valid():
		# 		user = register_form.save()
		# 		user.set_password(clean_password2.password2)
		# 		user.save()
		# 		profile = profile_form.save(commit=False)
		# 		profile.user = user
		pass

