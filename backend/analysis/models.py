import os
import uuid

from django.contrib.auth.models import User
from django.db import models


def get_file_path(_instance, filename):
    return os.path.join('files', 'uploads', f'{uuid.uuid4()}', filename)


class Corpus(models.Model):
    # TODO: users
    # user = models.ForeignKey(User, related_name='corpora', on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'corpora'


class Transcript(models.Model):
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    corpus = models.ForeignKey(
        Corpus, related_name='transcripts', on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class UploadFile(models.Model):
    # name of the uploaded file
    name = models.CharField(max_length=255)
    content = models.FileField(upload_to=get_file_path)
    corpus = models.ForeignKey(
        Corpus, related_name='files', on_delete=models.PROTECT, null=True, blank=True)
    # current processing status
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.name
