import os
from uuid import uuid4

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .utils import read_TAM


class Corpus(models.Model):
    # TODO: users
    # user = models.ForeignKey(User, related_name='corpora', on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    uuid = models.UUIDField(default=uuid4)

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


class AssessmentMethod(models.Model):
    def upload_path(self, filename):
        return os.path.join('files', 'TAMs', filename)

    name = models.CharField(max_length=50, unique=True)
    content = models.FileField(upload_to=upload_path, blank=True, null=True)

    def __str__(self):
        return self.name


@receiver(post_save, sender=AssessmentMethod)
def read_tam_file(sender, instance, created, **kwargs):
    if not created:
        # on update: delete all queries related to this method
        AssessmentQuery.objects.filter(method=instance).delete()

    try:
        read_TAM(instance)
    except Exception as error:
        #TODO: log
        print(error)


class AssessmentQuery(models.Model):
    method = models.ForeignKey(AssessmentMethod, related_name='queries',
                               on_delete=models.CASCADE)
    query_id = models.CharField(max_length=4)
    category = models.CharField(max_length=50, blank=True, null=True)
    subcat = models.CharField(max_length=50, blank=True, null=True)
    level = models.CharField(max_length=50, blank=True, null=True)
    item = models.CharField(max_length=50, blank=True, null=True)
    altitems = models.CharField(max_length=50, blank=True, null=True)
    implies = models.CharField(max_length=50, blank=True, null=True)
    original = models.BooleanField()
    pages = models.CharField(max_length=50, blank=True, null=True)
    phase = models.IntegerField(blank=True, null=True)
    query = models.CharField(max_length=500, blank=True, null=True)
    screening = models.BooleanField()
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.query_id

    class Meta:
        unique_together = ('method', 'query_id')
