class RefugioStrategiesAdapter:
    def __init__(self, status_code, data=None, errors=None):
        self.__status_code = status_code
        self.__data = data
        self.__errors = errors

    @property
    def status_code(self):
        return self.__status_code

    @property
    def data(self):
        return self.__data

    @property
    def errors(self):
        return self.__errors
