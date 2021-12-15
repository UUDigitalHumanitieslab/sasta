import glob
import os.path as op

import pytest
from analysis.convert.convert import convert
from analysis.models import (AssessmentMethod, Corpus, MethodCategory,
                             Transcript)
from django.conf import settings
from django.core.files import File
from parse.parse_utils import parse_and_create


@pytest.fixture
def cha_testfiles_dir():
    return op.join(settings.BASE_DIR, 'analysis', 'annotations', 'test_files')


@pytest.mark.django_db
@pytest.fixture()
def tarsp_category():
    obj = MethodCategory.objects.create(name='TARSP', zc_embeddings=True, levels=['Sz', 'Zc', 'Wg', 'VVW'])
    yield obj
    obj.delete()


@pytest.mark.django_db
@pytest.fixture
def tarsp_method(tarsp_category):
    method_dir = op.join(settings.BASE_DIR, 'sastadev', 'methods')
    file = glob.glob(f'{method_dir}/TARSP Index Current.xlsx')[0]
    with open(file, 'rb') as f:
        wrapped_file = File(f)
        instance = AssessmentMethod(name='tarsp_test_method', category=tarsp_category)
        instance.content.save(op.basename(file), wrapped_file)
    yield instance
    instance.delete()


@pytest.mark.django_db
@pytest.fixture
def tarsp_corpus(admin_user, tarsp_method, tarsp_category):
    obj = Corpus.objects.create(
        user=admin_user,
        name='tarsp_test_corpus',
        status='created',
        default_method=tarsp_method,
        method_category=tarsp_category
    )
    yield obj
    obj.delete()


@pytest.mark.django_db
@pytest.fixture
def tarsp_transcript(tarsp_corpus, cha_testfiles_dir):
    obj = Transcript.objects.create(
        name='tarsp_sample_1',
        status=Transcript.PARSED,
        corpus=tarsp_corpus
    )
    with open(op.join(cha_testfiles_dir, 'sample_1.cha'), 'rb') as f:
        obj.content.save('sample_1.cha', File(f))

    # TODO: mock this, don't actually parse when testing
    convert(obj)
    parse_and_create(obj)
    yield obj
    obj.delete()
