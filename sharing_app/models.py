from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, AbstractUser

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import smart_text


class Product(models.Model):
	STATUS_CHOOICES = (
		('added','added'),
		('pending','pending'),
		('deleted', 'deleted'),
		('withdraw', 'withdraw')
	)
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

	name = models.CharField(max_length=120,verbose_name='Tytuł', null=False, blank=False)
	category = models.CharField(max_length=120, verbose_name='Kategoria', choices=CATEGORY_CHOICES, blank=False)
	description = models.TextField(blank=False, null=False, verbose_name='Opis', default='Opis')
	min_number_of_players = models.IntegerField(blank=False, null=False, verbose_name='Minimalna liczba graczy', default=1)
	max_number_of_players = models.IntegerField(blank=True, verbose_name='Maksymalna liczba graczy', default=1)
	min_age = models.IntegerField(blank=True, null=True,verbose_name='Minimalny wiek gracza',default=0)
	image = models.FileField(null=True, blank=True)
	status = models.CharField(max_length=120,choices=STATUS_CHOOICES, default='pending', null=False, blank=False)



class Profile(models.Model):

	user = models.OneToOneField(User, on_delete=models.CASCADE)
	city = models.CharField(max_length=120, verbose_name = 'Miasto zamieszkania')
	owned_product = models.ManyToManyField(Product, through= 'ProductProfile')


	def __str__(self):
		return smart_text(self.user.username)

	@receiver(post_save, sender=User)
	def create_user_profile(sender, instance, created, **kwargs):
		if created:
			Profile.objects.create(user=instance)

	@receiver(post_save, sender=User)
	def save_user_profile(sender, instance, **kwargs):
		instance.profile.save()


class ProductProfile(models.Model):
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	user_have = models.BooleanField(default=True)

