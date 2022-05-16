import copy

from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, TemplateView
from requests import ConnectTimeout
from rest_framework import status

from src.apps.mascota.forms import VacunaForm, MascotaForm
from src.apps.mascota.models import Vacuna
from src.apps.mascota.utils.views_strategies import RefugioStrategies
from src.utils.classes.refugio_requests import RefugioRequests
from src.utils.constants import APIResource
from src.utils.fnc.generics import generic_api_delete


# region vacunas views
class VacunaApiListView(ListView):
    model = Vacuna
    template_name = "mascota__vacuna_listado.html"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        refugio_strategy = RefugioStrategies()
        self.__strategy = refugio_strategy.list(APIResource.VACUNAS)

    def get_info_via_api(self):
        return self.__strategy.exec(request=self.request)

    def get_queryset(self):
        return self.get_info_via_api()

    def get_context_data(self, **kwargs):
        context = super(VacunaApiListView, self).get_context_data(**kwargs)
        context['create_url'] = 'vacuna_new_api'
        context['edit_url'] = 'vacuna_edit_api'
        context['delete_url'] = 'vacuna_delete_api'
        return context

    def get(self, *args, **kwargs):
        if self.get_queryset() is None:
            return HttpResponseRedirect(reverse('home'))
        return super(VacunaApiListView, self).get(*args, **kwargs)


def vacuna_form_api(request, _id=None):
    RETURN_URL = 'vacuna_list_api'

    # region instancias de strategias
    refugio_strategy = RefugioStrategies()
    retrieve_strategy = refugio_strategy.retrieve(APIResource.VACUNAS)
    create_strategy = refugio_strategy.create(APIResource.VACUNAS)
    update_strategy = refugio_strategy.update(APIResource.VACUNAS)
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

    form = VacunaForm(initial=initial) if initial else VacunaForm()

    # Update/create
    if request.method == "POST":
        form = VacunaForm(request.POST, initial=initial)
        if form.is_valid():
            # region Editar registro de una vacuna
            if initial:
                request_copy = copy.copy(request)
                request_copy.method = 'PUT'
                response = update_strategy.exec(request_copy, pk=_id, data=form.cleaned_data)
            # endregion
            # region Crear registro de una vacuna
            else:
                request_copy = copy.copy(request)
                request_copy.method = 'POST'
                response = create_strategy.exec(request_copy, data=form.cleaned_data)
            # endregion

            # Se verifica si la api pudo actualizar/crear los datos de la vacuna
            if response is None:
                messages.error(request, 'Un error ha ocurrido intentando aplicar la accion sobre la vacuna '
                                        '<strong>{name}</strong>'
                                        ''.format(name=form.cleaned_data.get('nombre')))
                return HttpResponseRedirect(reverse(RETURN_URL))
            # Si no ocurrio ningun error durante el intento de crear o eliminar, se manda el mensaje de exito
            messages.success(request, 'Se ha realizado con exito la accion sobre la vacuna <strong>{name}</strong>'
                                      ''.format(name=form.cleaned_data.get('nombre')))
            return HttpResponseRedirect(reverse(RETURN_URL))

    return render(request, "mascota__vacuna_form.html", {
        "form": form,
    })


def vacuna_delete_api(request, _id):
    RETURN_URL = 'vacuna_list_api'

    # region instancias de strategias
    refugio_strategy = RefugioStrategies()
    retrieve_strategy = refugio_strategy.retrieve(APIResource.VACUNAS)
    delete_strategy = refugio_strategy.delete(APIResource.VACUNAS)
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
        tpl_name="mascota__vacuna_delete.html",
        redirect=reverse(RETURN_URL),
        custom_messages={
            'success': 'Se elimino el registro de: <strong>{}</strong>'.format(instance.get('nombre')),
            'error': 'Un error ha ocurrido intentando eliminar el registro de: <strong>{}</strong>'
                     ''.format(instance.get('nombre')),
        }
    )
# endregion


