# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from analysis.query.run import query_transcript
from analysis.query.xlsx_output import v1_to_xlsx, v2_to_xlsx
from django.db.models import Q
from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.views import APIView

from .convert.convert import convert
from .models import (AssessmentMethod, Corpus, MethodCategory, Transcript,
                     UploadFile)
from .parse.parse import parse_and_create
from .permissions import IsCorpusChildOwner, IsCorpusOwner
from .serializers import (AssessmentMethodSerializer, CorpusSerializer,
                          MethodCategorySerializer, TranscriptSerializer,
                          UploadFileSerializer)

# flake8: noqa: E501


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
        return self.queryset.filter(corpus__user=self.request.user)

    @action(detail=True, methods=['POST'], name='Score transcript')
    def query(self, request, *args, **kwargs):
        transcript = self.get_object()
        method_id = request.data.get('method')
        method = AssessmentMethod.objects.get(pk=method_id)

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
        method_id = request.data.get('method')

        only_inform = request.data.get('only_inform') == 'true'
        method = AssessmentMethod.objects.get(pk=method_id)
        zc_embed = method.category.zc_embeddings

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = "attachment; filename=saf_output.xlsx"

        allresults, queries_with_funcs = query_transcript(
            transcript, method, True, zc_embed, only_inform
        )

        spreadsheet = v2_to_xlsx(allresults, method, zc_embeddings=zc_embed)
        spreadsheet.save(response)

        return response

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
            transcript, method, False, zc_embed, False
        )

        form = form_func(allresults, None)
        form.seek(0)
        response = HttpResponse(
            form,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
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
        user_queryset = self.queryset.filter(user=self.request.user)
        return user_queryset

    @action(detail=True, methods=['GET'], name='parse_all')
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


class ProcessAllTranscriptsView(APIView):

    def get(self, request):
        to_convert = Transcript.objects.need_converting()
        to_parse = Transcript.objects.need_parsing()

        if (not to_convert) and (not to_parse):
            return Response('Nothing to do.', status=status.HTTP_204_NO_CONTENT)

        if to_convert:
            print(f'Attempting to convert {len(to_convert)} transcripts.')
            for obj in to_convert:
                res = convert(obj)
                if res:
                    print(f'succes for {obj.pk}')
                else:
                    print(f'failure for {obj.pk}')
            return Response(status=status.HTTP_204_NO_CONTENT)

        if to_parse:
            print(f'Attempting to parse {len(to_parse)} transcripts.')
            for obj in to_parse:
                res = parse_and_create(obj)
                if res:
                    print(f'succes for {obj.pk}')
                else:
                    print(f'failure for {obj.pk}')
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response('Something went wrong!', status=status.HTTP_400_BAD_REQUEST)
