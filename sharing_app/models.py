from django.db import models
from django.conf import settings

# Create your models here.
from django.utils.encoding import smart_text


class Profile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	city = models.CharField(max_length=120)
	email = models.EmailField

	def __str__(self):
		return smart_text(self.user.name)