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
	CATEGORY_CHOICES = (
		('', 'Wybierz kategorię'),
		('strategiczne', 'strategiczne'),
		('towarzyskie', 'towarzyskie'),
		('karciane', 'karciane'),
		('rodzinne', 'rodzinne'),
		('ekonomiczne', 'ekonomiczne'),
		('przygodowe', 'przygodowe'),
		('logiczne', 'logiczne'),
		('kooperacyjne', 'kooperacyjne'),
		('zręcznościowe', 'zręcznościowe'),
		('podróżne', 'podróżne'),
	)

	name = models.CharField(max_length=120,verbose_name='Tytuł', blank=False)
	category = models.CharField(max_length=120, verbose_name='Kategoria', choices=CATEGORY_CHOICES)
	description = models.TextField(blank=False, verbose_name='Opis', default='')
	min_number_of_players = models.IntegerField(blank=False, verbose_name='Minimalna liczba graczy', default='')
	max_number_of_players = models.IntegerField(blank=False, verbose_name='Maksymalna liczba graczy', default='')
	min_age = models.IntegerField(blank=True, verbose_name='Minimalny wiek gracza',default='')
	image = models.ImageField(upload_to='gallery/',blank=True)

