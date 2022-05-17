from django.db.models import Q
from django.http import Http404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from src.apps.adopcion.models import Persona
from src.apps.adopcion.api.serializers import PersonaSerializer


# region Persona views
class PersonaList(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Persona.objects.all()
        search_query = request.query_params.get('q')
        if search_query:
            args = [Q(nombre__icontains=search_query) | Q(apellidos__icontains=search_query) |
                    Q(email__icontains=search_query)]
            queryset = queryset.filter(*args)
        serializer = PersonaSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = PersonaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PersonaDetail(APIView):
    def get_object(self, pk):
        try:
            return Persona.objects.get(pk=pk)
        except Persona.DoesNotExist:
            raise Http404

    def get(self, request, pk, *args, **kwargs):
        instance = self.get_object(pk)
        serializer = PersonaSerializer(instance)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        instance = self.get_object(pk)
        serializer = PersonaSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk, *args, **kwargs):
        instance = self.get_object(pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# endregion
