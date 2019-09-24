# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpRequest

from .models import File


def upload(request: HttpRequest):
    file = File()
    # file.user = TODO
    file.name = request.POST['name']
    file.physical_filepath = request.POST['physical_filepath']
    file.filename = request.POST['filename']
    file.status = request.POST['status']
    file.save()
