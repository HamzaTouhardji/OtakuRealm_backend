from django.db import models



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
    #user = models.ManyToManyField(User, related_name='mangas', blank=True)
    #Le champs ci-dessus est un exemple, ne pas prendre en compte.

    def __str__(self):
        return self.title 
    class Meta:
        verbose_name_plural = 'Anime'


"""
class Reviews(models.Model):
    id_anime = models.ManyToManyField(Anime, related_name='mangas', blank=True)
    id_user = models.ManyToManyField(User, related_name='mangas', blank=True)
    date = models.DateField(auto_now=True)
    score = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.title 
"""

class Genre(models.Model):
    #le libellé
    wording = models.CharField(max_length=200)
    def __str__(self):
        return self.title 

"""
class Preferer(models.Model):
    id_user = models.ManyToManyField(User, related_name='mangas', blank=True)
    id_genre = models.ManyToManyField(User, related_name='mangas', blank=True)

    def __str__(self):
        return self.title 
"""