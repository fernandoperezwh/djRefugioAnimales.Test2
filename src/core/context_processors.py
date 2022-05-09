from django.conf import settings


def api_version(requests):
    return {'API_VERSION': settings.API_VERSION}
