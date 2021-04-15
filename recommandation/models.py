from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class Genre(models.Model):
    #le libellé
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name 

class Anime(models.Model):
    title = models.CharField(max_length=200)
    season = models.CharField(max_length=200)
    score = models.DecimalField(max_digits=4, decimal_places=2)
    production_studio = models.CharField(max_length=200)
    number_of_episodes = models.PositiveIntegerField()
    episode_duration = models.PositiveIntegerField()
    synopsis = models.TextField()
    URL = models.URLField() 
    genres = models.ManyToManyField(Genre)
    #user = models.ManyToManyField(User, related_name='mangas', blank=True)
    #Le champs ci-dessus est un exemple, ne pas prendre en compte.

    def __str__(self):
        return self.title 
    class Meta:
        verbose_name_plural = 'Anime'

class Utilisateur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    photo_de_profil = models.CharField(max_length=200)
    sexe = models.CharField(max_length=200)
    age = models.IntegerField()
    animes = models.ManyToManyField(Anime)
    genres = models.ManyToManyField(Genre)

class Review(models.Model):
    id_anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    id_utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    score = models.IntegerField()
    description = models.TextField()

class Preferer(models.Model):
    id_utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    id_genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

class Recommandation(models.Model):
    id_utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    id_anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    score = models.FloatField(null=True, blank=True, default=None)

class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError('Users must have an email address')
		if not username:
			raise ValueError('Users must have a username')

		user = self.model(
			email=self.normalize_email(email),
			username=username,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class Account(AbstractBaseUser):
	email 					= models.EmailField(verbose_name="email", max_length=60, unique=True)
	username 				= models.CharField(max_length=30, unique=True)
	date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin				= models.BooleanField(default=False)
	is_active				= models.BooleanField(default=True)
	is_staff				= models.BooleanField(default=False)
	is_superuser			= models.BooleanField(default=False)


	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	objects = MyAccountManager()

	def __str__(self):
		return self.email

	# For checking permissions. to keep it simple all admin have ALL permissons
	def has_perm(self, perm, obj=None):
		return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
		return True

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)