import csv
import logging
import os
import shutil

from django.conf import settings
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from .models import (AssessmentMethod, AssessmentQuery, Compound, CompoundFile,
                     Corpus, Transcript, UploadFile)
from .utils import extract, read_TAM

logger = logging.getLogger('sasta')


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


@receiver(post_delete, sender=Corpus)
def corpus_delete(sender, instance, **kwargs):
    corpus_dir = os.path.join(settings.MEDIA_ROOT, 'files', str(instance.uuid))
    shutil.rmtree(corpus_dir, ignore_errors=True)


@receiver(post_delete, sender=Transcript)
def transcript_delete(sender, instance, **kwargs):
    instance.content.delete(False)
    instance.parsed_content.delete(False)
    if instance.extracted_filename:
        try:
            os.remove(instance.extracted_filename)
        except FileNotFoundError:
            pass


@receiver(post_save, sender=UploadFile)
def extract_upload_file(sender, instance, created, **kwargs):
    if created:
        try:
            extract(instance)
        except Exception as error:
            logger.exception(error)


@receiver(post_delete, sender=UploadFile)
@receiver(post_delete, sender=AssessmentMethod)
@receiver(post_delete, sender=CompoundFile)
def file_delete(sender, instance, **kwargs):
    try:
        instance.content.delete(False)
    except FileNotFoundError:
        pass


@receiver(post_save, sender=AssessmentMethod)
def read_tam_file(sender, instance, created, **kwargs):
    if not created:
        # on update: delete all queries related to this method
        AssessmentQuery.objects.filter(method=instance).delete()
    try:
        read_TAM(instance)
    except Exception as error:
        logger.exception(error)


@receiver(post_save, sender=Corpus)
def initial_default_method(sender, instance, created, **kwargs):
    if created:
        try:
            instance.default_method = instance.method_category.definitions.latest()
            instance.save()
        except Exception as error:
            logger.exception(error)






