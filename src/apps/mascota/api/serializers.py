from rest_framework import serializers

from src.apps.mascota.models import Mascota, Vacuna
from src.apps.adopcion.api.serializers import PersonaSerializer


class VacunaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacuna
        fields = '__all__'


class MascotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mascota
        exclude = ('foto',)

    def to_representation(self, instance):
        self.fields['persona'] = PersonaSerializer()
        self.fields['vacunas'] = VacunaSerializer(many=True)
        return super().to_representation(instance)
