import pytest
from analysis.models import AssessmentMethod, Transcript


@pytest.mark.django_db
def test_embed_annotate(admin_client):
    # Todo: proper test
    method = AssessmentMethod.objects.first()
    transcript = Transcript.objects.get(id=826)

    response = admin_client.post('/api/transcripts/826/annotate/',
                                 {'method': method.name})
    assert 1 == 0
