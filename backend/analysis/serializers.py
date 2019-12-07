from rest_framework import serializers
from .models import UploadFile


class UploadFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadFile
        fields = '__all__'
