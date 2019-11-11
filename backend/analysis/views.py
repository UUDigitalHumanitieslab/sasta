# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from os import path
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


def list(request: HttpRequest):
    files = [{
        'name': file.name,
        'file_name': path.basename(file.content.name),
        'status': file.status
    } for file in File.objects.all()]
    return JsonResponse({
        'files': files
    })
