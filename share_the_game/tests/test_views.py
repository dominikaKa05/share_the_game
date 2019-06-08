import unittest

from django.contrib.auth.models import User
from django.http import response
from django.test import Client
from django.urls import reverse
from sharing_app.models import Product, Profile, ProductProfile
from sharing_app.forms import ShareForm

class ProfileVIewTest(unittest.TestCase):
	def setUp(self):
		self.client = Client()
		self.client.force_login(User.objects.get_or_create(username='testuser')[0])

	def test_profile_view_GET(self):
		response = self.client.get(reverse('profile_view'))
		self.assertEqual(response.status_code, 200)


class ProductlViewTest(unittest.TestCase):
	def setUp(self):
		self.client = Client()
		self.client.force_login(User.objects.get_or_create(username='testuser')[0])
		self.user = User.objects.get(username='testuser')
		self.product = Product.objects.create(name='game', category='karciana', description='blaaaa', min_number_of_players=1,
							   max_number_of_players=2, min_age=5)


	def test_detail_view_GET(self):
		response = self.client.get(reverse('product_detail',kwargs={'object_id': self.product.id}))
		self.assertEqual(response.status_code, 200)

	def test_add_to_collection(self):
		self.user_product = self.user.profile.owned_product.add(self.product)
		response = self.client.get(reverse('add_to_collection',kwargs={'object_id': self.product.id}))
		self.assertEqual(response.status_code, 200)
