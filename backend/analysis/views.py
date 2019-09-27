# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpRequest, JsonResponse

from .models import File


def upload(request: HttpRequest):
    file = File()
    # file.user = TODO
    file.content = request.FILES['content']
    file.name = request.POST['name']
    file.filename = request.POST['filename']
    file.status = 'pending'
    file.save()

    return JsonResponse({
        'name': file.name
    })
