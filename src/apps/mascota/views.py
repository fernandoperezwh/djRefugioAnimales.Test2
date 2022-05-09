from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, TemplateView
from requests import ConnectTimeout
from rest_framework import status

from src.apps.mascota.forms import VacunaForm, MascotaForm
from src.apps.mascota.models import Vacuna
from src.utils.classes.refugio_requests import RefugioRequests
from src.utils.fnc.generics import generic_api_delete


# region vacunas views
class VacunaApiListView(ListView):
    endpoint = '/api/vacunas/'
    model = Vacuna
    template_name = "mascota__vacuna_listado.html"
    api_request = RefugioRequests()

    def get_queryset(self):
        return self.get_info_via_api()

    def get_context_data(self, **kwargs):
        context = super(VacunaApiListView, self).get_context_data(**kwargs)
        context['create_url'] = 'vacuna_new_api'
        context['edit_url'] = 'vacuna_edit_api'
        context['delete_url'] = 'vacuna_delete_api'
        return context

    def get_endpoint(self, search_query=None):
        return self.endpoint

    def get_info_via_api(self, search_query=None):
        data = None
        try:
            endpoint = self.get_endpoint(search_query)
            response = self.api_request.get(endpoint, cookies=self.request.COOKIES)
            if response.status_code == status.HTTP_200_OK:
                data = response.json()
        except (ConnectionError, ConnectTimeout) as err:
            pass
        return data

    def get(self, *args, **kwargs):
        if self.get_queryset() is None:
            return HttpResponseRedirect(reverse('home'))
        return super(VacunaApiListView, self).get(*args, **kwargs)


