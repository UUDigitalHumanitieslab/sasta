from rest_framework import serializers

from .models import (AssessmentMethod, AssessmentQuery, Corpus, MethodCategory,
                     Transcript, UploadFile)


class UploadFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadFile
        fields = ['name', 'content', 'status', 'corpus']


class TranscriptSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=Transcript.STATUS_CHOICES)
    status_name = serializers.CharField(source='get_status_display')

    class Meta:
        model = Transcript
        fields = ('id', 'name', 'content',
                  'parsed_content', 'status', 'status_name', 'date_added', 'corpus', 'utterances')


class CorpusSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    files = UploadFileSerializer(read_only=True, many=True)
    transcripts = TranscriptSerializer(read_only=True, many=True)

    class Meta:
        model = Corpus
        fields = ('id', 'name', 'status', 'default_method', 'method_category', 'date_added', 'date_modified', 'files', 'transcripts')


class AssessmentQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentQuery
        fields = '__all__'


class MethodCategorySerializer(serializers.ModelSerializer):
    has_form = serializers.BooleanField()

    class Meta:
        model = MethodCategory
        fields = ('id', 'name', 'zc_embeddings', 'levels', 'has_form')


class AssessmentMethodSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    queries = AssessmentQuerySerializer(read_only=True, many=True)
    date_added = serializers.DateField(format='%d-%m-%Y', read_only=True)
    category = MethodCategorySerializer()

    class Meta:
        model = AssessmentMethod
        fields = ('id', 'name', 'category', 'content',
                  'date_added', 'queries', )
