from django.contrib import admin

# Register your models here.
from src.apps.adopcion.models import Persona


@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellidos', 'edad', 'telefono', 'email', 'domicilio')
    list_filter = ('nombre', 'apellidos')
    ordering = ('-nombre', '-apellidos')
