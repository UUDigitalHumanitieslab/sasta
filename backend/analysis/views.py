# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpRequest, JsonResponse
from django.shortcuts import render

from .convert.CHAT_converter import CHATConverter
from .models import File


from os import path


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
    convert = CHATConverter(input_path, output_path)
    convert.read()

    return JsonResponse({
        'msg': 'joe'
    })
