from sastadev.readmethod import read_method
from analysis.models import AssessmentQuery


def test_sastadev_queries(asta_method):
    result = read_method(asta_method.category.name.lower(),
                         asta_method.content.path)

    for q in result.queries.values():
        model = AssessmentQuery.objects.get(query_id=q.id, method=asta_method)
        assert model

        sd_obj = model.to_sastadev()
        assert sd_obj

        # Assert that the queries remain untouched after
        # two-way conversion
        assert sd_obj.__dict__ == q.__dict__
