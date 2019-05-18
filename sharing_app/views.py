from django.contrib.auth import authenticate, login
from django.http import request
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.edit import FormView
from sharing_app.forms import LoginForm, RegisterForm

from sharing_app.models import Profile
from django.contrib.auth.models import User


class MainPageView(View):
	def get(self, request):
		profile = Profile.objects.get(pk=1)
		ctx = {
			"profile": profile,
		}
		return render(request, "main_page.html", ctx)


class RegisterView(FormView):
	template_name = 'register_form.html'
	form_class = RegisterForm
	success_url = reverse_lazy('main_page')
	def form_valid(self, form):
		user = form.save()
		user.refresh_from_db()
		user.profile.city = form.cleaned_data.get('city')
		user.save()
		raw_password = form.cleaned_data.get('password1')
		user = authenticate(username=user.username, password=raw_password)
		login(request, user)
		return render(request, 'register_form.html', {'form':form})
#
# class LoginView(FormView):
# 	template_name = 'registration/login.html'
# 	form_class = LoginForm
# 	success_url = reverse_lazy('main_page')