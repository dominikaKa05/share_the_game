from django.contrib.auth import authenticate, login
from django.http import request
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import FormView
from search_views.views import SearchListView
from sharing_app.forms import  RegisterForm, ProductAddForm, ProductSearchForm

from sharing_app.models import Profile, Product
from django.contrib.auth.models import User

from sharing_app.templatetags.my_app_filters import ProductSearchFilter


class MainPageView(View):
	def get(self, request):
		profile = Profile.objects.get(pk=1)
		ctx = {
			"profile": profile,
		}
		return render(request, 'main_page.html', ctx)


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
		login(self.request, user)
		return render(self.request, 'main_page.html', {'form':form})

# class ProductSearchView(FormView):
# 	model = Product
# 	template_name = 'product_search.html'
# 	form_class = ProductSearchForm
# 	def form_valid(self, form):
# 		name =form.cleaned_data['name']
# 		category = form.cleaned_data['category']
# 		min_players = form.cleaned_data['min_number_of_players']
# 		max_players_= form.cleaned_data ['max_number_of_players']
# 		min_age = form.cleaned_data['min_age']
# 		if name != "":
# 			pass
# 		if category != "":
# 			pass
# 		if min_players != "":
# 			pass
# 		if max_players_!= "":
# 			pass
# 		if min_age != "":
# 			pass


class ProductSearchListView(SearchListView):
    model = Product
    paginate_by = 30
    template_name = 'product_search.html'
    form_class = ProductSearchForm
    filter_class = ProductSearchFilter



class ProductAddView(FormView):
	model = Product
	template_name = 'product_add.html'
	form_class = ProductAddForm



