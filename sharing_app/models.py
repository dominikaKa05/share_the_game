from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, AbstractUser

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import smart_text




class Profile(models.Model):

	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	city = models.CharField(max_length=120, verbose_name = 'Miasto zamieszkania')

	def __str__(self):
		return smart_text(self.name)

	@receiver(post_save, sender=User)
	def create_user_profile(sender, instance, created, **kwargs):
		if created:
			Profile.objects.create(user=instance)

	@receiver(post_save, sender=User)
	def save_user_profile(sender, instance, **kwargs):
		instance.profile.save()

class Product(models.Model):
	name = models.CharField(max_length=120,verbose_name='Tytuł')
	category = models.CharField(max_length=120, verbose_name='Kategoria')
	description = models.TextField()
	min_number_of_gamers = models.IntegerField()
	max_numer_of_gamers = models.IntegerField
	image = models.ImageField(upload_to='images/')

