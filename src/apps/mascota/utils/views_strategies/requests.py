from abc import abstractmethod, ABC

from requests import ConnectionError, ConnectTimeout
from rest_framework import status

from src.apps.mascota.utils.views_strategies.refugio_strategies_adapter import RefugioStrategiesAdapter
from src.utils.classes.refugio_requests import RefugioRequests


# region util clases
class IAPIRequestsStrategy(ABC):
    @property
    @abstractmethod
    def endpoint(self):
        pass


class APIRequestsBase:
    def __init__(self, *args, **kwargs):
        self.api_request = RefugioRequests()


class ListViaAPIRequestsStrategy(IAPIRequestsStrategy, APIRequestsBase, ABC):
    def exec(self, request) -> RefugioStrategiesAdapter:
        kwargs_strategy_adapter = {}
        try:
            response = self.api_request.get(self.endpoint, cookies=request.COOKIES)
            kwargs_strategy_adapter = {
                'status_code': response.status_code,
                'data': response.json() if response.content else {},
            }
            # Se obtienes los errores desde el response si ocurre alguno
            if response.status_code == status.HTTP_400_BAD_REQUEST:
                kwargs_strategy_adapter['errors'] = response.json()

        except (ConnectionError, ConnectTimeout) as err:
            pass

        # Se retorna un objeto que sirve como adaptador entre la estrategia de instancia y requests
        return RefugioStrategiesAdapter(**kwargs_strategy_adapter)


class RetrieveViaAPIRequestsStrategy(IAPIRequestsStrategy, APIRequestsBase, ABC):
    def exec(self, request, pk) -> RefugioStrategiesAdapter:
        kwargs_strategy_adapter = {}
        try:
            response = self.api_request.get(self.endpoint.format(id=pk), cookies=request.COOKIES)
            kwargs_strategy_adapter = {
                'status_code': response.status_code,
                'data': response.json() if response.content else {},
            }
            # Se obtienes los errores desde el response si ocurre alguno
            if response.status_code == status.HTTP_400_BAD_REQUEST:
                kwargs_strategy_adapter['errors'] = response.json()

        except (ConnectionError, ConnectTimeout) as err:
            pass

        # Se retorna un objeto que sirve como adaptador entre la estrategia de instancia y requests
        return RefugioStrategiesAdapter(**kwargs_strategy_adapter)


class UpdateViaAPIRequestsStrategy(IAPIRequestsStrategy, APIRequestsBase, ABC):
    def exec(self, request, pk, data=None) -> RefugioStrategiesAdapter:
        data = data or dict()
        kwargs_strategy_adapter = {}
        try:
            response = self.api_request.put(self.endpoint.format(id=pk), data=data, cookies=request.COOKIES)
            kwargs_strategy_adapter = {
                'status_code': response.status_code,
                'data': response.json() if response.content else {},
            }
            # Se obtienes los errores desde el response si ocurre alguno
            if response.status_code == status.HTTP_400_BAD_REQUEST:
                kwargs_strategy_adapter['errors'] = response.json()

        except (ConnectionError, ConnectTimeout) as err:
            pass

        # Se retorna un objeto que sirve como adaptador entre la estrategia de instancia y requests
        return RefugioStrategiesAdapter(**kwargs_strategy_adapter)


class CreateViaAPIRequestsStrategy(IAPIRequestsStrategy, APIRequestsBase, ABC):
    def exec(self, request, data=None) -> RefugioStrategiesAdapter:
        data = data or dict()
        kwargs_strategy_adapter = {}
        try:
            response = self.api_request.post(self.endpoint, data=data, cookies=request.COOKIES)
            kwargs_strategy_adapter = {
                'status_code': response.status_code,
                'data': response.json() if response.content else {},
            }
            # Se obtienes los errores desde el response si ocurre alguno
            if response.status_code == status.HTTP_400_BAD_REQUEST:
                kwargs_strategy_adapter['errors'] = response.json()

        except (ConnectionError, ConnectTimeout) as err:
            pass

        # Se retorna un objeto que sirve como adaptador entre la estrategia de instancia y requests
        return RefugioStrategiesAdapter(**kwargs_strategy_adapter)


class DeleteViaAPIRequestsStrategy(IAPIRequestsStrategy, APIRequestsBase, ABC):
    def exec(self, request, pk) -> RefugioStrategiesAdapter:
        kwargs_strategy_adapter = {}
        try:
            response = self.api_request.delete(self.endpoint.format(id=pk), cookies=request.COOKIES)
            kwargs_strategy_adapter = {
                'status_code': response.status_code,
                'data': response.json() if response.content else {},
            }
            # Se obtienes los errores desde el response si ocurre alguno
            if response.status_code == status.HTTP_400_BAD_REQUEST:
                kwargs_strategy_adapter['errors'] = response.json()

        except (ConnectionError, ConnectTimeout) as err:
            pass

        # Se retorna un objeto que sirve como adaptador entre la estrategia de instancia y requests
        return RefugioStrategiesAdapter(**kwargs_strategy_adapter)
# endregion


# region list strategies
class ListVacunaViaAPIRequestsStrategy(ListViaAPIRequestsStrategy):
    endpoint = '/api/vacunas/'


class ListMascotaViaAPIRequestsStrategy(ListViaAPIRequestsStrategy):
    endpoint = '/api/mascotas/'


class ListPersonaViaAPIRequestsStrategy(ListViaAPIRequestsStrategy):
    endpoint = '/api/personas/'
# endregion


# region retrieve strategies
class RetrieveVacunaViaAPIRequestsStrategy(RetrieveViaAPIRequestsStrategy):
    endpoint = '/api/vacunas/{id}/'


class RetrieveMascotaViaAPIRequestsStrategy(RetrieveViaAPIRequestsStrategy):
    endpoint = '/api/mascotas/{id}/'


class RetrieveMascotaPersonaViaAPIRequestsStrategy(RetrieveViaAPIRequestsStrategy):
    endpoint = '/api/mascotas/{id}/persona/'


class RetrievePersonaViaAPIRequestsStrategy(RetrieveViaAPIRequestsStrategy):
    endpoint = '/api/personas/{id}/'
# endregion


# region update strategies
class UpdateVacunaViaAPIRequestsStrategy(UpdateViaAPIRequestsStrategy):
    endpoint = '/api/vacunas/{id}/'


class UpdateMascotaViaAPIRequestsStrategy(UpdateViaAPIRequestsStrategy):
    endpoint = '/api/mascotas/{id}/'


class UpdatePersonaViaAPIRequestsStrategy(UpdateViaAPIRequestsStrategy):
    endpoint = '/api/personas/{id}/'
# endregion


# region create strategies
class CreateVacunaViaAPIRequestsStrategy(CreateViaAPIRequestsStrategy):
    endpoint = '/api/vacunas/'


class CreateMascotaViaAPIRequestsStrategy(CreateViaAPIRequestsStrategy):
    endpoint = '/api/mascotas/'


class CreatePersonaViaAPIRequestsStrategy(CreateViaAPIRequestsStrategy):
    endpoint = '/api/personas/'
# endregion


# region delete strategies
class DeleteVacunaViaAPIRequestsStrategy(DeleteViaAPIRequestsStrategy):
    endpoint = '/api/vacunas/{id}/'


class DeleteMascotaViaAPIRequestsStrategy(DeleteViaAPIRequestsStrategy):
    endpoint = '/api/mascotas/{id}/'


class DeletePersonaViaAPIRequestsStrategy(DeleteViaAPIRequestsStrategy):
    endpoint = '/api/personas/{id}/'
# endregion
