import requests
from django.conf import settings


class RefugioRequests:
    """ Clase de utilidad para realizar las peticiones al API entre lotes del proyecto.
    """

    def __init__(self, base_endpoint=None, timeout=10):
        self.__base_endpoint = base_endpoint or settings.API_ENDPOINT
        self.__timeout = timeout
        self.__headers = dict()
        self.__cookies = dict()

    def set_timeout(self, timeout):
        if not isinstance(timeout, int):
            raise TypeError("El tipo de dato del timeout debe ser un número entero")
        self.__timeout = timeout

    def get_timeout(self):
        return self.__timeout

    def get_header(self, key):
        return self.__headers.get(key)

    def set_header(self, key, value):
        if value is not None:
            self.__headers[key] = value
        # Si el valor del header es nulo y se encuentra dentro de los headers lo eliminamos
        if value is None and key in self.__headers.keys():
            del self.__headers[key]

    def get_headers(self):
        return self.__headers

    def get_cookie(self, key):
        return self.__cookies.get(key)

    def set_cookie(self, key, value):
        if value is not None:
            self.__cookies[key] = value
        # Si el valor del header es nulo y se encuentra dentro de los headers lo eliminamos
        if value is None and key in self.__cookies.keys():
            del self.__cookies[key]

    def get_cookies(self):
        return self.__cookies

    def __clean_path(self, path):
        return F"/{path}".replace('//', '/')

    def __requests(self, method, path, **kwargs):
        # Si no este especificado el timeout entonces lo agregamos
        kwargs['timeout'] = kwargs.get('timeout', self.__timeout)

        # Agregamos los headers que vienen en los parametros junto con los headers definidos en la clase
        kwargs['headers'] = {**self.get_headers(), **kwargs.get('headers', dict())}
        #
        return requests.request(method, path, **kwargs)

    def __set_csrf_token_from_cookies(self, cookies=None):
        cookies = cookies or dict()
        self.set_header('X-CSRFToken', cookies.get('csrftoken', None))

    def get(self, path, **kwargs):
        endpoint = F"{self.__base_endpoint}{self.__clean_path(path)}"
        return self.__requests('get', endpoint, **kwargs)

    def post(self, path, data=None, **kwargs):
        data = data or dict()
        endpoint = F"{self.__base_endpoint}{self.__clean_path(path)}"
        # Se intenta obtener de las cookies el csrf token
        if kwargs.get('cookies'):
            self.__set_csrf_token_from_cookies(kwargs.get('cookies'))
        #
        return self.__requests('post', endpoint, data=data, **kwargs)

    def put(self, path, data=None, **kwargs):
        data = data or dict()
        endpoint = F"{self.__base_endpoint}{self.__clean_path(path)}"
        # Se intenta obtener de las cookies el csrf token
        if kwargs.get('cookies'):
            self.__set_csrf_token_from_cookies(kwargs.get('cookies'))
        #
        return self.__requests('put', endpoint, data=data, **kwargs)

    def delete(self, path, **kwargs):
        endpoint = F"{self.__base_endpoint}{self.__clean_path(path)}"
        # Se intenta obtener de las cookies el csrf token
        if kwargs.get('cookies'):
            self.__set_csrf_token_from_cookies(kwargs.get('cookies'))
        #
        return self.__requests('delete', endpoint, **kwargs)

