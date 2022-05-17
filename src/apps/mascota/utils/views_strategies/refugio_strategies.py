from django.conf import settings

from src.apps.mascota.utils.views_strategies.instances import (
    ListVacunaViaAPIInstanceStrategy, ListMascotaViaAPIInstanceStrategy, ListPersonaViaAPIInstanceStrategy,
    DetailVacunaViaAPIInstanceStrategy, DetailMascotaViaAPIInstanceStrategy, DetailPersonaViaAPIInstanceStrategy,
    DetailMascotaPersonaViaAPIInstanceStrategy)
from src.apps.mascota.utils.views_strategies.requests import (
    ListVacunaViaAPIRequestsStrategy, ListMascotaViaAPIRequestsStrategy, ListPersonaViaAPIRequestsStrategy,
    CreateVacunaViaAPIRequestsStrategy, CreateMascotaViaAPIRequestsStrategy, CreatePersonaViaAPIRequestsStrategy,
    RetrieveVacunaViaAPIRequestsStrategy, RetrieveMascotaViaAPIRequestsStrategy, RetrievePersonaViaAPIRequestsStrategy,
    RetrieveMascotaPersonaViaAPIRequestsStrategy,
    UpdateVacunaViaAPIRequestsStrategy, UpdateMascotaViaAPIRequestsStrategy, UpdatePersonaViaAPIRequestsStrategy,
    DeleteVacunaViaAPIRequestsStrategy, DeleteMascotaViaAPIRequestsStrategy, DeletePersonaViaAPIRequestsStrategy)
from src.utils.constants import APIStrategy, APIResource


