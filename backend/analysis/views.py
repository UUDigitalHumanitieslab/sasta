# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from os import path, remove

from django.http import HttpRequest, JsonResponse

from .convert.chat_converter import SifReader
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


def convert(request: HttpRequest):
    file = File.objects.filter(name=request.POST['name']).first()
    input_path = file.content.name
    output_path = input_path.replace(
        '/uploads/', '/converted/').replace('.txt', '.cha')

    reader = SifReader(input_path)
    reader.document.write_chat(output_path)

    return JsonResponse({
        'msg': 'converted'
    })


def delete(request: HttpRequest):
    file = File.objects.filter(name=request.POST['name']).first()
    remove(file.content.name)
    file.delete()
    return JsonResponse({
        'msg': 'deleted'
    })
