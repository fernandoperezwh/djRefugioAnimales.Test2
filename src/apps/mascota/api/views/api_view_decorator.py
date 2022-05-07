from django.db.models import Q
from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from src.apps.mascota.api.serializers import VacunaSerializer, MascotaSerializer
from src.apps.mascota.models import Vacuna, Mascota


# region Vacuna views
@api_view(['GET', 'POST'])
def vacuna_list(request):
    # region [POST] method
    if request.method == 'POST':
        serializer = VacunaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    # endregion

    # region [GET] method
    queryset = Vacuna.objects.all()
    search_query = request.query_params.get('q')
    if search_query:
        queryset = queryset.filter(nombre__icontains=search_query)
    serializer = VacunaSerializer(queryset, many=True)
    return Response(serializer.data)
    # endregion


@api_view(['GET', 'PUT', 'DELETE'])
def vacuna_detail(request, pk):
    def get_object(pk):
        try:
            return Vacuna.objects.get(pk=pk)
        except Vacuna.DoesNotExist:
            raise Http404

    # region [PUT] method
    if request.method == 'PUT':
        instance = get_object(pk)
        serializer = VacunaSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    # endregion

    # region [DELETE] method
    if request.method == 'DELETE':
        instance = get_object(pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    # endregion

    # region [GET] method
    instance = get_object(pk)
    serializer = VacunaSerializer(instance)
    return Response(serializer.data)
    # endregion
# endregion


# region Mascota views
@api_view(['GET', 'POST'])
def mascota_list(request):
    # region [POST] method
    if request.method == 'POST':
        serializer = MascotaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    # endregion

    # region [GET] method
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
    # endregion


@api_view(['GET', 'PUT', 'DELETE'])
def mascota_detail(request, pk):
    def get_object(pk):
        try:
            return Mascota.objects.get(pk=pk)
        except Mascota.DoesNotExist:
            raise Http404

    # region [PUT] method
    if request.method == 'PUT':
        instance = get_object(pk)
        serializer = MascotaSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    # endregion

    # region [DELETE] method
    if request.method == 'DELETE':
        instance = get_object(pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    # endregion

    # region [GET] method
    instance = get_object(pk)
    serializer = MascotaSerializer(instance)
    return Response(serializer.data)
    # endregion
# endregion