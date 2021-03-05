"""otakurealm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

from django.contrib import admin
from django.urls import path, include 

from recommandation.views import RecommandationSerializer
from rest_framework import routers

from recommandation import views

router = routers.DefaultRouter()
router.register(r'recommandation', RecommandationSerializer, basename='recommandation')

urlpatterns = [
    path('', include(router.urls)),
    #url(r'^$', views.index, name="index"),
    url(r'^recommandation/', include('recommandation.urls')),
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

"""

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from recommandation import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^recommandation/', include('recommandation.urls')),
    url(r'^admin/', admin.site.urls)
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns