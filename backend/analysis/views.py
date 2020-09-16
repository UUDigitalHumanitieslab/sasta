# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q
from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from analysis.query.run import query_transcript
from analysis.query.xlsx_output import v1_to_xlsx, v2_to_xlsx

from .convert.convert import convert
from .models import AssessmentMethod, Corpus, Transcript, UploadFile, MethodCategory
from .parse.parse import parse_and_create
from .serializers import (AssessmentMethodSerializer, CorpusSerializer,
                          MethodCategorySerializer, TranscriptSerializer,
                          UploadFileSerializer)

# flake8: noqa: E501


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

        allresults, queries_with_funcs = query_transcript(transcript, method)

        spreadsheet = v1_to_xlsx(allresults, queries_with_funcs)
        spreadsheet.save(response)

        return response

    @action(detail=True, methods=['POST'], name='Annotate')
    def annotate(self, request, *args, **kwargs):
        transcript = self.get_object()
        method_name = request.data.get('method')

        only_inform = request.data.get('only_inform') == 'true'
        method = AssessmentMethod.objects.filter(name=method_name).first()
        zc_embed = method.category.zc_embeddings

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = "attachment; filename=saf_output.xlsx"

        allresults, queries_with_funcs = query_transcript(
            transcript, method, True, zc_embed, only_inform)

        spreadsheet = v2_to_xlsx(allresults, zc_embeddings=zc_embed)
        spreadsheet.save(response)

        return response

    @action(detail=True, methods=['GET'], name='toCHAT')
    def toCHAT(self, request, *args, **kwargs):
        transcript = self.get_object()
        if transcript.status == 'converted':
            return Response(self.get_serializer(transcript).data)
        result = convert(transcript)
        if result:
            return Response(self.get_serializer(result).data)
        return Response(None, status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET'], name='parse')
    def parse(self, request, *args, **kwargs):
        transcript = self.get_object()
        if transcript.status in ('converted', 'parsing-failed'):
            result = parse_and_create(transcript)
            if result:
                return Response(self.get_serializer(result).data)
        if transcript.status == 'parsed':
            return Response(self.get_serializer(transcript).data)

        return Response(None, status.HTTP_400_BAD_REQUEST)


class CorpusViewSet(viewsets.ModelViewSet):
    serializer_class = CorpusSerializer
    queryset = Corpus.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user_queryset = self.queryset.filter(user=self.request.user)
        return user_queryset

    @action(detail=True, methods=['GET'], name='parse_all')
    def convert_all(self, request, *args, **kwargs):
        corpus = self.get_object()
        transcripts = Transcript.objects.filter(
            Q(corpus=corpus),
            Q(status='created') | Q(status='conversion-failed'))

        for t in transcripts:
            res = convert(t)
            if not res:
                return Response('Failed', status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(corpus).data)

    @action(detail=True, methods=['GET'], name='parse_all')
    def parse_all(self, request, *args, **kwargs):
        corpus = self.get_object()
        transcripts = Transcript.objects.filter(
            Q(corpus=corpus),
            Q(status='converted') | Q(status='parsing-failed'))

        for t in transcripts:
            res = parse_and_create(t)
            if not res:
                return Response('Failed', status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(corpus).data)

    @action(detail=True, methods=['POST'], name='download')
    def download(self, request, *args, **kwargs):
        corpus = self.get_object()
        stream = corpus.download_as_zip()
        response = HttpResponse(
            stream.getvalue(), content_type='application/x-zip-compressed')
        response['Content-Disposition'] = f'attachment; filename={corpus.name}.zip'

        return response


class AssessmentMethodViewSet(viewsets.ModelViewSet):
    queryset = AssessmentMethod.objects.all()
    serializer_class = AssessmentMethodSerializer


class MethodCategoryViewSet(viewsets.ModelViewSet):
    queryset = MethodCategory.objects.all()
    serializer_class = MethodCategory
