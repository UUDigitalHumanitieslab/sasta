from rest_framework import serializers

from .models import Corpus, Transcript, UploadFile


class UploadFileSerializer(serializers.ModelSerializer):
    corpus = serializers.CharField(source='corpus.name', required=False)

    class Meta:
        model = UploadFile
        corpus = serializers.SerializerMethodField()
        fields = ['name', 'content', 'status', 'corpus']

    # work around circular dependency
    def get_corpus(self, obj):
        return CorpusSerializer(obj.corpus).data

    def create(self, validated_data):
        if 'corpus' in validated_data:
            corpus_data = validated_data.pop('corpus')
            corpus_instance, _created = Corpus.objects.get_or_create(
                name=corpus_data['name'],
                defaults={'status': 'created'})
            return UploadFile.objects.create(**validated_data, corpus=corpus_instance)
        return UploadFile.objects.create(**validated_data)


class TranscriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transcript
        fields = '__all__'


class CorpusSerializer(serializers.ModelSerializer):
    files = UploadFileSerializer(read_only=True, many=True)
    transcripts = TranscriptSerializer(read_only=True, many=True)

    class Meta:
        model = Corpus
        fields = ('name', 'status', 'files', 'transcripts')
