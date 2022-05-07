from rest_framework import generics

from src.apps.mascota.api.serializers import VacunaSerializer, MascotaSerializer
from src.apps.mascota.models import Vacuna, Mascota


class VacunaList(generics.ListCreateAPIView):
    queryset = Vacuna.objects.all()
    serializer_class = VacunaSerializer


class VacunaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vacuna.objects.all()
    serializer_class = VacunaSerializer


class MascotaList(generics.ListCreateAPIView):
    queryset = Mascota.objects.all()
    serializer_class = MascotaSerializer


class MascotaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Mascota.objects.all()
    serializer_class = MascotaSerializer
