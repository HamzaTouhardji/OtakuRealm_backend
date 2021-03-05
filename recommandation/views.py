from django.http import HttpResponse
from django.shortcuts import render

from .models import User, Anime
from .serializers import RecommandationSerializer

from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

"""
Cette fonction est appelé dans la page d'acceuil. Elle affiche l'ensemble des mangas de la BDD
"""
def index(request):
    message = "OTAKUREALM !"
    return HttpResponse(message)

def listing(request):
    # request albums
    lesMangas = Anime.objects.all()[:12]
    formatted_mangas = ["<li>{}</li>".format(manga.title) for manga in lesMangas]
    message = """<ul>{}</ul>""".format("\n".join(formatted_mangas))
    return HttpResponse(message)
"""
def detail(request, manga_id):
    lesMangas = Manga.objects.filter(id)
    id = int(manga_id) # make sure we have an integer.
    manga = MANGA[id] # get the album with its id.
    message = "Le nom du manga est {}".format(manga['name'])
    return HttpResponse(message)


class RecommandationViewSet(viewsets.ModelViewSet):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Manga.objects.all()
    serializer_class = RecommandationSerializer


def search(request):
    query = request.GET.get('query')
    if not query:
        manga = Manga.objects.all()
    else:
        #title__icontains n'est pas sensible a la casse et affiche les mangas meme si on donne qu'une partie du nom du manga
        lesMangas = Manga.objects.filter(title__icontains=query)
        #if len(lesMangas) == 0:
        if not lesMangas.exists():
            message = "Misère de misère, nous n'avons trouvé aucun résultat !"
        else:
            lesMangas = ["<li>{}</li>".format(manga.title) for manga in lesMangas]
            message = ""
                Nous avons trouvé les albums correspondant à votre requête ! Les voici :
                <ul>
                    {}
                </ul>
            "".format("</li><li>".join(lesMangas))

    return HttpResponse(message)
    
    """