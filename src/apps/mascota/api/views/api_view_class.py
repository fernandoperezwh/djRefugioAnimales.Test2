from django.db.models import Q
from django.http import Http404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from src.apps.adopcion.api.serializers import PersonaSerializer
from src.apps.mascota.models import Vacuna, Mascota
from src.apps.mascota.api.serializers import VacunaSerializer, MascotaSerializer


# region Vacuna views
class VacunaList(APIView):
    def get(self, request):
        queryset = Vacuna.objects.all()
        search_query = request.query_params.get('q')
        if search_query:
            queryset = queryset.filter(nombre__icontains=search_query)
        serializer = VacunaSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = VacunaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VacunaDetail(APIView):
    def get_object(self, pk):
        try:
            return Vacuna.objects.get(pk=pk)
        except Vacuna.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        instance = self.get_object(pk)
        serializer = VacunaSerializer(instance)
        return Response(serializer.data)

    def put(self, request, pk):
        instance = self.get_object(pk)
        serializer = VacunaSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        instance = self.get_object(pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# endregion


# region Mascota views
class MascotaList(APIView):
    def get(self, request):
        queryset = Mascota.objects.prefetch_related('persona').all()
        search_query = request.query_params.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(nombre__icontains=search_query) |
                Q(persona__nombre__icontains=search_query) |
                Q(persona__apellidos__icontains=search_query)
            )
        serializer = MascotaSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MascotaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MascotaDetail(APIView):
    def get_object(self, pk):
        try:
            return Mascota.objects.get(pk=pk)
        except Mascota.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        instance = self.get_object(pk)
        serializer = MascotaSerializer(instance)
        return Response(serializer.data)

    def put(self, request, pk):
        instance = self.get_object(pk)
        serializer = MascotaSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        instance = self.get_object(pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MascotaPersonaDetail(APIView):
    def get_object(self, pk):
        try:
            return Mascota.objects.get(pk=pk)
        except Mascota.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        instance = self.get_object(pk)
        serializer = PersonaSerializer(instance.persona)
        return Response(serializer.data)
# endregion