def vacuna_form_api(request, _id=None):
    RETURN_URL = 'vacuna_list_api'
    initial = {}
    api_request = RefugioRequests()
    # Se verifica la existencia
    if _id:
        try:
            endpoint = '/api/vacunas/{id}/'.format(id=_id)
            response = api_request.get(endpoint, cookies=request.COOKIES)
            if response.status_code != 200:
                raise Http404
            initial = response.json()
        except (ConnectionError, ConnectTimeout) as err:
            messages.error(request, 'Un error a ocurrido consultando los datos de la vacuna con id: {id}'
                                    ''.format(id=_id))
            return HttpResponseRedirect(reverse('vacuna_list_api'))

    form = VacunaForm(initial=initial) if initial else VacunaForm()

    # Update/create
    if request.method == "POST":
        form = VacunaForm(request.POST, initial=initial)
        if form.is_valid():
            try:
                if initial:
                    # Editar registro de una vacuna
                    response = api_request.put('api/vacunas/{id}/'.format(id=_id), data=form.cleaned_data,
                                            cookies=request.COOKIES)
                else:
                    # Crear registro de una vacuna
                    response = api_request.post('api/vacunas/', data=form.cleaned_data, cookies=request.COOKIES)

            except (ConnectionError, ConnectTimeout) as err:
                messages.error(request, 'Un error desconocido ha ocurrido intentando aplicar la accion sobre la '
                                        'vacuna <strong>{name}</strong>'
                                        ''.format(name=form.cleaned_data.get('nombre')))
                return HttpResponseRedirect(reverse(RETURN_URL))

            # Se verifica si la api pudo actualizar/crear los datos de la vacuna
            if response.status_code not in (200, 201):
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
    endpoint = '/api/vacunas/{id}/'.format(id=_id)
    api_request = RefugioRequests()
    # Se intenta obtener el registro a eliminar
    try:
        response = api_request.get(endpoint, cookies=request.COOKIES)
        if response.status_code != 200:
            raise Http404
        instance = response.json()
    except (ConnectionError, ConnectTimeout) as err:
        messages.error(request, 'Un error a ocurrido consultando los datos de la vacuna con id: {id}'
                                ''.format(id=_id))
        return HttpResponseRedirect(reverse(RETURN_URL))
    # Se manda a llamar las instrucciones genericas para eliminar en base al funcionamiento del api
    return generic_api_delete(
        request=request,
        endpoint=endpoint,
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


# region vacunas views
class MascotaApiListView(ListView):
    endpoint = '/api/mascotas/'
    model = Vacuna
    template_name = "mascota__mascota_listado.html"
    api_request = RefugioRequests()

    def get_queryset(self):
        return self.get_info_via_api()

    def get_context_data(self, **kwargs):
        context = super(MascotaApiListView, self).get_context_data(**kwargs)
        context['create_url'] = 'mascota_new_api'
        context['edit_url'] = 'mascota_edit_api'
        context['delete_url'] = 'mascota_delete_api'
        context['owner_detail'] = 'mascota_persona_api'
        return context

    def get_endpoint(self, search_query=None):
        return self.endpoint

    def get_info_via_api(self, search_query=None):
        data = None
        try:
            endpoint = self.get_endpoint(search_query)
            response = self.api_request.get(endpoint, cookies=self.request.COOKIES)
            if response.status_code == status.HTTP_200_OK:
                data = response.json()
        except (ConnectionError, ConnectTimeout) as err:
            pass
        return data

    def get(self, *args, **kwargs):
        if self.get_queryset() is None:
            return HttpResponseRedirect(reverse('home'))
        return super(MascotaApiListView, self).get(*args, **kwargs)


def mascota_form_api(request, _id=None):
    RETURN_URL = 'mascota_list_api'
    initial = {}
    api_request = RefugioRequests()
    # Se verifica la existencia
    if _id:
        try:
            endpoint = '/api/mascotas/{id}/'.format(id=_id)
            response = api_request.get(endpoint, cookies=request.COOKIES)
            if response.status_code != 200:
                raise Http404
            initial = response.json()
            initial = {
                **initial,
                'persona': initial.get('persona', {}).get('id'),
                'vacunas': map(lambda vacuna: vacuna.get('id'),
                               initial.get('vacunas', list())),
            }
        except (ConnectionError, ConnectTimeout) as err:
            messages.error(request, 'Un error a ocurrido consultando los datos de la vacuna con id: {id}'
                                    ''.format(id=_id))
            return HttpResponseRedirect(reverse('mascota_list_api'))

    form = MascotaForm(initial=initial) if initial else MascotaForm()

    # Update/create
    if request.method == "POST":
        form = MascotaForm(request.POST, initial=initial)
        if form.is_valid():
            try:
                # Obtnemos el valor de cleaned data y sobreescribimos los valores para persona y vacunas
                cleaned_data = {
                    **form.cleaned_data,
                    'persona': form.cleaned_data.get('persona').id,
                    'vacunas': list(map(lambda vacuna: vacuna.id, form.cleaned_data.get('vacunas', []))),
                }
                if initial:
                    # Editar registro de una vacuna
                    response = api_request.put('api/mascotas/{id}/'.format(id=_id), data=cleaned_data,
                                               cookies=request.COOKIES)
                else:
                    # Crear registro de una vacuna
                    response = api_request.post('api/mascotas/', data=cleaned_data, cookies=request.COOKIES)

            except (ConnectionError, ConnectTimeout) as err:
                messages.error(request, 'Un error desconocido ha ocurrido intentando aplicar la accion sobre la '
                                        'mascota <strong>{name}</strong>'
                                        ''.format(name=form.cleaned_data.get('nombre')))
                return HttpResponseRedirect(reverse(RETURN_URL))

            # Se verifica si la api pudo actualizar/crear los datos de la vacuna
            if response.status_code not in (200, 201):
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
    endpoint = '/api/mascotas/{id}/'.format(id=_id)
    api_request = RefugioRequests()
    # Se intenta obtener el registro a eliminar
    try:
        response = api_request.get(endpoint, cookies=request.COOKIES)
        if response.status_code != 200:
            raise Http404
        instance = response.json()
    except (ConnectionError, ConnectTimeout) as err:
        messages.error(request, 'Un error a ocurrido consultando los datos de la mascota con id: {id}'
                                ''.format(id=_id))
        return HttpResponseRedirect(reverse(RETURN_URL))
    # Se manda a llamar las instrucciones genericas para eliminar en base al funcionamiento del api
    return generic_api_delete(
        request=request,
        endpoint=endpoint,
        instance=instance,
        tpl_name="mascota__vacuna_delete.html",
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
