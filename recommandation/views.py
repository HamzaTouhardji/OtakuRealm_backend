from django.http import HttpResponse
#from .models import MANGA

def index(request):
    message = "Salut tout le monde !"
    return HttpResponse(message)


def listing(request):
    listManga = ["<li>{}</li>".format(manga['name']) for manga in MANGA]
    message = """<ul>{}</ul>""".format("\n".join(listManga))
    return HttpResponse(message)

def detail(request, manga_id):
    id = int(manga_id) # make sure we have an integer.
    manga = MANGA[id] # get the album with its id.
    auteur = " ".join([auteur['name'] for auteur in manga['auteur']]) # grab artists name and create a string out of it.
    message = "Le nom du manga est {}. Il a été écrit par {}".format(manga['name'], auteur)
    return HttpResponse(message)

def search(request):
    query = request.GET.get('query')
    if not query:
        message = "Aucun manga n'est demandé"
    else:
        listMangas = [
            manga for manga in MANGA
            if query in " ".join(auteur['name'] for auteur in manga['auteur'])
        ]

        if len(listMangas) == 0:
            message = "Misère de misère, nous n'avons trouvé aucun résultat !"
        else:
            listMangas = ["<li>{}</li>".format(manga['name']) for manga in listMangas]
            message = """
                Nous avons trouvé les albums correspondant à votre requête ! Les voici :
                <ul>
                    {}
                </ul>
            """.format("</li><li>".join(listMangas))

    return HttpResponse(message)