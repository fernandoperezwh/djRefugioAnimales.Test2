from django import forms

from src.apps.mascota.models import Vacuna, Mascota
from src.utils.fnc.build_form_input_attrs import build_form_input_attrs


class VacunaForm(forms.ModelForm):
    class Meta:
        model = Vacuna
        fields = ('nombre',)
        widgets = {
            'nombre': forms.TextInput(attrs=build_form_input_attrs('nombre')),
        }


class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ('nombre', 'sexo', 'edad', 'fecha_rescate', 'persona', 'vacunas')
        widgets = {
            'nombre': forms.TextInput(attrs=build_form_input_attrs('nombre')),
            'sexo': forms.TextInput(attrs=build_form_input_attrs('sexo')),
            'edad': forms.NumberInput(attrs=build_form_input_attrs('edad')),
            'fecha_rescate': forms.DateInput(attrs=build_form_input_attrs('fecha_rescate')),
            'persona': forms.Select(attrs=build_form_input_attrs('persona')),
            'vacunas': forms.SelectMultiple(attrs=build_form_input_attrs('vacunas')),
        }
