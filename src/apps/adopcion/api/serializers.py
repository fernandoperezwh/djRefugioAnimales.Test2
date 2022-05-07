from rest_framework import serializers

from src.apps.adopcion.models import Persona


class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = '__all__'
