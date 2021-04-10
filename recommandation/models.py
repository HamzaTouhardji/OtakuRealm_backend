from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

class Genre(models.Model):
    #le libellé
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name 

class Anime(models.Model):
    title = models.CharField(max_length=200)
    season = models.PositiveIntegerField()
    score = models.IntegerField()
    production_studio = models.CharField(max_length=200)
    number_of_episodes = models.PositiveIntegerField()
    episode_duration = models.PositiveIntegerField()
    synopsis = models.TextField()
    rating = models.IntegerField()
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
    score = models.IntegerField()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)