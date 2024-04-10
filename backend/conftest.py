import glob
from collections import Counter
from os import path as op

import pytest
from analysis.models import AssessmentMethod, MethodCategory
from django.conf import settings
from django.core.files import File
from sastadev.allresults import AllResults
from sastadev.conf import settings as sd_settings

from lxml import etree


@pytest.fixture
def cha_testfiles_dir():
    return op.join(settings.BASE_DIR, 'test_files')


@pytest.fixture
def tarsp_category(db):
    obj = MethodCategory.objects.create(
        name='TARSP', zc_embeddings=True,
        levels=['Sz', 'Zc', 'Wg', 'VVW'],
        marking_postcodes=['[+ G]'])
    yield obj
    obj.delete()


@pytest.fixture
def stap_category(db):
    obj = MethodCategory.objects.create(
        name='STAP', zc_embeddings=False,
        levels=['Complexiteit', 'Grammaticale fout'],
        marking_postcodes=['[+ G]', '[+ VU]'])
    yield obj
    obj.delete()


@pytest.fixture
def asta_category(db):
    obj = MethodCategory.objects.create(
        name='ASTA', zc_embeddings=False, levels=[
            "Samplegrootte",
            "MLU",
            "Taalmaat",
            "Foutenanalyse",
            "Lemma"
        ], marking_postcodes=["[+ G]"])
    yield obj
    obj.delete()


@pytest.fixture
def method_dir():
    return op.join(sd_settings.SD_DIR, 'data', 'methods')


@pytest.fixture
def tarsp_method(db, tarsp_category, method_dir):
    file = glob.glob(f'{method_dir}/TARSP Index Current.xlsx')[0]
    with open(file, 'rb') as f:
        wrapped_file = File(f)
        instance = AssessmentMethod(
            name='tarsp_test_method', category=tarsp_category)
        instance.content.save(op.basename(file), wrapped_file)
    yield instance
    instance.delete()


@pytest.fixture
def asta_method(db, asta_category, method_dir):
    file = glob.glob(f'{method_dir}/ASTA Index Current.xlsx')[0]
    with open(file, 'rb') as f:
        wrapped_file = File(f)
        instance = AssessmentMethod(
            name='asta_test_method', category=asta_category)
        instance.content.save(op.basename(file), wrapped_file)
    yield instance
    instance.delete()


@pytest.fixture
def single_utt_allresults(cha_testfiles_dir):
    parsed = etree.parse(
        op.join(cha_testfiles_dir, 'single_utt_corrected.xml'))
    utts = parsed.xpath('alpino_ds')

    return AllResults(
        uttcount=2,
        coreresults={('A029', 'A029'): Counter({'1': 1}), ('A045', 'A045'): Counter({'1': 1}),
                     ('A001', 'A001'): Counter({'1': 1}), ('A003', 'A003'): Counter({'1': 2}),
                     ('A013', 'A013'): Counter({'1': 1}), ('A018', 'A018'): Counter({'1': 2}),
                     ('A021', 'A021'): Counter({'1': 2}), ('A024', 'A024'): Counter({'1': 2}),
                     ('A051', 'beet'): Counter({'1': 1}), ('A051', 'vertellen'): Counter({'1': 1}),
                     ('A051', 'ongeluk'): Counter({'1': 1}), ('A051', 'hebben'): Counter({'1': 1})},

        exactresults={('A029', 'A029'): [('1', 1)], ('A045', 'A045'): [('1', 2)],
                      ('A001', 'A001'): [('1', 7)], ('A003', 'A003'): [('1', 8), ('1', 13)],
                      ('A013', 'A013'): [('1', 4)], ('A018', 'A018'): [('1', 12), ('1', 18)],
                      ('A021', 'A021'): [('1', 6), ('1', 17)], ('A024', 'A024'): [('1', 4), ('1', 15)],
                      ('A051', 'beet'): [('1', 6)], ('A051', 'vertellen'): [('1', 12)],
                      ('A051', 'ongeluk'): [('1', 17)], ('A051', 'hebben'): [('1', 18)],
                      },
        postresults={'A046': Counter({('beet', '1'): 1, ('ongeluk', '1'): 1}),
                     'A049': Counter({('vertellen', '1'): 1, ('hebben', '1'): 1})},
        allmatches=None,  # Not provided in this fixture
        filename='single_utt',
        analysedtrees=[(n + 1, tree) for n, tree in enumerate(utts)],
        annotationinput=True,
        allutts={1: ['ja', 'uh', 'ik', 'vind', 'het', 'beetje', 'moeilijk',
                     'om', 'het', 'goed', 'te', 'vertellen', 'want', 'ik',
                     'heb', 'een', 'ongeluk', 'gehad']}

    )
