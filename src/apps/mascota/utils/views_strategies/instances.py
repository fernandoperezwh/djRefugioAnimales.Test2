from abc import ABC, abstractmethod

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from src.utils.constants import ApiVersion

# region Classes base
class APIInstanceBase(ABC):

    def __init__(self):
        self.context = dict()

    @property
    @abstractmethod
    def api_class(self):
        pass

    def _get_viewset_actions(self):
        """
        Verifica si 'api_class' es una subclase de GenericViewSet para enviar los actions
        """
        if issubclass(self.api_class, GenericViewSet):
            return self.context.pop('viewset_actions', {})
        return dict()

    def _validate_api_class(self):
        if not issubclass(self.api_class, APIView):
            raise ValueError('La clase definida en "api_class" debe ser una subclase de "APIView"')


class CallAPIInstance(APIInstanceBase, ABC):
    def _exec(self, request, *args, **kwargs):
        """
        Llama a ejecutar la clase de DRF para la información solicitada
        """
        request.content_type = 'application/json'
        self._validate_api_class()

        viewset_actions = self._get_viewset_actions()
        if viewset_actions:
            return self.api_class.as_view(viewset_actions)(request, *args, **kwargs)
        return self.api_class.as_view()(request, *args, **kwargs)

    def exec(self, request, *args, **kwargs):
        response = self._exec(request, *args, **kwargs)
        return response.data if (200 <= response.status_code < 300) else None
# endregion


# region list strategies
class ListVacunaViaAPIInstanceStrategy(CallAPIInstance):
    @property
    def api_class(self):
        if settings.API_VERSION == ApiVersion.V2:
            from src.apps.mascota.api.views.api_view_class import VacunaList
            return VacunaList

        elif settings.API_VERSION == ApiVersion.V3:
            from src.apps.mascota.api.views.generic_view import VacunaList
            return VacunaList

        elif settings.API_VERSION == ApiVersion.V4:
            from src.apps.mascota.api.views.view_set import VacunaViewSet
            self.context = {
                'viewset_actions': {
                    'get': 'list',
                    'post': 'create',
                },
            }
            return VacunaViewSet


class ListMascotaViaAPIInstanceStrategy(CallAPIInstance):
    @property
    def api_class(self):
        if settings.API_VERSION == ApiVersion.V2:
            from src.apps.mascota.api.views.api_view_class import MascotaList
            return MascotaList

        elif settings.API_VERSION == ApiVersion.V3:
            from src.apps.mascota.api.views.generic_view import MascotaList
            return MascotaList

        elif settings.API_VERSION == ApiVersion.V4:
            from src.apps.mascota.api.views.view_set import MascotaViewSet
            self.context = {
                'viewset_actions': {
                    'get': 'list',
                    'post': 'create',
                },
            }
            return MascotaViewSet


class ListPersonaViaAPIInstanceStrategy(CallAPIInstance):
    @property
    def api_class(self):
        if settings.API_VERSION == ApiVersion.V2:
            from src.apps.adopcion.api.views.api_view_class import PersonaList
            return PersonaList

        elif settings.API_VERSION == ApiVersion.V3:
            from src.apps.adopcion.api.views.generic_view import PersonaList
            return PersonaList

        elif settings.API_VERSION == ApiVersion.V4:
            from src.apps.adopcion.api.views.view_set import PersonaViewSet
            self.context = {
                'viewset_actions': {
                    'get': 'list',
                    'post': 'create',
                },
            }
            return PersonaViewSet
# endregion


# region detail strategies
class DetailVacunaViaAPIInstanceStrategy(CallAPIInstance):
    @property
    def api_class(self):
        if settings.API_VERSION == ApiVersion.V2:
            from src.apps.mascota.api.views.api_view_class import VacunaDetail
            return VacunaDetail

        elif settings.API_VERSION == ApiVersion.V3:
            from src.apps.mascota.api.views.generic_view import VacunaDetail
            return VacunaDetail

        elif settings.API_VERSION == ApiVersion.V4:
            from src.apps.mascota.api.views.view_set import VacunaViewSet
            self.context = {
                'viewset_actions': {
                    'get': 'retrieve',
                    'put': 'update',
                    'patch': 'partial_update',
                    'delete': 'destroy',
                },
            }
            return VacunaViewSet


class DetailMascotaViaAPIInstanceStrategy(CallAPIInstance):
    @property
    def api_class(self):
        if settings.API_VERSION == ApiVersion.V2:
            from src.apps.mascota.api.views.api_view_class import MascotaDetail
            return MascotaDetail

        elif settings.API_VERSION == ApiVersion.V3:
            from src.apps.mascota.api.views.generic_view import MascotaDetail
            return MascotaDetail

        elif settings.API_VERSION == ApiVersion.V4:
            from src.apps.mascota.api.views.view_set import MascotaViewSet
            self.context = {
                'viewset_actions': {
                    'get': 'retrieve',
                    'put': 'update',
                    'patch': 'partial_update',
                    'delete': 'destroy',
                },
            }
            return MascotaViewSet


class DetailPersonaViaAPIInstanceStrategy(CallAPIInstance):
    @property
    def api_class(self):
        if settings.API_VERSION == ApiVersion.V2:
            from src.apps.adopcion.api.views.api_view_class import PersonaDetail
            return PersonaDetail

        elif settings.API_VERSION == ApiVersion.V3:
            from src.apps.adopcion.api.views.generic_view import PersonaDetail
            return PersonaDetail

        elif settings.API_VERSION == ApiVersion.V4:
            from src.apps.adopcion.api.views.view_set import PersonaViewSet
            self.context = {
                'viewset_actions': {
                    'get': 'retrieve',
                    'put': 'update',
                    'patch': 'partial_update',
                    'delete': 'destroy',
                },
            }
            return PersonaViewSet
# endregion