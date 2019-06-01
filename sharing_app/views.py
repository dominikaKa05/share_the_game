from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.storage import session
from django.http import request, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, RedirectView, CreateView, TemplateView
from django.views.generic.edit import FormView
from search_views.views import SearchListView
from share_the_game import settings
from sharing_app.forms import RegisterForm, ProductSearchForm, ProductAddForm, ShareForm
from sharing_app.models import Profile, Product
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


class LogoutView(View):
	def get(self, request):
		logout(request)
		# session['just_logged_out'] = True
		return HttpResponseRedirect('/')



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

	def list(request):
		product = Product.objects.all()
		return render(request, "product_search.html", {'product': product})


# class ProductAddView(LoginRequiredMixin, CreateView):
# 	model = Product
# 	template_name = 'product_form.html'
#     fields = "__all__"

class ProductAddView(LoginRequiredMixin, FormView, ):
	model = Product
	template_name = 'product_form.html'
	form_class = ProductAddForm

	def form_valid(self, form):
		new_product = Product()
		new_product.name = form.cleaned_data['name']
		new_product.category = form.cleaned_data['category']
		new_product.description = form.cleaned_data['description']
		new_product.min_number_of_players = form.cleaned_data['min_number_of_players']
		new_product.max_number_of_players = form.cleaned_data['max_number_of_players']
		new_product.min_age = form.cleaned_data['min_age']
		new_product.image = self.request.FILES['image']
		new_product.save()
		return redirect('product_detail', new_product.pk)


# class ProductCreate(CreateView):
# 	model = Product
# 	fields = '__all__'


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

class ProfileView(LoginRequiredMixin, View):
	def get(self, request):
		logged_user = Profile.objects.get(pk=request.user.id)
		user_products = logged_user.owned_product.all()
		ctx = {
			'logged_user': logged_user,
			'user_products': user_products
		}
		return render(request, 'profile.html', ctx)


class ProductDetailView(LoginRequiredMixin, View):

	def get(self, request, object_id):
		product = Product.objects.get(pk=object_id)
		ctx = {
			'product': product
		}
		return render(request, 'product_detail.html', ctx)


class AddToCollectionView(LoginRequiredMixin, View):

	def get(self, request, object_id):
		product = Product.objects.get(pk=object_id)
		logged_user = Profile.objects.get(pk=request.user.id)
		logged_user.owned_product.add(product)
		owner = product.profile_set.all()
		user_products = logged_user.owned_product.all()

		ctx = {
			'product': product,
			'owner': owner,
			'logged_user': logged_user,
			'user_products': user_products
		}
		return render(request, 'profile.html', ctx)


class BorrowProductView(LoginRequiredMixin, View):

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
			product = Product.objects.get(pk=object_id)
			logged_user = Profile.objects.get(pk=request.user.id)
			product_owners= Profile.objects.filter(owned_product__id=object_id)
			sharing_user = product_owners.filter(city=selected_city).exclude(id=logged_user.id).order_by('?').first()

			# product_owners = product.profile_set.all()
			# owner_sharing = Profile.objects.filter(id=product_owners.id)
			# sharing_user = owner_sharing.filter(city=selected_city).exclude(id=logged_user.id).order_by('?').first()
			# sharing_user = Profile.objects.get(pk=owner_sharing.id)
			# sharing_user = Profile.objects.filter(city=selected_city).filter(owned_product=product.id).exclude(id=logged_user.id).order_by('?').first()
			from_email = settings.EMAIL_HOST_USER
			to_email = [from_email, sharing_user.user.email]

			send_mail(
				'Cześć! ',
				get_template('email.html').render(
					({
						'logged_user': logged_user,
						'product': product,
						'borrow_date': borrow_date,
						'return_date': return_date
					})
				),
				from_email,
				to_email,
				fail_silently=True,
			)
			info = str('Twoja prośba o wypożyczenie gry została wysłana do użytkownika:' + sharing_user.user.username)
			ctx = {

				'info':info,
				'sharing_user': sharing_user
			}
		return render(request, 'success_borrow.html', ctx)
	# template_name = 'borrow_product.html'
	# form_class = ShareForm
	#
	# # success_url = '/thanks/'
	#
	# def get(self, request, object_id):
	#
	# def form_valid(self, form):
	# 	selected_city = form.cleaned_data['city']
	# 	borrow_date = form.cleaned_data['borrow_date']
	# 	return_date = form.cleaned_data['return_date']
	# 	product = Product.objects.get(pk=self.request.object.id)
	# 	logged_user = Profile.objects.get(pk=self.request.user.id)
	# 	sharing_user = Profile.objects.filter(city=selected_city).order_by('?').first()
	# 	send_mail(
	# 		'Cześć! ',
	# 		get_template('email.html').render(
	# 			Context({
	# 				'logged_user': logged_user,
	# 				'product': product,
	# 				'borrow_date': borrow_date,
	# 				'return_date': return_date,
	# 			})
	# 		),
	# 		logged_user.email,
	# 		sharing_user.email,
	# 		fail_silently=True
	# 	)
	#
	# 	return super().form_valid(form)

class SuccessBorrowView(TemplateView):
	template_name = 'success_borrow.html'


