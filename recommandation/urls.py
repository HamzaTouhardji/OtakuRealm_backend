from django.conf.urls import url

from . import views # import views so we can use them in urls.


urlpatterns = [
    url(r'^$', views.index), # "/recommandation" will call the method "index" in "views.py"
]