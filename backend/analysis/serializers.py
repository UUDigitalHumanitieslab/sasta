from rest_framework import serializers

from .models import Corpus, Transcript, UploadFile


class UploadFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadFile
        fields = '__all__'


class TranscriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transcript
        fields = '__all__'


class CorpusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Corpus
        fields = '__all__'
