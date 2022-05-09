from django.conf.urls import url

from src.apps.adopcion import views

urlpatterns = [
    url(r'^persona/list/$', views.PersonaApiListView.as_view(), name='persona_list_api'),
    url(r'^persona/new/$', views.persona_form_api, name='persona_new_api'),
    url(r'^persona/edit/(\d+)/$', views.persona_form_api, name='persona_edit_api'),
    url(r'^persona/delete/(\d+)/$', views.persona_delete_api, name='persona_delete_api'),
]