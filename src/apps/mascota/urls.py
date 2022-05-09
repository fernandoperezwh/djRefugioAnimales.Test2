from django.conf.urls import url

from src.apps.mascota import views

urlpatterns = [
    url(r'^vacuna/list/$', views.VacunaApiListView.as_view(), name="vacuna_list_api"),
    url(r'^vacuna/new/$', views.vacuna_form_api, name="vacuna_new_api"),
    url(r'^vacuna/edit/(\d+)/$', views.vacuna_form_api, name="vacuna_edit_api"),
    url(r'^vacuna/delete/(\d+)/$', views.vacuna_delete_api, name="vacuna_delete_api"),


    url(r'^mascota/list/$', views.MascotaApiListView.as_view(), name="mascota_list_api"),
    url(r'^mascota/new/$', views.mascota_form_api, name="mascota_new_api"),
    url(r'^mascota/edit/(\d+)/$', views.mascota_form_api, name="mascota_edit_api"),
    url(r'^mascota/delete/(\d+)/$', views.mascota_delete_api, name="mascota_delete_api"),
    url(r'^mascota/(\d+)/persona/$', views.MascotaPersonaView.as_view(), name="mascota_persona_api"),
]