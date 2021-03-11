from django.conf.urls import url
from knox import views as knox_views
from django.urls import path

from . import views # import views so we can use them in urls.
from .views import RegisterAPI, LoginAPI


urlpatterns = [
    #url(r'^$', views.index), url(r'^pi/recommandation/', include('recommandation.urls')),

    # GET, POST, DELETE
    url(r'^api/recommandation$', views.recommandation_list),
    # GET, PUT, DELETE
    url(r'^api/recommandation/(?P<pk>[0-9]+)$', views.recommandation_detail),

    path('hello/', views.HelloView.as_view(), name='hello'),

    path('api/register/', RegisterAPI.as_view(), name='register'),

    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
]