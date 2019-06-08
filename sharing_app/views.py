import random
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.storage import session
from django.core.exceptions import ValidationError
from django.http import request, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template
from django.urls import reverse_lazy
import datetime
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from search_views.views import SearchListView
from share_the_game import settings
from sharing_app.forms import RegisterForm, ProductSearchForm, ProductAddForm, ShareForm
from sharing_app.models import Profile, Product, ProductProfile
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from sharing_app.templatetags.my_app_filters import ProductSearchFilter


class MainPageView(View):
	def get(self, request):
		try:
			just_logged_out = request.session.get('just_logged_out', False)
		except:
			just_logged_out = False
		ctx = {
			'just_logged_out':just_logged_out

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
		send_mail(
			'Witaj w świecie planszówkowej wymiany!',
			'Dziękujemy za rejestrację na naszym portalu i zapraszamy do dzielenia się planszówkową radością :)',
			settings.EMAIL_HOST_USER,
			[user.email, settings.EMAIL_HOST_USER],
			fail_silently=False,
		)
		return render(self.request, 'main_page.html', {'form': form})



class ProductSearchListView(LoginRequiredMixin, SearchListView):
	login_url = '/login/'
	model = Product
	paginate_by = 30
	template_name = 'product_search.html'
	form_class = ProductSearchForm
	filter_class = ProductSearchFilter

	def list(request):
		product = Product.objects.all()
		return render(request, "product_search.html", {'product': product})


class ProductAddView(LoginRequiredMixin, FormView, ):
	login_url = '/login/'
	model = Product
	template_name = 'product_form.html'
	form_class = ProductAddForm


	def form_valid(self, form):
		# product_add_form = form
		new_product = Product()
		new_product.name = form.cleaned_data['name']
		new_product.category = form.cleaned_data['category']
		new_product.description = form.cleaned_data['description']
		new_product.min_number_of_players = form.cleaned_data['min_number_of_players']
		new_product.max_number_of_players = form.cleaned_data['max_number_of_players']
		new_product.min_age = form.cleaned_data['min_age']
		new_product.image = self.request.FILES['image']
		new_product.status = 'pending'
		new_product.save()
		# product_add_form.save(commit=False)
		# return redirect('product_detail', new_product.pk)
		return redirect('main_page')



class ProfileView(LoginRequiredMixin, View):
	login_url = '/login/'
	def get(self, request):
		logged_user = Profile.objects.get(pk=request.user.id)
		user_products = ProductProfile.objects.filter(profile__user_id=logged_user.id)
		ctx = {
			'logged_user': logged_user,
			'user_products': user_products
		}
		return render(request, 'profile.html', ctx)


class ProductDetailView(LoginRequiredMixin, View):
	login_url = '/login/'

	def get(self, request, object_id):
		product = Product.objects.get(pk=object_id)
		ctx = {
			'product': product
		}
		return render(request, 'product_detail.html', ctx)


class AddToCollectionView(LoginRequiredMixin, View):
	login_url = '/login/'

	def get(self, request, object_id):
		selected_product = Product.objects.get(pk=object_id)
		logged_user = Profile.objects.get(pk=request.user.id)
		user_product = logged_user.owned_product.add(selected_product)
		user_products = logged_user.owned_product.all()

		ctx = {
			'selected_product': selected_product,
			'logged_user': logged_user,
			'user_products': user_products,
			'user_product': user_product

		}
		return render(request, 'main_page.html', ctx)


class BorrowProductView(LoginRequiredMixin, View):
	login_url = '/login/'

	def get(self, request, object_id):
		form = ShareForm()
		ctx = {
			'form': form,
			'object_id':object_id
		}
		return render(request, 'borrow_product.html', ctx)

	def post(self, request,object_id):
		form = ShareForm(request.POST)

		if form.is_valid():
			selected_city = form.cleaned_data['selected_city']
			borrow_date = form.cleaned_data['borrow_date']
			return_date = form.cleaned_data['return_date']
			how_get = form.cleaned_data['how_get']
			delivery_adress = form.cleaned_data['delivery_adress']
			selected_product = Product.objects.get(pk=object_id)
			logged_user = Profile.objects.get(pk=request.user.id)
			if borrow_date < datetime.datetime.now().date() or return_date <= borrow_date or return_date < datetime.datetime.now().date():
				raise ValidationError('Data jest niepoprawna')
			else:
				if how_get == 'Odbiór osobisty':
					owners_from_city = ProductProfile.objects.filter(profile__city=selected_city, product_id=object_id, user_have=True).exclude(profile_id=logged_user.id)
					sharing_user = random.choice(owners_from_city)
					from_email = settings.EMAIL_HOST_USER
					to_email = [from_email, sharing_user.profile.user.email]
					send_mail(
						'Cześć! ',
						get_template('email.html').render(
							({
								'logged_user': logged_user,
								'selected_product': selected_product,
								'borrow_date': borrow_date,
								'return_date': return_date,
								'how_get': how_get,
								'delivery_adress': delivery_adress,
								'sharing_user': sharing_user,
								'object_id': object_id
							})
						),
						from_email,
						to_email,
						fail_silently=True,
					)
				else:
					owners_all = ProductProfile.objects.filter(product_id=object_id, user_have=True).exclude(profile_id=logged_user.id)
					sharing_user = random.choice(owners_all)
					from_email = settings.EMAIL_HOST_USER
					to_email = [from_email, sharing_user.profile.user.email]
					send_mail(
						'Cześć! ',
						get_template('email.html').render(
							({
								'logged_user': logged_user,
								'selected_product': selected_product,
								'borrow_date': borrow_date,
								'return_date': return_date,
								'how_get': how_get,
								'delivery_adress': delivery_adress,
								'sharing_user': sharing_user,
								'object_id':object_id
							})
						),
						from_email,
						to_email,
						fail_silently=True,
					)

				return render(request, 'success_borrow.html', {'sharing_user':sharing_user})

class SuccessBorrowView(LoginRequiredMixin,TemplateView):
	login_url = '/login/'
	template_name = 'success_borrow.html'


class UnavailableProductView(LoginRequiredMixin,View):
	login_url = '/login/'
	def get(self, request, object_id):
		product = Product.objects.get(pk=object_id)
		logged_user = Profile.objects.get(pk=request.user.id)
		user_selected_product = ProductProfile.objects.get(product_id=object_id, profile_id=request.user.id)
		user_products = ProductProfile.objects.filter(profile__user_id=logged_user.id)
		ProductProfile.objects.filter(pk=user_selected_product.id).update(user_have=False)
		ctx = {
			'user_selected_product': user_selected_product,
			'user_products': user_products,
		}
		return render(request, 'profile.html',ctx)


class AvailableProductView(LoginRequiredMixin,View):
	login_url = '/login/'
	def get(self, request, object_id):
		product = Product.objects.get(pk=object_id)
		logged_user = Profile.objects.get(pk=request.user.id)
		user_selected_product = ProductProfile.objects.get(product_id=object_id, profile_id=request.user.id)
		user_products = ProductProfile.objects.filter(profile__user_id=logged_user.id)
		ProductProfile.objects.filter(pk=user_selected_product.id).update(user_have=True)
		ctx = {
			'user_selected_product': user_selected_product,
			'user_products': user_products,
		}
		return render(request, 'profile.html', ctx)
