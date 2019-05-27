from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import request, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, RedirectView, CreateView
from django.views.generic.edit import FormView
from search_views.views import SearchListView
from share_the_game import settings
from sharing_app.forms import RegisterForm, ProductAddForm, ProductSearchForm

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
		return render(self.request, 'main_page.html', {'form': form})


class LogoutView(View):
	def get(self, request):
		logout(request)
		return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)


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


class ProductSearchListView(LoginRequiredMixin, SearchListView):
	model = Product
	paginate_by = 30
	template_name = 'product_search.html'
	form_class = ProductSearchForm
	filter_class = ProductSearchFilter


# class ProductAddView(LoginRequiredMixin, CreateView):
# 	model = Product
# 	template_name = 'product_add.html'
#     fields = "__all__"

class ProductAddView(LoginRequiredMixin, FormView):
	model = Product
	template_name = 'product_add.html'
	form_class = ProductAddForm

	def form_valid(self, form):
		new_product = Product()
		new_product.name = form.cleaned_data['name']
		new_product.category = form.cleaned_data['category']
		new_product.description = form.cleaned_data['description']
		new_product.min_number_of_players = form.cleaned_data['min_number_of_players']
		new_product.max_number_of_players = form.cleaned_data['max_number_of_players']
		new_product.min_age = form.cleaned_data['min_age']
		new_product.image = request.FILES['image']
		new_product.save()
		return redirect('product_detail', new_product.pk)


# class ProfileView(View):
# 	def get(self,request):
# 		owner = request.user
#
# 		products = Product.objects.get(pk=request.user.id)
# 		ctx = {
# 			'products': products,
# 			'owner': owner
# 		}
# 		return render(request, 'profile.html', ctx)

class ProfileView(ListView):
	model = Profile

	def head(self, *args, **kwargs):
		owner = request.user
		products = Product.objects.filter(request.user.id)
		owned_products = Profile.owned_product.get(pk=products.id)
		response = HttpResponse('')
		# RFC 1123 date format
		response['Last-Modified'] = last_book.publication_date.strftime('%a, %d %b %Y %H:%M:%S GMT')
		return response


class ProductDetailListView(View):

	def get(self,request, object_id):
		product=  Product.objects.get(pk=object_id)