# region mascotas views
class MascotaApiListView(ListView):
    model = Vacuna
    template_name = "mascota__mascota_listado.html"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        refugio_strategy = RefugioStrategies()
        self.__strategy = refugio_strategy.list(APIResource.MASCOTAS)

    def get_info_via_api(self):
        return self.__strategy.exec(request=self.request)

    def get_queryset(self):
        return self.get_info_via_api()

    def get_context_data(self, **kwargs):
        context = super(MascotaApiListView, self).get_context_data(**kwargs)
        context['create_url'] = 'mascota_new_api'
        context['edit_url'] = 'mascota_edit_api'
        context['delete_url'] = 'mascota_delete_api'
        context['owner_detail'] = 'mascota_persona_api'
        return context

    def get(self, *args, **kwargs):
        if self.get_queryset() is None:
            return HttpResponseRedirect(reverse('home'))
        return super(MascotaApiListView, self).get(*args, **kwargs)


def mascota_form_api(request, _id=None):
    RETURN_URL = 'mascota_list_api'

    # region instancias de strategias
    refugio_strategy = RefugioStrategies()
    retrieve_strategy = refugio_strategy.retrieve(APIResource.MASCOTAS)
    create_strategy = refugio_strategy.create(APIResource.MASCOTAS)
    update_strategy = refugio_strategy.update(APIResource.MASCOTAS)
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
        initial = {
            **response,
            'persona': response.get('persona', {}).get('id'),
            'vacunas': map(lambda vacuna: vacuna.get('id'),
                           response.get('vacunas', list())),
        }
    # endregion

    form = MascotaForm(initial=initial) if initial else MascotaForm()

    # Update/create
    if request.method == "POST":
        form = MascotaForm(request.POST, initial=initial)
        if form.is_valid():
            cleaned_data = {
                **form.cleaned_data,
                'persona': form.cleaned_data.get('persona').id,
                'vacunas': list(map(lambda vacuna: vacuna.id, form.cleaned_data.get('vacunas', []))),
            }
            # region Editar registro de una mascota
            if initial:
                request_copy = copy.copy(request)
                request_copy.method = 'PUT'
                response = update_strategy.exec(request_copy, pk=_id, data=cleaned_data)
            # endregion
            # region Crear registro de una mascota
            else:
                request_copy = copy.copy(request)
                request_copy.method = 'POST'
                response = create_strategy.exec(request_copy, data=cleaned_data)
            # endregion

            # Se verifica si la api pudo actualizar/crear los datos de la mascota
            if response is None:
                messages.error(request, 'Un error ha ocurrido intentando aplicar la accion sobre la mascota '
                                        '<strong>{name}</strong>'
                                        ''.format(name=form.cleaned_data.get('nombre')))
                return HttpResponseRedirect(reverse(RETURN_URL))
            # Si no ocurrio ningun error durante el intento de crear o eliminar, se manda el mensaje de exito
            messages.success(request, 'Se ha realizado con exito la accion sobre la mascota <strong>{name}</strong>'
                                      ''.format(name=form.cleaned_data.get('nombre')))
            return HttpResponseRedirect(reverse(RETURN_URL))

    return render(request, "mascota__mascota_form.html", {
        "form": form,
    })


def mascota_delete_api(request, _id):
    RETURN_URL = 'mascota_list_api'

    # region instancias de strategias
    refugio_strategy = RefugioStrategies()
    retrieve_strategy = refugio_strategy.retrieve(APIResource.MASCOTAS)
    delete_strategy = refugio_strategy.delete(APIResource.MASCOTAS)
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
        tpl_name="mascota__mascota_delete.html",
        redirect=reverse(RETURN_URL),
        custom_messages={
            'success': 'Se elimino el registro de: <strong>{}</strong>'.format(instance.get('nombre')),
            'error': 'Un error ha ocurrido intentando eliminar el registro de: <strong>{}</strong>'
                     ''.format(instance.get('nombre')),
        }
    )


class MascotaPersonaView(TemplateView):
    template_name = 'mascota__detalle_persona.html'

    def get_context_data(self, **kwargs):
        context = super(MascotaPersonaView, self).get_context_data(**kwargs)
        context['object'] = self.__get_info_persona()
        return context

    def __get_info_persona(self):
        data = None
        api_request = RefugioRequests()
        try:
            response = api_request.get('/api/mascotas/{mascota_id}/persona/'.format(mascota_id=self.args[0]),
                                       cookies=self.request.COOKIES)
            if response.status_code == status.HTTP_200_OK:
                data = response.json()
        except (ConnectionError, ConnectTimeout) as err:
            pass
        return data
# endregion
