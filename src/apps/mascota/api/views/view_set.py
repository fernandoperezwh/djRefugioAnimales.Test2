from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from src.apps.adopcion.api.serializers import PersonaSerializer
from src.apps.mascota.api.serializers import VacunaSerializer, MascotaSerializer
from src.apps.mascota.models import Vacuna, Mascota


class VacunaViewSet(viewsets.ModelViewSet):
    queryset = Vacuna.objects.all()
    serializer_class = VacunaSerializer


class MascotaViewSet(viewsets.ModelViewSet):
    queryset = Mascota.objects.all()
    serializer_class = MascotaSerializer

    @action(
        detail=True,
        url_path='persona',
        url_name='persona')
    def detail_persona(self, request, pk=None):
        serializer = PersonaSerializer(self.get_object().persona)
        return Response(serializer.data)
