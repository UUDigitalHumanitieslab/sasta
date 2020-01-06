import os
import uuid

from django.contrib.auth.models import User
from django.core.files.base import File
from django.db import models
from docx import Document


class Corpus(models.Model):
    # TODO: users
    # user = models.ForeignKey(User, related_name='corpora', on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    uuid = models.UUIDField(default=uuid.uuid4)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'corpora'


class Transcript(models.Model):
    def upload_path(self, filename):
        if str(self.corpus.uuid) in filename:
            return filename.replace('extracted', 'transcripts')
        return os.path.join('files', f'{self.corpus.uuid}', 'transcripts', filename)

    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    corpus = models.ForeignKey(
        Corpus, related_name='transcripts', on_delete=models.PROTECT)
    content = models.FileField(upload_to=upload_path, blank=True, null=True)

    def __str__(self):
        return self.name


class UploadFile(models.Model):
    # base upload location on corpus uuid
    def upload_path(self, filename):
        return os.path.join('files', f'{self.corpus.uuid}', 'uploads', filename)

    name = models.CharField(max_length=255)
    content = models.FileField(upload_to=upload_path)
    corpus = models.ForeignKey(
        Corpus, related_name='files', on_delete=models.PROTECT, null=True, blank=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.name
