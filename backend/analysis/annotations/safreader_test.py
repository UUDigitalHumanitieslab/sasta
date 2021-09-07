import pytest
import os.path as op

from analysis.query.run import query_transcript
from analysis.annotations.safreader import SAFReader


@pytest.mark.django_db
def test_read_saf(tarsp_method, tarsp_transcript, cha_testfiles_dir):
    true_results, _ = query_transcript(tarsp_transcript, tarsp_method, annotate=True, only_inform=False, zc_embed=tarsp_method.category.zc_embeddings)
    reader = SAFReader(op.join(cha_testfiles_dir, 'sample_1_SAF.xlsx'), tarsp_method)

    read_results = reader.document.to_allresults()

    assert sorted(read_results.coreresults.keys()) == sorted(true_results.coreresults.keys())
    for q, hits in read_results.coreresults.items():
        true_hits = true_results.coreresults[q]
        assert hits == true_hits
