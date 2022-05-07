from rest_framework import generics

from src.apps.adopcion.api.serializers import PersonaSerializer
from src.apps.adopcion.models import Persona


class PersonaList(generics.ListCreateAPIView):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer


class PersonaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer