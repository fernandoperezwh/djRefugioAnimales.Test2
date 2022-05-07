from django.conf.urls import url

from src.apps.adopcion.api.views import api_view_class as views


urlpatterns = [
    url(r'^personas/$', views.PersonaList.as_view()),
    url(r'^personas/(?P<pk>\d+)/$', views.PersonaDetail.as_view()),
]
