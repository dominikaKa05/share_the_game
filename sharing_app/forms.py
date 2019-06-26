from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.contrib.auth.models import User

from .models import Product


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


