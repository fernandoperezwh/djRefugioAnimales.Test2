"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from src.utils.constants.api_version import ApiVersion


# region Dependiendo a la configuración del proyecto es como importamos las vistas a utilizar
api_version = settings.API_VERSION
api_url_patterns = []

if api_version == ApiVersion.V1:
    api_url_patterns = [
        path('api/', include('src.apps.adopcion.api.urls.api_view_decorator')),
        path('api/', include('src.apps.mascota.api.urls.api_view_decorator')),
    ]
elif api_version == ApiVersion.V2:
    api_url_patterns = [
        path('api/', include('src.apps.adopcion.api.urls.api_view_class')),
        path('api/', include('src.apps.mascota.api.urls.api_view_class')),
    ]
elif api_version == ApiVersion.V3:
    api_url_patterns = [
        path('api/', include('src.apps.adopcion.api.urls.generic_view')),
        path('api/', include('src.apps.mascota.api.urls.generic_view')),
    ]
elif api_version == ApiVersion.V4:
    api_url_patterns = [
        path('api/', include('src.apps.adopcion.api.urls.view_set')),
        path('api/', include('src.apps.mascota.api.urls.view_set')),
    ]
else:
    raise ImportError(F"La versión del API {api_version} no es una configuración valida.")
# endregion

urlpatterns = [
    path('admin/', admin.site.urls),
    # Se agregan las urls del api dependiendo de la versión en la que corre el proyecto
    *api_url_patterns,
]
