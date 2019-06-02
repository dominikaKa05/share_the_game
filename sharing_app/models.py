from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, AbstractUser

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import smart_text
from django_random_queryset import RandomManager


class Product(models.Model):
	CATEGORY_CHOICES = (
		('', 'Wybierz kategorię gry'),
		('strategiczna', 'strategiczna'),
		('towarzyska', 'towarzyska'),
		('karciana', 'karciana'),
		('rodzinna', 'rodzinna'),
		('ekonomiczna', 'ekonomiczna'),
		('przygodowa', 'przygodowa'),
		('logiczna', 'logiczna'),
		('kooperacyjna', 'kooperacyjna'),
		('zręcznościowa', 'zręcznościowa'),
		('podróżna', 'podróżna'),
	)

	name = models.CharField(max_length=120,verbose_name='Tytuł', blank=False)
	category = models.CharField(max_length=120, verbose_name='Kategoria', choices=CATEGORY_CHOICES)
	description = models.TextField(blank=False, verbose_name='Opis', default='Opis')
	min_number_of_players = models.IntegerField(blank=False, verbose_name='Minimalna liczba graczy', default=0)
	max_number_of_players = models.IntegerField(blank=True, verbose_name='Maksymalna liczba graczy', default=0)
	min_age = models.IntegerField(blank=True, verbose_name='Minimalny wiek gracza',default=0)
	image = models.FileField(null=True, blank=True)




class Profile(models.Model):

	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	city = models.CharField(max_length=120, verbose_name = 'Miasto zamieszkania')
	owned_product = models.ManyToManyField(Product)


	# def __str__(self):
	# 	return smart_text(self.user.username)

	@receiver(post_save, sender=User)
	def create_user_profile(sender, instance, created, **kwargs):
		if created:
			Profile.objects.create(user=instance)

	@receiver(post_save, sender=User)
	def save_user_profile(sender, instance, **kwargs):
		instance.profile.save()

