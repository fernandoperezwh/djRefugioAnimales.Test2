from rest_framework import viewsets

from src.apps.adopcion.api.serializers import PersonaSerializer
from src.apps.adopcion.models import Persona


class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer

