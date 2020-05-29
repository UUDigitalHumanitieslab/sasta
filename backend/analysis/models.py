import csv
import logging
import os
import shutil
from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.conf import settings

from .permissions import IsOwner, IsOwnerOrAdmin
from .utils import read_TAM, extract, get_items_list

logger = logging.getLogger('sasta')


class Compound(models.Model):
    HeadDiaNew = models.CharField(max_length=100)
    FlatClass = models.CharField(max_length=100)
    Class = models.CharField(max_length=100)

    def __str__(self):
        return self.HeadDiaNew


class CompoundFile(models.Model):
    content = models.FileField(
        upload_to=os.path.join('files', 'compoundfiles'))

    def __str__(self):
        return os.path.split(self.content.name)[1]


@receiver(post_save, sender=CompoundFile)
def save_compounds(sender, instance, **kwargs):
    Compound.objects.all().delete()
    with open(instance.content.path) as f:
        data = csv.reader(f, delimiter='\\')
        compounds = []
        for i, row in enumerate(data):
            compounds.append(
                Compound(HeadDiaNew=row[1], FlatClass=row[0], Class=row[2]))
        Compound.objects.bulk_create(compounds)


class Corpus(models.Model):
    user = models.ForeignKey(
        User, related_name='corpora', on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    uuid = models.UUIDField(default=uuid4)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'corpora'


@receiver(post_delete, sender=Corpus)
def corpus_delete(sender, instance, **kwargs):
    corpus_dir = os.path.join(settings.MEDIA_ROOT, 'files', str(instance.uuid))
    shutil.rmtree(corpus_dir, ignore_errors=True)


class Transcript(models.Model):
    def upload_path(self, filename):
        return os.path.join('files', f'{self.corpus.uuid}', 'transcripts', filename)

    def upload_path_parsed(self, filename):
        return os.path.join('files', f'{self.corpus.uuid}', 'parsed', filename)

    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    corpus = models.ForeignKey(
        Corpus, related_name='transcripts', on_delete=models.CASCADE)
    content = models.FileField(upload_to=upload_path, blank=True, null=True)
    parsed_content = models.FileField(
        upload_to=upload_path_parsed, blank=True, null=True)
    extracted_filename = models.CharField(
        max_length=500, blank=True, null=True)

    def __str__(self):
        return self.name


@receiver(post_delete, sender=Transcript)
def transcript_delete(sender, instance, **kwargs):
    instance.content.delete(False)
    instance.parsed_content.delete(False)
    if instance.extracted_filename:
        os.remove(instance.extracted_filename)


class Utterance(models.Model):
    # def upload_path(self, filename):
    #     transcript_dir, _ = os.path.splitext(self.transcript.content.name)
    #     return os.path.join(transcript_dir, filename)

    sentence = models.CharField(max_length=500)
    speaker = models.CharField(max_length=50)
    utt_id = models.IntegerField(blank=True, null=True)
    parse_tree = models.TextField(blank=True)
    transcript = models.ForeignKey(
        Transcript, related_name='utterances', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.utt_id}\t|\t{self.speaker}:\t{self.sentence}'


class UploadFile(models.Model):
    def upload_path(self, filename):
        return os.path.join('files', f'{self.corpus.uuid}', 'uploads', filename)

    name = models.CharField(max_length=255)
    content = models.FileField(upload_to=upload_path)
    corpus = models.ForeignKey(
        Corpus, related_name='files', on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.name


@receiver(post_save, sender=UploadFile)
def extract_upload_file(sender, instance, created, **kwargs):
    if created:
        try:
            extract(instance)
        except Exception as error:
            logger.exception(error)


class AssessmentMethod(models.Model):
    def upload_path(self, filename):
        return os.path.join('files', 'TAMs', filename)

    name = models.CharField(max_length=50, unique=True)
    date_added = models.DateField(auto_now_add=True)
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
        logger.error(error)
        print(f'error in read_tam_file:\t{error}')


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
    fase = models.IntegerField(blank=True, null=True)
    inform = models.BooleanField()
    query = models.CharField(max_length=5000, blank=True, null=True)
    screening = models.BooleanField()
    process = models.IntegerField()
    special1 = models.CharField(max_length=50, blank=True, null=True)
    special2 = models.CharField(max_length=50, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.query_id

    def altitems_list(self, sep):
        if not self.altitems:
            return []
        return get_items_list(self.altitems, sep)

    def implies_list(self, sep):
        if not self.implies:
            return []
        return get_items_list(self.implies, sep)

    class Meta:
        unique_together = ('method', 'query_id')


@receiver(post_delete, sender=UploadFile)
@receiver(post_delete, sender=AssessmentMethod)
@receiver(post_delete, sender=CompoundFile)
def file_delete(sender, instance, **kwargs):
    instance.content.delete(False)
