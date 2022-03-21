# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from io import BytesIO, StringIO

from analysis.annotations.safreader import SAFReader
from analysis.annotations.enrich_chat import enrich_chat
from analysis.query.run import query_transcript
from analysis.query.xlsx_output import v1_to_xlsx, v2_to_xlsx
from convert.chat_writer import ChatWriter
from django.db.models import Q
from django.http import HttpResponse
from parse.parse_utils import parse_and_create
from parse.tasks import parse_transcript_task
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.response import Response

from .convert.convert import convert
from .models import (AnalysisRun, AssessmentMethod, Corpus, MethodCategory,
                     Transcript, UploadFile)
from .permissions import IsCorpusChildOwner, IsCorpusOwner
from .serializers import (AssessmentMethodSerializer, CorpusSerializer,
                          MethodCategorySerializer, TranscriptSerializer,
                          UploadFileSerializer)
from .utils import StreamFile
from celery import group


# flake8: noqa: E501
SPREADSHEET_MIMETYPE = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'


class UploadFileViewSet(viewsets.ModelViewSet):
    queryset = UploadFile.objects.all()
    serializer_class = UploadFileSerializer
    permission_classes = (IsCorpusChildOwner, )

    def get_queryset(self):
        return self.queryset.filter(corpus__user=self.request.user)


