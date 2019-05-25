from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.http import request

from django.forms import ModelForm, PasswordInput
from django.contrib.auth.models import User
from .models import Profile, Product


# class LoginForm(ModelForm):
# 	class Meta:
# 		model = User
# 		fields = ['username', 'password']
# 		widgets = {
# 			'password': forms.PasswordInput(),
# 		}


class RegisterForm(UserCreationForm):

	city = forms.CharField(label= 'Miasto')

	class Meta:
		model = User
		fields = ('username', 'password1', 'password2', 'email', 'city')
		widgets = {
			'password1': forms.PasswordInput(),
			'password2': forms.PasswordInput()
		}

# class ProductSearchForm(ModelForm):
# 	class Meta:
# 		model = Product
# 		fields = '__all__'
# 		exclude = ('image','description')

class ProductSearchForm(forms.Form):
	search_title = forms.CharField(
		required=False,
		label='Szukaj po tytule',
		widget=forms.TextInput(attrs={'placeholder': 'Szukaj!'})
	)

	search_category = forms.CharField(
		required=False,
		label='Szukaj po kateogorii',
		widget=forms.TextInput(attrs={'placeholder': 'Szukaj!'})

	)

	# search_players_min = forms.IntegerField(
	# 	required=False,
	# 	label='Minimalna liczba graczy'
	# )

	search_players = forms.IntegerField(
		required=False,
		label=' liczba graczy'
	)

	search_age_min = forms.IntegerField(
		required=False,
		label='Minimalny wiek gracza'
	)


class ProductAddForm(ModelForm):
	class Meta:
		model = Product
		fields = '__all__'
