# region Mascota views
from django.db.models import Q
from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from src.apps.adopcion.api.serializers import PersonaSerializer
from src.apps.adopcion.models import Persona


@api_view(['GET', 'POST'])
def persona_list(request):
    # region [POST] method
    if request.method == 'POST':
        serializer = PersonaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    # endregion

    # region [GET] method
    queryset = Persona.objects.all()
    search_query = request.query_params.get('q')
    if search_query:
        args = [Q(nombre__icontains=search_query) | Q(apellidos__icontains=search_query) |
                Q(email__icontains=search_query)]
        queryset = queryset.filter(*args)
    serializer = PersonaSerializer(queryset, many=True)
    return Response(serializer.data)
    # endregion


@api_view(['GET', 'PUT', 'DELETE'])
def persona_detail(request, pk):
    def get_object(pk):
        try:
            return Persona.objects.get(pk=pk)
        except Persona.DoesNotExist:
            raise Http404

    # region [PUT] method
    if request.method == 'PUT':
        instance = get_object(pk)
        serializer = PersonaSerializer(instance, data=request.data)
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
    serializer = PersonaSerializer(instance)
    return Response(serializer.data)
    # endregion
# endregion