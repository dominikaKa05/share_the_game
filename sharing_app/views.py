from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from sharing_app.forms import LoginForm, RegisterForm

from .models import Profile


# Create your views here

class MainPageView(TemplateView):
	template_name = 'main_page.html'

class RegisterView(FormView):
	template_name = 'register_form.html'
	form_class = RegisterForm
	success_url = reverse_lazy('main_page')


class LoginView(FormView):
	template_name = 'login_form.html'
	form_class = LoginForm
	success_url = reverse_lazy('main_page')