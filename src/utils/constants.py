class ApiVersion:
    """
    Enum que indica la versión del api a utilizar
    """
    V1 = 'v1'
    V2 = 'v2'
    V3 = 'v3'
    V4 = 'v4'


class APIStrategy:
    """
    ENUM que indica la estrategia a utilizar para obtener la
    información desde la api con DRF.
    """
    REQUESTS = 'requests'
    INSTANCE = 'instance'

    @staticmethod
    def as_list():
        return [APIStrategy.REQUESTS, APIStrategy.INSTANCE]


class APIResource:
    """
    ENUM que indica los recursos disponibles de la api
    """
    VACUNAS = 'vacunas'
    MASCOTAS = 'mascotas'
    MASCOTAS_PERSONAS = 'mascotas_personas'
    PERSONAS = 'personas'

    @staticmethod
    def as_list():
        return [APIResource.MASCOTAS, APIResource.MASCOTAS_PERSONAS, APIResource.VACUNAS, APIResource.PERSONAS]
