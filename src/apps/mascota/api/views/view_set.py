from rest_framework import viewsets

from src.apps.mascota.api.serializers import VacunaSerializer, MascotaSerializer
from src.apps.mascota.models import Vacuna, Mascota


class VacunaViewSet(viewsets.ModelViewSet):
    queryset = Vacuna.objects.all()
    serializer_class = VacunaSerializer


class MascotaViewSet(viewsets.ModelViewSet):
    queryset = Mascota.objects.all()
    serializer_class = MascotaSerializer
