# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpRequest, JsonResponse
from rest_framework import viewsets

from .models import Corpus, Transcript, UploadFile
from .serializers import (CorpusSerializer, TranscriptSerializer,
                          UploadFileSerializer)


class UploadFileViewSet(viewsets.ModelViewSet):
    queryset = UploadFile.objects.all()
    serializer_class = UploadFileSerializer


class TranscriptViewSet(viewsets.ModelViewSet):
    queryset = Transcript.objects.all()
    serializer_class = TranscriptSerializer


class CorpusViewSet(viewsets.ModelViewSet):
    queryset = Corpus.objects.all()
    serializer_class = CorpusSerializer


def upload(request: HttpRequest):
    file = UploadFile()
    # file.user = TODO
    file.content = request.FILES['content']
    file.name = request.POST['name']
    file.filename = request.POST['filename']
    file.status = 'pending'
    file.save()

    return JsonResponse({
        'name': file.name
    })
