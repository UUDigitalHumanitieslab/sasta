import pytest
import os
from .safreader import SAFReader
from ..models import AssessmentMethod

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


@pytest.mark.django_db
def test_reader():
    method = AssessmentMethod.objects.first()
    print(method)
    filep = os.path.join(BASE_DIR, 'test_sample.xlsx')
    reader = SAFReader(filep, method)
    assert len(reader.data) == 160
