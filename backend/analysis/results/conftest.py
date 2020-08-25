import pytest
from analysis.models import AssessmentQuery, AssessmentMethod


@pytest.fixture
def mock_method(db):
    method = AssessmentMethod.objects.create(name='mock_method')
    query = AssessmentQuery.objects.create(method=method,
                                           query_id='T003',
                                           category='Zinsconstructies',
                                           subcat='Mededelende Zin',
                                           level='Sz',
                                           item='6+',
                                           altitems='None',
                                           implies='None',
                                           original='True',
                                           pages='56',
                                           fase='6',
                                           query='sziplus6',
                                           inform='True',
                                           screening='True',
                                           process='0',
                                           special1='None',
                                           special2='None',
                                           comments='Some comments')
    return method
