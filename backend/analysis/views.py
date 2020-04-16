# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action

from .models import AssessmentMethod, Corpus, Transcript, UploadFile
from .score.run_queries import annotate_transcript, query_transcript
from .serializers import (AssessmentMethodSerializer, CorpusSerializer,
                          TranscriptSerializer, UploadFileSerializer)
from .utils import v1_to_xlsx, v2_to_xlsx


class UploadFileViewSet(viewsets.ModelViewSet):
    queryset = UploadFile.objects.all()
    serializer_class = UploadFileSerializer


class TranscriptViewSet(viewsets.ModelViewSet):
    queryset = Transcript.objects.all()
    serializer_class = TranscriptSerializer

    @action(detail=True, methods=['POST'], name='Score transcript')
    def score(self, request, *args, **kwargs):
        transcript = self.get_object()
        method_name = request.data.get('method')
        method = AssessmentMethod.objects.filter(name=method_name).first()

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = "attachment; filename=matches_output.xlsx"

        v1res = query_transcript(transcript, method)
        spreadsheet = v1_to_xlsx(v1res)
        spreadsheet.save(response)

        return response

    @action(detail=True, methods=['POST'], name='Annotate')
    def annotate(self, request, *args, **kwargs):
        transcript = self.get_object()
        method_name = request.data.get('method')
        method = AssessmentMethod.objects.filter(name=method_name).first()
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = "attachment; filename=saf_output.xlsx"

        v2res = annotate_transcript(transcript, method)
        spreadsheet = v2_to_xlsx(v2res)
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
