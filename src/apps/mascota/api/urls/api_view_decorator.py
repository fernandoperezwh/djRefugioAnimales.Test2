from django.conf.urls import url

from src.apps.mascota.api.views import api_view_decorator as views


urlpatterns = [
    url(r'^vacunas/$', views.vacuna_list),
    url(r'^vacunas/(?P<pk>\d+)/$', views.vacuna_detail),
    url(r'^mascotas/$', views.mascota_list),
    url(r'^mascotas/(?P<pk>\d+)/$', views.mascota_detail),
]
