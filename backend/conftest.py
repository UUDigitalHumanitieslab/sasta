import pytest
from django.conf import settings
from analysis.models import MethodCategory, AssessmentMethod
from os import path as op
from sastadev.conf import settings as sd_settings
import glob
from django.core.files import File


@pytest.fixture
def cha_testfiles_dir():
    return op.join(settings.BASE_DIR, 'test_files')


@pytest.fixture
def tarsp_category(db):
    obj = MethodCategory.objects.create(
        name='TARSP', zc_embeddings=True, levels=[
            'Sz', 'Zc', 'Wg', 'VVW'], marking_postcodes=['[+ G]'])
    yield obj
    obj.delete()


@pytest.fixture
def stap_category(db):
    obj = MethodCategory.objects.create(
        name='STAP', zc_embeddings=False, levels=[
            'Complexiteit', 'Grammaticale fout'], marking_postcodes=['[+ G]', '[+ VU]'])
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
