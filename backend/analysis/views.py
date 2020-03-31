# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import AssessmentMethod, Corpus, Transcript, UploadFile
from .serializers import (AssessmentMethodSerializer, CorpusSerializer, TranscriptSerializer,
                          UploadFileSerializer)

from django.http import HttpRequest, JsonResponse, HttpResponse

from .score.run_queries import query_transcript, v1_to_xlsx, v2_to_xlsx, annotate_transcript


class UploadFileViewSet(viewsets.ModelViewSet):
    queryset = UploadFile.objects.all()
    serializer_class = UploadFileSerializer


class TranscriptViewSet(viewsets.ModelViewSet):
    queryset = Transcript.objects.all()
    serializer_class = TranscriptSerializer

    @action(detail=True, methods=['POST'], name='Score transcript')
    def score(self, request, *args, **kwargs):
        transcript = self.get_object()
        method = AssessmentMethod.objects.first()

        v1res = query_transcript(transcript, method)

        return JsonResponse(v1res)

    @action(detail=True, methods=['POST'], name='Annotate')
    def annotate(self, request, *args, **kwargs):
        transcript = self.get_object()
        method = AssessmentMethod.objects.first()

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = "attachment; filename=test.xlsx"

        v2res = annotate_transcript(transcript, method)
        spreadsheet = v2_to_xlsx(v2res, response)
        spreadsheet.save(response)

        return response


class CorpusViewSet(viewsets.ModelViewSet):
    serializer_class = CorpusSerializer
    queryset = Corpus.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user_queryset = self.queryset.filter(user=self.request.user)
        return user_queryset


class AssessmentMethodViewSet(viewsets.ModelViewSet):
    queryset = AssessmentMethod.objects.all()
    serializer_class = AssessmentMethodSerializer
