import unittest
from sharing_app.forms import RegisterForm, ProductSearchForm, ProductAddForm, ShareForm
from sharing_app.models import Product


class RegisterFormTestCase(unittest.TestCase):

	def test_valid_data(self):
		form = RegisterForm({
			'username': 'Leela',
			'email': 'leela@example.com',
			'password1': 'lululala',
			'password2': 'lululala',
			'city': 'Londyn'
		})
		self.assertTrue(form.is_valid())
		comment = form.save()
		self.assertEqual(comment.username, "Leela")


class ProductSearchFormTestCase(unittest.TestCase):
	def setUp(self):
		self.product = Product.objects.create(name='Monopol', description='super')

	def test_valid_data(self):
		form = ProductSearchForm ({ 'search title': 'Monopol'})
		self.assertTrue(form.is_valid())
		self.assertEqual(self.product.description, "super")


class ProductAddFormTestCase(unittest.TestCase):

	def test_valid_data(self):
		form = ProductAddForm({
			'name': 'Chińczyk',
			'category': 'towarzyska',
			'description': 'najlepsza gra pod słońcem',
			'min_number_of_players': 3,
		})
		self.assertTrue(form.is_valid())
		comment = form.save()
		self.assertEqual(comment.category, 'towarzyska')

class ShareFormTest(unittest.TestCase):

	def test_valid_data(self):
		form = ShareForm({
			'how_get' : 'Wysyłka (opłacana przez osobę wypożyczają)',
			'borrow_date': '2019-07-01',
			'return_date': '2019-07-02',
		})
		self.assertTrue(form.is_valid())

