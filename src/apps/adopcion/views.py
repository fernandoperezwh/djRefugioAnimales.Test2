import copy

from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.views.generic import ListView
from rest_framework import status

from src.apps.adopcion.models import Persona
from src.apps.adopcion.forms import PersonaForm
from src.apps.mascota.utils.views_strategies.refugio_strategies import RefugioStrategies
from src.utils.constants import APIResource
from src.utils.fnc.generics import generic_api_delete


# region persona - API Clase based views
class PersonaApiListView(ListView):
    model = Persona
    template_name = "adopcion__persona_listado.html"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        refugio_strategy = RefugioStrategies()
        self.__strategy = refugio_strategy.list(APIResource.PERSONAS)

    def get_info_via_api(self):
        response = self.__strategy.exec(request=self.request)
        return response.data

    def get_queryset(self):
        return self.get_info_via_api()

    def get_context_data(self, **kwargs):
        context = super(PersonaApiListView, self).get_context_data(**kwargs)
        context['create_url'] = 'persona_new_api'
        context['edit_url'] = 'persona_edit_api'
        context['delete_url'] = 'persona_delete_api'
        return context

    def get(self, *args, **kwargs):
        if self.get_queryset() is None:
            return HttpResponseRedirect(reverse('home'))
        return super(PersonaApiListView, self).get(*args, **kwargs)


def persona_form_api(request, _id=None):
    RETURN_URL = 'persona_list_api'

    # region instancias de strategias
    refugio_strategy = RefugioStrategies()
    retrieve_strategy = refugio_strategy.retrieve(APIResource.PERSONAS)
    create_strategy = refugio_strategy.create(APIResource.PERSONAS)
    update_strategy = refugio_strategy.update(APIResource.PERSONAS)
    # endregion

    initial = {}
    # region se verifica la existencia del objeto si se pasa un id
    if _id:
        # Se realiza una copia del request ya que el metodo por instancias necesita saber el metodo en el
        #  request, al ser un metodo POST de Django va a intentar crear siempre un registro, pero quizas queremos
        #  leer (GET) o editar (POST)
        request_copy = copy.copy(request)
        request_copy.method = 'GET'
        response = retrieve_strategy.exec(request_copy, pk=_id)
        if response.status_code == status.HTTP_404_NOT_FOUND:
            raise Http404
        initial = response.data
    # endregion

    form = PersonaForm(initial=initial) if initial else PersonaForm()

    # Update/create
    if request.method == "POST":
        form = PersonaForm(request.POST, initial=initial)
        if form.is_valid():
            # region Editar registro de una persona
            if initial:
                request_copy = copy.copy(request)
                request_copy.method = 'PUT'
                response = update_strategy.exec(request_copy, pk=_id, data=form.cleaned_data)
            # endregion
            # region Crear registro de una persona
            else:
                request_copy = copy.copy(request)
                request_copy.method = 'POST'
                response = create_strategy.exec(request_copy, data=form.cleaned_data)
            # endregion

            # Se verifica algun error con el envio del formulario
            if response.status_code == status.HTTP_400_BAD_REQUEST and response.errors:
                for field in response.errors.keys():
                    if field == 'non_field_errors':
                        form.add_error('__all__', response.errors.get(field)[0])
                        continue
                    form.add_error(field, response.errors.get(field)[0])
                return render(request, "adopcion__persona_form.html", {
                    "form": form,
                })

            # Se verifica algun error 500 o algo raro
            if response.status_code is None or response.status_code >= status.HTTP_500_INTERNAL_SERVER_ERROR:
                messages.error(request, 'Un error ha ocurrido intentando aplicar la accion sobre la persona '
                                        '<strong>{first_name} {last_name}</strong>'
                                        ''.format(first_name=form.cleaned_data.get('nombre'),
                                                  last_name=form.cleaned_data.get('apellidos')))
                return HttpResponseRedirect(reverse(RETURN_URL))
            # Si no ocurrio ningun error durante el intento de crear o eliminar, se manda el mensaje de exito
            messages.success(request, 'Se ha realizado con exito la accion sobre la persona <strong>{first_name} '
                                      '{last_name}</strong>'
                                      ''.format(first_name=form.cleaned_data.get('nombre'),
                                                last_name=form.cleaned_data.get('apellidos')))
            return HttpResponseRedirect(reverse(RETURN_URL))

    return render(request, "adopcion__persona_form.html", {
        "form": form,
    })


def persona_delete_api(request, _id):
    RETURN_URL = 'persona_list_api'

    # region instancias de strategias
    refugio_strategy = RefugioStrategies()
    retrieve_strategy = refugio_strategy.retrieve(APIResource.PERSONAS)
    delete_strategy = refugio_strategy.delete(APIResource.PERSONAS)
    # endregion

    # region se intenta obtener el registro a eliminar
    request_copy = copy.copy(request)
    request_copy.method = 'GET'
    instance = retrieve_strategy.exec(request_copy, pk=_id)
    if instance.status_code == status.HTTP_404_NOT_FOUND:
        raise Http404
    # endregion

    # Se manda a llamar las instrucciones genericas para eliminar en base al funcionamiento del api
    return generic_api_delete(
        request=request,
        strategy=delete_strategy,
        instance=instance,
        tpl_name="adopcion__persona_delete.html",
        redirect=reverse(RETURN_URL),
        custom_messages={
            'success': 'Se elimino el registro de: <strong>{} {}</strong>'
                       ''.format(instance.data.get('nombre'), instance.data.get('apellidos')),
            'error': 'Un error ha ocurrido intentando eliminar el registro de: <strong>{} {}</strong>'
                     ''.format(instance.data.get('nombre'), instance.data.get('apellidos')),
        }
    )
# endregion
