from django.conf.urls import url
from knox import views as knox_views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views # import views so we can use them in urls.
from .views import RegisterAPI,UtilisateurViewSet,  LoginAPI, AnimeList, ListUsers, CustomAuthToken, AnimeDetails, GenericAPIView, GenreList, UserList


router = DefaultRouter()
router.register('users', UtilisateurViewSet)
urlpatterns = [
    path('api/anime/', AnimeList.as_view()),
    #path('api/users/', UtilisateurViewSet.as_view()),
    path('api/', include(router.urls)),
    path('api/token/', CustomAuthToken.as_view()),

    path('api/genre/', GenreList.as_view()),
    path('api/generic/anime/<int:id>', GenericAPIView.as_view()),
    path('api/anime/<int:id>', AnimeDetails.as_view()),

    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
]