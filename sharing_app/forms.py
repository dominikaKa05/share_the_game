from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm, PasswordInput, SelectDateWidget
from django.contrib.auth.models import User
import datetime

from .models import Profile, Product


class RegisterForm(UserCreationForm):
	city = forms.CharField(label='Miasto', required=True)

	class Meta:
		model = User
		fields = ('username', 'password1', 'password2', 'email', 'city')
		widgets = {
			'password1': forms.PasswordInput(),
			'password2': forms.PasswordInput()
		}


class ProductSearchForm(forms.Form):
	search_title = forms.CharField(
		required=False,
		label='Tytuł',
		widget=forms.TextInput(attrs={'placeholder': 'Wpisz tytuł'})
	)

	search_category = forms.CharField(
		required=False,
		label='Kategoria',
		widget=forms.TextInput(attrs={'placeholder': 'Wpisz kategorię'})
	)

	search_players_min = forms.IntegerField(
		required=False,
		label='Minimalna liczba graczy',
		widget=forms.NumberInput(attrs={'placeholder': 'od:'})
	)

	search_players_max = forms.IntegerField(
		required=False,
		label=' Maksymalna liczba graczy ',
		widget=forms.NumberInput(attrs={'placeholder': 'do:'})
	)

	search_age_min = forms.IntegerField(
		required=False,
		label='Wiek gracza'
	)


class ProductAddForm(ModelForm):
	class Meta:
		model = Product
		exclude = ['status']


class ShareForm(forms.Form):
	DELIVERY_CHOICES = (
		('Odbiór osobisty', 'Odbiór osobisty'),
		('Wysyłka (opłacana przez osobę wypożyczają)', 'Wysyłka (opłacana przez osobę wypożyczają)'))
	selected_city = forms.CharField(label='Miejscowość zamieszkania wypożyczającego', max_length=100, required=False)
	how_get = forms.ChoiceField(label='Wybierz sposoób dostarczenia gry', choices=DELIVERY_CHOICES, required=True)
	delivery_adress = forms.CharField(label='Adres do wysyłki', required=False)
	borrow_date = forms.DateField(label='Data wypożyczenia', required=True,
								  widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD'}))
	return_date = forms.DateField(label='Data zwrotu', required=True,
								  widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD'}))

	# def clean(self):
	# 	cleaned_data = super(ShareForm, self).clean()
	# 	# here all fields have been validated individually,
	# 	# and so cleaned_data is fully populated
	# 	borrow_date = cleaned_data.get('borrow_date')
	# 	return_date = cleaned_data.get('return_date')
	# 	if borrow_date and return_date:
	# 		if borrow_date < datetime.datetime.now().date() or return_date < datetime.datetime.now().date():
	# 			msg = u"Daty nie mogą być z przeszłości !"
	# 			self.add_error('borrow_date',msg)
	# 		if return_date < datetime.datetime.now().date():
	# 			msg = u"Data zwrotu nie może być wcześniejsza niż wypożyczenia"
	# 			self.add_error('return_date',msg)
	# 	return cleaned_data

