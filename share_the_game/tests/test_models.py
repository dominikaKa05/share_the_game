
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.http import response
from django.test import TestCase, Client
from sharing_app.models import Profile, Product, ProductProfile
import unittest



class ProfileModelTestCase(TestCase):
	def setUp(self):
		self.product = Product.objects.create(name='game', description='super')
		self.user = User.objects.create(username='baba', email='baba@gmail.com')
		self.productprofile = ProductProfile.objects.create(product_id=self.product.id,profile_id=self.user.id)

	def test_add_product(self):
		self.assertTrue(self.productprofile.user_have, True)


	def tearDown(self) -> None:
		self.product = None
		self.user = None
		self.productprofile = None

class ProductModelTestCase(TestCase):
	def setUp(self):
		self.game = Product.objects.create(name='Super gra', category='rodzinna', description='blaaaa', min_number_of_players=1,
							   max_number_of_players=2, min_age=5)

	def test_status(self):
		self.assertEquals(self.game.status,'pending')

	def tearDown(self) -> None:
		self.game = None



class SimpleTest(unittest.TestCase):
	def setUp(self):
		self.client = Client()
		self.client.login(username='anakonda', password='bubu.sucks')
		self.assertEqual(response.status_code, 200)
