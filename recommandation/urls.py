from django.conf.urls import url
from knox import views as knox_views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import routers

from . import views # import views so we can use them in urls.
from .views import RegisterAPI,RechercheListView, RechercheViewSet, RecipeDetailAPIView, InfoUser,TopAnimeAnnee, TopAnimeAllTime,TopAnimeSaison, UtilisateurViewSet, RecommandationViewSet,  LoginAPI, AnimeList, CustomAuthToken, AnimeDetails, GenericAPIView, GenreList, UserList


router = routers.SimpleRouter()
router.register(r'info_utilisateur', UtilisateurViewSet, basename='utilisateur')
router.register(r'recommandation', RecommandationViewSet, basename='recommandation')
#router.register(r'recherche', RechercheViewSet, basename='recherche')



urlpatterns = [
    path('api/anime/', AnimeList.as_view()),
    path('api/anime_allTime/', TopAnimeAllTime.as_view()),
    path('api/anime_saison/', TopAnimeSaison.as_view()),
    path('api/anime_annee/', TopAnimeAnnee.as_view()),

    path('api/recherche/', RechercheListView.as_view()),

    #path('api/info_utilisateur/', InfoUser.as_view()),
    path('api/', include(router.urls)),
    path('api/token/', CustomAuthToken.as_view()),
    path('api/snippets', RecipeDetailAPIView.as_view()),
    #path('api/recommandation', InfoList.as_view()),
    #path('api/recommandation/', RecommandationViewSet.as_view()),

    path('api/genre/', GenreList.as_view()),
    path('api/generic/anime/<int:id>', GenericAPIView.as_view()),
    path('api/anime/<int:id>', AnimeDetails.as_view()),

    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', CustomAuthToken.as_view(), name='login'),
    
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
]