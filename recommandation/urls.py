from django.conf.urls import url

from . import views # import views so we can use them in urls.


urlpatterns = [
    url(r'^$', views.listing),    
    url(r'^(?P<manga_id>[0-9]+)/$', views.detail),
    url(r'^search/$', views.search),
]