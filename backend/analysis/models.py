import os
import uuid

from django.db import models


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
        return os.path.join('files', f'{self.corpus.uuid}', 'transcripts', filename)

    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    corpus = models.ForeignKey(
        Corpus, related_name='transcripts', on_delete=models.PROTECT)
    content = models.FileField(upload_to=upload_path, blank=True, null=True)

    def __str__(self):
        return self.name


class Utterance(models.Model):
    def upload_path(self, filename):
        transcript_dir, _ = os.path.splitext(self.transcript.content.name)
        return os.path.join(transcript_dir, filename)

    text = models.CharField(max_length=50)
    speaker = models.CharField(max_length=50)
    utt_id = models.IntegerField(blank=True, null=True)
    transcript = models.ForeignKey(
        Transcript, related_name='utterances', on_delete=models.CASCADE)
    content = models.FileField(upload_to=upload_path)

    def __str__(self):
        return self.text


class UploadFile(models.Model):
    def upload_path(self, filename):
        return os.path.join('files', f'{self.corpus.uuid}', 'uploads', filename)

    name = models.CharField(max_length=255)
    content = models.FileField(upload_to=upload_path)
    corpus = models.ForeignKey(
        Corpus, related_name='files', on_delete=models.PROTECT, null=True, blank=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.name
