from analysis.models import AssessmentQuery
from analysis.query.functions import Query
import pytest


@pytest.mark.django_db
def test_model_to_query(mock_method):
    model = AssessmentQuery.objects.filter(
        method=mock_method, query__isnull=False).first()
    obj = Query.from_model(model)

    assert obj.process == 0
    assert obj.id == 'T003'
