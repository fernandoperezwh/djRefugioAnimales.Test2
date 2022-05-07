from django.conf.urls import url

from src.apps.adopcion.api.views import api_view_decorator as views


urlpatterns = [
    url(r'^personas/$', views.persona_list),
    url(r'^personas/(?P<pk>\d+)/$', views.persona_detail),
]
