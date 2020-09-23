from rest_framework import serializers

from .models import (AssessmentMethod, AssessmentQuery, Corpus, MethodCategory,
                     Transcript, UploadFile)


class UploadFileSerializer(serializers.ModelSerializer):
    corpus = serializers.CharField(source='corpus.name', required=False)
    corpus_id = serializers.CharField(source='corpus.id', required=False)

    class Meta:
        model = UploadFile
        corpus = serializers.SerializerMethodField()
        fields = ['name', 'content', 'status', 'corpus', 'corpus_id']

    # work around circular dependency
    def get_corpus(self, obj):
        return CorpusSerializer(obj.corpus).data

    def create(self, validated_data):
        user = self.context['request'].user
        corpus_data = validated_data.pop('corpus')
        corpus_instance, _created = Corpus.objects.get_or_create(
            name=corpus_data['name'],
            user=user,
            defaults={'status': 'created'})
        return UploadFile.objects.create(**validated_data,
                                         corpus=corpus_instance)


class TranscriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transcript
        fields = ('id', 'name', 'content',
                  'parsed_content', 'status', 'corpus', 'utterances')


class CorpusSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    files = UploadFileSerializer(read_only=True, many=True)
    transcripts = TranscriptSerializer(read_only=True, many=True)

    class Meta:
        model = Corpus
        fields = ('id', 'name', 'status', 'files', 'transcripts')


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
