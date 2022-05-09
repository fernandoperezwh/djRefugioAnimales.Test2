from django import forms

from src.apps.adopcion.models import Persona
from src.utils.fnc.build_form_input_attrs import build_form_input_attrs


class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ('nombre', 'apellidos', 'edad', 'telefono', 'email', 'domicilio')
        widgets = {
            'nombre': forms.TextInput(attrs=build_form_input_attrs('nombre')),
            'apellidos': forms.TextInput(attrs=build_form_input_attrs('apellidos')),
            'edad': forms.NumberInput(attrs=build_form_input_attrs('edad')),
            'telefono': forms.TextInput(attrs=build_form_input_attrs('telefono')),
            'email': forms.EmailInput(attrs=build_form_input_attrs('email')),
            'domicilio': forms.TextInput(attrs=build_form_input_attrs('domicilio')),
        }
