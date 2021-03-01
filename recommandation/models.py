from django.db import models

class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=200, unique=True)
    
    def __str__(self):
        return self.name

class Manga(models.Model):
    title = models.CharField(max_length=200)
    picture = models.URLField()
    user = models.ManyToManyField(User, related_name='mangas', blank=True)
    #Le paramètre related_name indique le nom à utiliser pour la relation inverse depuis l'objet lié vers celui-ci.

    def __str__(self):
        return self.title 