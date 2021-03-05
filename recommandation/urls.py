from django.conf.urls import url

from . import views # import views so we can use them in urls.


urlpatterns = [
    #url(r'^$', views.index), url(r'^pi/recommandation/', include('recommandation.urls')),

    # GET, POST, DELETE
    url(r'^api/recommandation$', views.recommandation_list),
    # GET, PUT, DELETE
    url(r'^api/recommandation/(?P<pk>[0-9]+)$', views.recommandation_detail),
    # GET
    url(r'^api/recommandation/published$', views.recommandation_list_published)
    #url(r'^admin/', admin.site.urls)
]