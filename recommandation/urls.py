from django.conf.urls import url
from knox import views as knox_views
from django.urls import path

from . import views # import views so we can use them in urls.
from .views import RegisterAPI, LoginAPI, AnimeList, AnimeDetails


urlpatterns = [
    path('api/anime/', AnimeList.as_view()),
    path('api/anime/<int:id>', AnimeDetails.as_view()),

    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
]