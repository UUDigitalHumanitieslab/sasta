import os.path as op

import pytest
from analysis.convert.convert import convert
from analysis.models import (AnalysisRun, Transcript)
from django.core.files import File
from parse.parse_utils import create_utterance_objects


@pytest.fixture
def tarsp_transcript(db, tarsp_corpus, cha_testfiles_dir):
    obj = Transcript.objects.create(
        name='tarsp_sample_5',
        status=Transcript.PARSED,
        corpus=tarsp_corpus
    )
    with open(op.join(cha_testfiles_dir, 'sample_5.cha'), 'rb') as f:
        obj.content.save('sample_5.cha', File(f))
    convert(obj)
    with open(op.join(cha_testfiles_dir, 'sample_5.xml'), 'rb') as f:
        obj.parsed_content.save('sample_5.xml', File(f))
    create_utterance_objects(obj)
    obj.save()
    yield obj
    obj.delete()


@pytest.fixture
def asta_transcript(db, asta_corpus, cha_testfiles_dir):
    obj = Transcript.objects.create(
        name='asta_sample_16',
        status=Transcript.PARSED,
        corpus=asta_corpus
    )
    with open(op.join(cha_testfiles_dir, 'sample_16.cha'), 'rb') as f:
        obj.content.save('sample_16.cha', File(f))
    convert(obj)
    with open(op.join(cha_testfiles_dir, 'sample_16.xml'), 'rb') as f:
        obj.parsed_content.save('sample_16.xml', File(f))
    create_utterance_objects(obj)
    obj.save()
    yield obj
    obj.delete()


@pytest.fixture
def asta_transcript_corrections(db, asta_transcript, asta_method, cha_testfiles_dir):
    obj = AnalysisRun(
        transcript=asta_transcript,
        method=asta_method,
        is_manual_correction=True
    )
    with open(op.join(cha_testfiles_dir, 'sample_16_SAF_corrected.xlsx'), 'rb') as f:
        obj.annotation_file.save('sample_16_SAF_corrected.xlsx', File(f))
    obj.save()
    yield obj
    obj.delete()
