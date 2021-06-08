import logging
import os
import zipfile
from io import BytesIO
from itertools import chain
from uuid import uuid4

from sastadev.external_functions import form_map
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from lxml import etree as ET

from .utils import get_items_list

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


class MethodCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    zc_embeddings = models.BooleanField()
    levels = ArrayField(base_field=models.CharField(max_length=20, blank=True))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'method categories'

    def get_form_function(self):
        try:
            return form_map.get(self.name)
        except KeyError:
            return None

    def has_form(self):
        return True if self.get_form_function() else False


class AssessmentMethod(models.Model):
    def upload_path(self, filename):
        return os.path.join('files', 'TAMs', filename)

    name = models.CharField(max_length=50)
    date_added = models.DateField(auto_now_add=True)
    content = models.FileField(upload_to=upload_path, blank=True, null=True)
    category = models.ForeignKey(
        MethodCategory, related_name='definitions', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (('category', 'name'))

    def get_item_mapping(self, sep):
        queries = self.queries.all()
        mapping = {}
        for q in queries:
            mapping.update(q.get_item_mapping(sep))
        return mapping


class Corpus(models.Model):
    user = models.ForeignKey(
        User, related_name='corpora', on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    uuid = models.UUIDField(default=uuid4)
    date_added = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
    default_method = models.ForeignKey(AssessmentMethod,
                                       on_delete=models.SET_NULL, related_name='corpora', blank=True, null=True)

    def __str__(self):
        return self.name

    def download_as_zip(self):
        stream = BytesIO()
        transcripts = self.transcripts.all()
        files = [(t.content.path, t.parsed_content.path) for t in transcripts]
        files = list(chain.from_iterable(files))
        zipf = zipfile.ZipFile(stream, "w")
        for f in files:
            arcname = os.path.split(f)[1]
            zipf.write(f, arcname)
        zipf.close()
        return stream

    class Meta:
        verbose_name_plural = 'corpora'


class Transcript(models.Model):
    UNKNOWN = 0
    CREATED = 1
    CONVERTING, CONVERTED, CONVERSION_FAILED = 2, 3, 4
    PARSING, PARSED, PARSING_FAILED = 5, 6, 7

    STATUS_CHOICES = (
        (UNKNOWN, 'unknown'),
        (CREATED, 'created'),
        (CONVERTING, 'converting'),
        (CONVERTED, 'converted'),
        (CONVERSION_FAILED, 'conversion-failed'),
        (PARSING, 'parsing'),
        (PARSED, 'parsed'),
        (PARSING_FAILED, 'parsing-failed'),
    )

    def upload_path(self, filename):
        return os.path.join('files', f'{self.corpus.uuid}',
                            'transcripts', filename)

    def upload_path_parsed(self, filename):
        return os.path.join('files', f'{self.corpus.uuid}',
                            'parsed', filename)

    name = models.CharField(max_length=255)
    status = models.PositiveIntegerField(
        choices=STATUS_CHOICES, default=UNKNOWN)
    # status = models.CharField(max_length=50)
    corpus = models.ForeignKey(
        Corpus, related_name='transcripts', on_delete=models.CASCADE)
    content = models.FileField(upload_to=upload_path, blank=True, null=True)
    parsed_content = models.FileField(
        upload_to=upload_path_parsed, blank=True, null=True)
    extracted_filename = models.CharField(
        max_length=500, blank=True, null=True)
    date_added = models.DateField(auto_now_add=True)

    # objects = TranscriptManager()
    target_speakers = models.CharField(max_length=500, blank=True)
    target_ids = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def target_speakers_list(self):
        return self.target_speakers.split(',')


class Utterance(models.Model):
    sentence = models.CharField(max_length=500)
    speaker = models.CharField(max_length=50)
    utt_id = models.IntegerField(blank=True, null=True)
    xsid = models.IntegerField(blank=True, null=True)
    parse_tree = models.TextField(blank=True)
    transcript = models.ForeignKey(
        Transcript, related_name='utterances', on_delete=models.CASCADE)

    @property
    def syntree(self):
        if self.parse_tree:
            return ET.fromstring(self.parse_tree)
        return None

    @property
    def for_analysis(self):
        """ Utterance should be analysed if:
        - Speaker is in target list
            - If target xsids, utt should also have xsid
        OR
        - Utterance has xsid
        """
        if self.speaker in self.transcript.target_speakers_list:
            if self.transcript.target_ids:
                return self.xsid is not None
            return True
        return self.xsid is not None

    def __str__(self):
        return f'{self.utt_id}\t|\t{self.speaker}:\t{self.sentence}'


class UploadFile(models.Model):
    def upload_path(self, filename):
        return os.path.join('files', f'{self.corpus.uuid}',
                            'uploads', filename)

    name = models.CharField(max_length=255)
    content = models.FileField(upload_to=upload_path)
    corpus = models.ForeignKey(
        Corpus, related_name='files', on_delete=models.CASCADE,
        null=True, blank=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.name


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
    screening = models.BooleanField(blank=True, null=True)
    process = models.IntegerField()
    special1 = models.CharField(max_length=50, blank=True, null=True)
    special2 = models.CharField(max_length=50, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.query_id

    def get_altitems_list(self, sep):
        if not self.altitems:
            return []
        return get_items_list(self.altitems, sep)

    def get_implies_list(self, sep):
        if not self.implies:
            return []
        return get_items_list(self.implies, sep)

    def get_item_mapping(self, sep):
        ''' mapping of all possible items (including altitems) to this query'''
        if (not self.item) or (not self.level):
            return {}
        result = {(self.item.lower(), self.level.lower()):
                  (self.query_id, self.fase)}
        alt_items = self.get_altitems_list(sep)
        if alt_items:
            for item in alt_items:
                if (item, self.level.lower()) not in result:
                    result[(item, self.level.lower())] = (
                        self.query_id, self.fase)
        return result

    class Meta:
        unique_together = ('method', 'query_id')
