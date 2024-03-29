from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.shortcuts import render

from .models import  Product
from .forms import ProductAddForm
from .views import ProductAddView



class ProductAdmin(admin.ModelAdmin):
	list_display = ['name', 'status']
	ordering = ['name']
	actions=['accept_product']


	def accept_product(modeladmin, request, queryset):
		queryset.update(status='accepted')
		if 'do_action' in request.POST:
			form = ProductAddForm(request.POST)
			if form.is_valid():
				status = form.cleaned_data['status']
				updated = queryset.update(status='accepted')
			else:
				form = ProductAddForm()

			return render(request, 'admin',
						  {'title': u'Choose genre',
						   'objects': queryset,
						   'form': form})



admin.site.register(Product, ProductAdmin)