class RefugioStrategies:
    def __validate_strategy(self):
        if settings.API_STRATEGY not in APIStrategy.as_list():
            raise ValueError(F"La estrategia \"{settings.API_STRATEGY}\" no es valida. "
                             F"Favor de verificar su configuración.")

    def __validate_resource(self, resource):
        if resource not in APIResource.as_list():
            raise ValueError(F"El recurso \"{resource}\" no es un recurso valido.")

    # region retrieve methods
    def retrieve_vacunas(self):
        strategy = None
        if settings.API_STRATEGY == APIStrategy.INSTANCE:
            strategy = DetailVacunaViaAPIInstanceStrategy
        elif settings.API_STRATEGY == APIStrategy.REQUESTS:
            strategy = RetrieveVacunaViaAPIRequestsStrategy
        return strategy

    def retrieve_mascotas(self):
        strategy = None
        if settings.API_STRATEGY == APIStrategy.INSTANCE:
            strategy = DetailMascotaViaAPIInstanceStrategy
        elif settings.API_STRATEGY == APIStrategy.REQUESTS:
            strategy = RetrieveMascotaViaAPIRequestsStrategy
        return strategy

    def retrieve_mascotas_personas(self):
        strategy = None
        if settings.API_STRATEGY == APIStrategy.INSTANCE:
            strategy = DetailMascotaPersonaViaAPIInstanceStrategy
        elif settings.API_STRATEGY == APIStrategy.REQUESTS:
            strategy = RetrieveMascotaPersonaViaAPIRequestsStrategy
        return strategy

    def retrieve_personas(self):
        strategy = None
        if settings.API_STRATEGY == APIStrategy.INSTANCE:
            strategy = DetailPersonaViaAPIInstanceStrategy
        elif settings.API_STRATEGY == APIStrategy.REQUESTS:
            strategy = RetrievePersonaViaAPIRequestsStrategy
        return strategy
    # endregion

    # region list methods
    def list_vacunas(self):
        strategy = None
        if settings.API_STRATEGY == APIStrategy.INSTANCE:
            strategy = ListVacunaViaAPIInstanceStrategy
        elif settings.API_STRATEGY == APIStrategy.REQUESTS:
            strategy = ListVacunaViaAPIRequestsStrategy
        return strategy

    def list_mascotas(self):
        strategy = None
        if settings.API_STRATEGY == APIStrategy.INSTANCE:
            strategy = ListMascotaViaAPIInstanceStrategy
        elif settings.API_STRATEGY == APIStrategy.REQUESTS:
            strategy = ListMascotaViaAPIRequestsStrategy
        return strategy

    def list_personas(self):
        strategy = None
        if settings.API_STRATEGY == APIStrategy.INSTANCE:
            strategy = ListPersonaViaAPIInstanceStrategy
        elif settings.API_STRATEGY == APIStrategy.REQUESTS:
            strategy = ListPersonaViaAPIRequestsStrategy
        return strategy
    # endregion

    # region create methods
    def create_vacunas(self):
        strategy = None
        if settings.API_STRATEGY == APIStrategy.INSTANCE:
            strategy = ListVacunaViaAPIInstanceStrategy
        elif settings.API_STRATEGY == APIStrategy.REQUESTS:
            strategy = CreateVacunaViaAPIRequestsStrategy
        return strategy

    def create_mascotas(self):
        strategy = None
        if settings.API_STRATEGY == APIStrategy.INSTANCE:
            strategy = ListMascotaViaAPIInstanceStrategy
        elif settings.API_STRATEGY == APIStrategy.REQUESTS:
            strategy = CreateMascotaViaAPIRequestsStrategy
        return strategy

    def create_personas(self):
        strategy = None
        if settings.API_STRATEGY == APIStrategy.INSTANCE:
            strategy = ListPersonaViaAPIInstanceStrategy
        elif settings.API_STRATEGY == APIStrategy.REQUESTS:
            strategy = CreatePersonaViaAPIRequestsStrategy
        return strategy
    # endregion

    # region update methods
    def update_vacunas(self):
        strategy = None
        if settings.API_STRATEGY == APIStrategy.INSTANCE:
            strategy = DetailVacunaViaAPIInstanceStrategy
        elif settings.API_STRATEGY == APIStrategy.REQUESTS:
            strategy = UpdateVacunaViaAPIRequestsStrategy
        return strategy

    def update_mascotas(self):
        strategy = None
        if settings.API_STRATEGY == APIStrategy.INSTANCE:
            strategy = DetailMascotaViaAPIInstanceStrategy
        elif settings.API_STRATEGY == APIStrategy.REQUESTS:
            strategy = UpdateMascotaViaAPIRequestsStrategy
        return strategy

    def update_personas(self):
        strategy = None
        if settings.API_STRATEGY == APIStrategy.INSTANCE:
            strategy = DetailPersonaViaAPIInstanceStrategy
        elif settings.API_STRATEGY == APIStrategy.REQUESTS:
            strategy = UpdatePersonaViaAPIRequestsStrategy
        return strategy
    # endregion

    # region delete methods
    def delete_vacunas(self):
        strategy = None
        if settings.API_STRATEGY == APIStrategy.INSTANCE:
            strategy = DetailVacunaViaAPIInstanceStrategy
        elif settings.API_STRATEGY == APIStrategy.REQUESTS:
            strategy = DeleteVacunaViaAPIRequestsStrategy
        return strategy

    def delete_mascotas(self):
        strategy = None
        if settings.API_STRATEGY == APIStrategy.INSTANCE:
            strategy = DetailMascotaViaAPIInstanceStrategy
        elif settings.API_STRATEGY == APIStrategy.REQUESTS:
            strategy = DeleteMascotaViaAPIRequestsStrategy
        return strategy

    def delete_personas(self):
        strategy = None
        if settings.API_STRATEGY == APIStrategy.INSTANCE:
            strategy = DetailPersonaViaAPIInstanceStrategy
        elif settings.API_STRATEGY == APIStrategy.REQUESTS:
            strategy = DeletePersonaViaAPIRequestsStrategy
        return strategy
    # endregion

    # region public methods
    def retrieve(self, resource):
        self.__validate_strategy()
        self.__validate_resource(resource)
        return getattr(self, F"retrieve_{resource}")()()

    def list(self, resource):
        self.__validate_strategy()
        self.__validate_resource(resource)
        return getattr(self, F"list_{resource}")()()

    def create(self, resource):
        self.__validate_strategy()
        self.__validate_resource(resource)
        return getattr(self, F"create_{resource}")()()

    def update(self, resource):
        self.__validate_strategy()
        self.__validate_resource(resource)
        return getattr(self, F"update_{resource}")()()

    def delete(self, resource):
        self.__validate_strategy()
        self.__validate_resource(resource)
        return getattr(self, F"delete_{resource}")()()
    # endregion

