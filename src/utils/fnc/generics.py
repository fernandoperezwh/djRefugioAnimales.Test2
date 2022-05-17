import copy

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework import status


def generic_api_delete(request, strategy, instance, tpl_name, redirect, custom_messages={}):
    DEFAULT_SUCCESS_MESSAGE = "Se elimino el registro correctamente."

    if request.method == "POST":
        request_copy = copy.copy(request)
        request_copy.method = 'DELETE'
        response = strategy.exec(request_copy, pk=instance.data.get('id'))

        if response.status_code != status.HTTP_204_NO_CONTENT:
            messages.success(request, custom_messages.get('error') or DEFAULT_SUCCESS_MESSAGE)
            return HttpResponseRedirect(redirect)

        # En este punto estamos seguros que se borro el registro e informamos al cliente
        messages.success(request, custom_messages.get('success') or DEFAULT_SUCCESS_MESSAGE)
        return HttpResponseRedirect(redirect)
    return render(request, tpl_name, {
        'object': instance.data,
        'redirect': redirect,
    })