class TranscriptViewSet(viewsets.ModelViewSet):
    queryset = Transcript.objects.all()
    serializer_class = TranscriptSerializer
    permission_classes = (IsCorpusChildOwner,)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset.all()
        return self.queryset.filter(corpus__user=self.request.user)

    def create_analysis_run(self, transcript, method, saf, is_manual=False):
        if not isinstance(saf, BytesIO):
            stream = BytesIO()
            saf.save(stream)
        else:
            stream = saf
        run = AnalysisRun(transcript=transcript, method=method, is_manual_correction=is_manual)

        now = datetime.datetime.now()
        stamp = now.strftime('%Y%m%d_%H%M')

        filename = f'{transcript.name}_{stamp}_saf.xlsx'
        run.annotation_file.save(filename, StreamFile(stream))
        run.save()
        return run

    @ action(detail=True, methods=['POST'], name='Score transcript')
    def query(self, request, *args, **kwargs):
        transcript = self.get_object()
        method_id = request.data.get('method')
        method = AssessmentMethod.objects.get(pk=method_id)

        response = HttpResponse(
            content_type=SPREADSHEET_MIMETYPE)
        response['Content-Disposition'] = "attachment; filename=matches_output.xlsx"

        allresults, queries_with_funcs = query_transcript(transcript, method)

        spreadsheet = v1_to_xlsx(allresults, queries_with_funcs)
        spreadsheet.save(response)

        return response

    @action(detail=True, methods=['POST'], name='Annotate')
    def annotate(self, request, *args, **kwargs):
        transcript = self.get_object()
        method_id = request.data.get('method')

        method = AssessmentMethod.objects.get(pk=method_id)
        zc_embed = method.category.zc_embeddings

        allresults, queries_with_funcs = query_transcript(
            transcript, method, True, zc_embed
        )

        spreadsheet = v2_to_xlsx(allresults, method, zc_embeddings=zc_embed)
        self.create_analysis_run(transcript, method, spreadsheet)

        format = request.data.get('format', 'xlsx')

        if format == 'xlsx':
            spreadsheet = v2_to_xlsx(
                allresults, method, zc_embeddings=zc_embed)

            response = HttpResponse(
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = "attachment; filename=saf_output.xlsx"
            spreadsheet.save(response)

            return response

        if format == 'cha':
            enriched = enrich_chat(transcript, allresults, method)
            output = StringIO()
            writer = ChatWriter(enriched, target=output)
            writer.write()
            output.seek(0)

            response = HttpResponse(
                output.getvalue(), content_type='text/plain')
            response['Content-Disposition'] = "attachment; filename=annotated.cha"

            return response

    @action(detail=True, methods=['GET'], name='Download latest annotation', url_path='annotations/latest')
    def latest_annotations(self, request, *args, **kwargs):
        obj = self.get_object()
        run = AnalysisRun.objects.filter(transcript=obj).latest()

        filename = run.annotation_file.name.split('/')[-1]
        response = HttpResponse(run.annotation_file, content_type=SPREADSHEET_MIMETYPE)
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response

    @action(detail=True, methods=['GET'], name='Reset annotations', url_path='annotations/reset')
    def reset_annotations(self, request, *args, **kwargs):
        obj = self.get_object()
        all_runs = AnalysisRun.objects.filter(transcript=obj)
        all_runs.delete()
        return Response('Success', status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], name='Upload annotations', url_path='annotations/upload')
    def upload_annotations(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            latest_run = AnalysisRun.objects.filter(transcript=obj).latest()
        except AnalysisRun.DoesNotExist:
            return Response('No previous annotations found for this transcript. Run regular annotating at least once before providing corrected input.',
                            status=status.HTTP_400_BAD_REQUEST)

        file = request.FILES['content'].file

        new_run = self.create_analysis_run(obj, latest_run.method, file, is_manual=True)

        try:
            reader = SAFReader(new_run.annotation_file.path, latest_run.method)
        except Exception as e:
            new_run.delete()
            return Response(str(e), status.HTTP_400_BAD_REQUEST)

        if reader.errors:
            new_run.delete()
            return Response(reader.formatted_errors(), status.HTTP_400_BAD_REQUEST)

        return Response('Success', status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], name='Generate form')
    def generateform(self, request, *args, **kwargs):
        transcript = self.get_object()
        method_id = request.data.get('method')
        method = AssessmentMethod.objects.get(pk=method_id)
        zc_embed = method.category.zc_embeddings

        # Find the form function for this method
        form_func = method.category.get_form_function()
        if not form_func:
            raise ParseError(detail='No form definition for this method.')

        allresults, _ = query_transcript(
            transcript, method, annotate=False, zc_embed=zc_embed,
        )

        form = form_func(allresults, None, in_memory=True)
        form.seek(0)
        response = HttpResponse(
            form,
            content_type=SPREADSHEET_MIMETYPE)
        response['Content-Disposition'] = f"attachment; filename={transcript.name}_{method.category.name}_form.xlsx"

        return response

    @action(detail=True, methods=['GET'], name='toCHAT')
    def toCHAT(self, request, *args, **kwargs):
        transcript = self.get_object()
        if transcript.status == Transcript.CONVERTED:
            return Response(self.get_serializer(transcript).data)
        result = convert(transcript)
        if result:
            return Response(self.get_serializer(result).data)
        return Response(None, status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET'], name='parse')
    def parse(self, request, *args, **kwargs):
        transcript = self.get_object()
        if transcript.status in (Transcript.CONVERTED, Transcript.PARSING_FAILED):
            result = parse_and_create(transcript)
            if result:
                return Response(self.get_serializer(result).data)
        if transcript.status == Transcript.PARSED:
            return Response(self.get_serializer(transcript).data)

        return Response(None, status.HTTP_400_BAD_REQUEST)


class CorpusViewSet(viewsets.ModelViewSet):
    serializer_class = CorpusSerializer
    queryset = Corpus.objects.all()
    permission_classes = (IsCorpusOwner, )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset.all()
        return self.queryset.filter(user=self.request.user)

    @action(detail=True, methods=['GET'], name='convert_all')
    def convert_all(self, request, *args, **kwargs):
        corpus = self.get_object()
        transcripts = Transcript.objects.filter(
            Q(corpus=corpus),
            Q(status=Transcript.CREATED) | Q(status=Transcript.CONVERSION_FAILED))

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
            Q(status=Transcript.CONVERTED) | Q(status=Transcript.PARSING_FAILED))
        for t in transcripts:
            res = parse_and_create(t)
            if not res:
                return Response('Failed', status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(corpus).data)

    @action(detail=True, methods=['GET'], name='parse_all_async')
    def parse_all_async(self, request, *args, **kwargs):
        corpus = self.get_object()
        transcripts = Transcript.objects.filter(
            Q(corpus=corpus), Q(status=Transcript.CONVERTED) | Q(status=Transcript.PARSING_FAILED)
        )
        task = group(parse_transcript_task.s(t.id) for t in transcripts).delay()

        if not task:
            return Response('Failed to create task', status.HTTP_400_BAD_REQUEST)
        return Response(task.id)

    @action(detail=True, methods=['POST'], name='download')
    def download(self, request, *args, **kwargs):
        corpus = self.get_object()
        stream = corpus.download_as_zip()
        response = HttpResponse(
            stream.getvalue(), content_type='application/x-zip-compressed')
        response['Content-Disposition'] = f'attachment; filename={corpus.name}.zip'

        return response

    @action(detail=True, methods=['POST'], name='setdefaultmethod')
    def defaultmethod(self, request, *args, **kwargs):
        corpus = self.get_object()
        method_id = request.data.get('method')
        if method_id == 'null':
            method = None
        else:
            method = AssessmentMethod.objects.get(pk=method_id)
        corpus.default_method = method
        corpus.save()
        return Response('Succes')


class AssessmentMethodViewSet(viewsets.ModelViewSet):
    queryset = AssessmentMethod.objects.all()
    serializer_class = AssessmentMethodSerializer


class MethodCategoryViewSet(viewsets.ModelViewSet):
    queryset = MethodCategory.objects.all()
    serializer_class = MethodCategorySerializer
