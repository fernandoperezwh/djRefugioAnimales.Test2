import copy

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render


def generic_api_delete(request, strategy, instance, tpl_name, redirect, custom_messages={}):
    DEFAULT_SUCCESS_MESSAGE = "Se elimino el registro correctamente."

    if request.method == "POST":
        request_copy = copy.copy(request)
        request_copy.method = 'DELETE'
        strategy.exec(request_copy, pk=instance.get('id'))

        # En este punto estamos seguros que se borro el registro e informamos al cliente
        messages.success(request, custom_messages.get('success') or DEFAULT_SUCCESS_MESSAGE)
        return HttpResponseRedirect(redirect)
    return render(request, tpl_name, {
        'object': instance,
        'redirect': redirect,
    })
