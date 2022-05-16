from abc import abstractmethod, ABC

from requests import ConnectionError, ConnectTimeout
from rest_framework import status

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

    def exec(self, request):
        data = None
        try:
            response = self.api_request.get(self.endpoint, cookies=request.COOKIES)
            if response.status_code == status.HTTP_200_OK:
                data = response.json()
        except (ConnectionError, ConnectTimeout) as err:
            pass
        return data


class RetrieveViaAPIRequestsStrategy(IAPIRequestsStrategy, APIRequestsBase, ABC):
    def exec(self, request, pk):
        data = None
        try:
            response = self.api_request.get(self.endpoint.format(id=pk), cookies=request.COOKIES)
            if response is not None and response.status_code == status.HTTP_200_OK:
                data = response.json()
        except (ConnectionError, ConnectTimeout) as err:
            pass
        return data


class UpdateViaAPIRequestsStrategy(IAPIRequestsStrategy, APIRequestsBase, ABC):
    def exec(self, request, pk, data=None):
        data = data or dict()
        response_data = None
        try:
            response = self.api_request.put(self.endpoint.format(id=pk), data=data, cookies=request.COOKIES)
            if bool(response is not None and
                    response.status_code in (status.HTTP_200_OK, status.HTTP_201_CREATED)):
                response_data = response.json()
        except (ConnectionError, ConnectTimeout) as err:
            pass
        return response_data


class CreateViaAPIRequestsStrategy(IAPIRequestsStrategy, APIRequestsBase, ABC):
    def exec(self, request, data=None):
        data = data or dict()
        response_data = None
        try:
            response = self.api_request.post(self.endpoint, data=data, cookies=request.COOKIES)
            if bool(response is not None and
                    response.status_code in (status.HTTP_200_OK, status.HTTP_201_CREATED)):
                response_data = response.json()
        except (ConnectionError, ConnectTimeout) as err:
            pass
        return response_data


class DeleteViaAPIRequestsStrategy(IAPIRequestsStrategy, APIRequestsBase, ABC):
    def exec(self, request, pk):
        response_data = None
        try:
            response = self.api_request.delete(self.endpoint.format(id=pk), cookies=request.COOKIES)
            if bool(response is not None and
                    response.status_code in (status.HTTP_200_OK, status.HTTP_201_CREATED)):
                response_data = response.json()
        except (ConnectionError, ConnectTimeout) as err:
            pass
        return response_data
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
