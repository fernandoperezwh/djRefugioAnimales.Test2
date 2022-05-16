import copy

from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.views.generic import ListView
from requests import ConnectionError, ConnectTimeout

from src.apps.adopcion.models import Persona
from src.apps.adopcion.forms import PersonaForm
from src.apps.mascota.utils.views_strategies import RefugioStrategies
from src.utils.classes.refugio_requests import RefugioRequests
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
        return self.__strategy.exec(request=self.request)

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
        if response is None:
            raise Http404
        initial = response
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

            # Se verifica si la api pudo actualizar/crear los datos de la persona
            if response is None:
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
    if instance is None:
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
                       ''.format(instance.get('nombre'), instance.get('apellidos')),
            'error': 'Un error ha ocurrido intentando eliminar el registro de: <strong>{} {}</strong>'
                     ''.format(instance.get('nombre'), instance.get('apellidos')),
        }
    )
# endregion
