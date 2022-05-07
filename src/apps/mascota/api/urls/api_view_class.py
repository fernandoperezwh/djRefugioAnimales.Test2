from django.conf.urls import url

from src.apps.mascota.api.views import api_view_class as views


urlpatterns = [
    url(r'^vacunas/$', views.VacunaList.as_view()),
    url(r'^vacunas/(?P<pk>\d+)/$', views.VacunaDetail.as_view()),
    url(r'^mascotas/$', views.MascotaList.as_view()),
    url(r'^mascotas/(?P<pk>\d+)/$', views.MascotaDetail.as_view()),
]
