import copy

from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, TemplateView
from rest_framework import status

from src.apps.mascota.forms import VacunaForm, MascotaForm
from src.apps.mascota.models import Vacuna
from src.apps.mascota.utils.views_strategies.refugio_strategies import RefugioStrategies
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
        response = self.__strategy.exec(request=self.request)
        return response.data

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
        if response.status_code == status.HTTP_404_NOT_FOUND:
            raise Http404
        initial = response.data
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

            # Se verifica algun error con el envio del formulario
            if response.status_code == status.HTTP_400_BAD_REQUEST and response.errors:
                for field in response.errors.keys():
                    if field == 'non_field_errors':
                        form.add_error('__all__', response.errors.get(field)[0])
                        continue
                    form.add_error(field, response.errors.get(field)[0])
                return render(request, "mascota__vacuna_form.html", {
                    "form": form,
                })

            # Se verifica algun error 500 o algo raro
            if response.status_code is None or response.status_code >= status.HTTP_500_INTERNAL_SERVER_ERROR:
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
    if instance.status_code == status.HTTP_404_NOT_FOUND:
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
            'success': 'Se elimino el registro de: <strong>{}</strong>'.format(instance.data.get('nombre')),
            'error': 'Un error ha ocurrido intentando eliminar el registro de: <strong>{}</strong>'
                     ''.format(instance.data.get('nombre')),
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
        response = self.__strategy.exec(request=self.request)
        return response.data

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
        if response.status_code == status.HTTP_404_NOT_FOUND:
            raise Http404
        initial = {
            **response.data,
            'persona': response.data.get('persona', {}).get('id'),
            'vacunas': map(lambda vacuna: vacuna.get('id'),
                           response.data.get('vacunas', list())),
        }
    # endregion

    form = MascotaForm(initial=initial) if initial else MascotaForm()

    # Update/create
    if request.method == "POST":
        form = MascotaForm(request.POST, initial=initial)
        if form.is_valid():
            cleaned_data = {
                **form.cleaned_data,
                'persona': form.cleaned_data.get('persona').id if form.cleaned_data.get('persona') else None,
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

            # Se verifica algun error con el envio del formulario
            if response.status_code == status.HTTP_400_BAD_REQUEST and response.errors:
                for field in response.errors.keys():
                    if field == 'non_field_errors':
                        form.add_error('__all__', response.errors.get(field)[0])
                        continue
                    form.add_error(field, response.errors.get(field)[0])
                return render(request, "mascota__mascota_form.html", {
                    "form": form,
                })

            # Se verifica algun error 500 o algo raro
            if response.status_code is None or response.status_code >= status.HTTP_500_INTERNAL_SERVER_ERROR:
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
    if instance.status_code == status.HTTP_404_NOT_FOUND:
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
            'success': 'Se elimino el registro de: <strong>{}</strong>'.format(instance.data.get('nombre')),
            'error': 'Un error ha ocurrido intentando eliminar el registro de: <strong>{}</strong>'
                     ''.format(instance.data.get('nombre')),
        }
    )


class MascotaPersonaView(TemplateView):
    template_name = 'mascota__detalle_persona.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        refugio_strategy = RefugioStrategies()
        self.__strategy = refugio_strategy.retrieve(APIResource.MASCOTAS_PERSONAS)

    def get_context_data(self, **kwargs):
        context = super(MascotaPersonaView, self).get_context_data(**kwargs)
        response = self.__strategy.exec(request=self.request, pk=self.args[0])
        if response.status_code == status.HTTP_404_NOT_FOUND:
            raise Http404
        context['object'] = response.data
        return context
# endregion
