from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
from django.utils.encoding import smart_text




class Profile(models.Model):

	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	name = models.CharField(max_length=120, verbose_name= 'Nazwa użytkownika', default= '', unique= True)
	password = models.CharField(max_length=20, verbose_name='Hasło', default='')
	password2 = models.CharField(max_length=20, verbose_name='Potwierdż hasło', default= '')
	city = models.CharField(max_length=120, verbose_name = 'Miasto zamieszkania')
	email = models.EmailField(null=False, verbose_name= 'Adres email', unique= True, default='')

	def __str__(self):
		return smart_text(self.user.name)