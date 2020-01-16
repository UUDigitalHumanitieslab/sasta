# -*- coding: utf-8 -*-
from __future__ import unicode_literals
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
