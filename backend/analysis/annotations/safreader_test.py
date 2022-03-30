from operator import itemgetter
import pytest
import os.path as op

from analysis.query.run import query_transcript
from analysis.annotations.safreader import SAFReader


def test_read_saf(tarsp_method, tarsp_transcript, cha_testfiles_dir):
    true_results, _ = query_transcript(tarsp_transcript, tarsp_method, annotate=True, zc_embed=tarsp_method.category.zc_embeddings)
    assert not true_results.annotationinput

    reader = SAFReader(op.join(cha_testfiles_dir, 'sample_5_SAF.xlsx'), tarsp_method, tarsp_transcript)
    read_results = reader.document.to_allresults()

    # are the coreresults the same?
    assert sorted(read_results.coreresults.keys()) == sorted(true_results.coreresults.keys())
    for q, hits in read_results.coreresults.items():
        true_hits = true_results.coreresults[q]
        assert hits == true_hits

    # are all the annotations the same?
    assert true_results.annotations.keys() == reader.document.reformatted_annotations.keys()
    for q, annos in true_results.annotations.items():
        true_annos = reader.document.reformatted_annotations[q]
        for word, true_word in zip(annos, true_annos):
            hits = sorted(word.hits, key=itemgetter('level', 'item'))
            true_hits = sorted(true_word.hits, key=itemgetter('level', 'item'))
            assert hits == true_hits

    # are the exactresults the same?
    true_exact = {k: sorted(v) for (k, v) in true_results.exactresults.items() if v != []}
    read_exact = {k: sorted(v) for (k, v) in read_results.exactresults.items() if v != []}
    assert true_exact == read_exact

    # are the allutts the same?
    assert true_results.allutts == read_results.allutts



def test_astalex(asta_method, asta_transcript, asta_transcript_corrections, cha_testfiles_dir):
    true_results, _ = query_transcript(asta_transcript, asta_method, annotate=True, zc_embed=False)
    assert true_results.annotationinput

    assert true_results.annotations.get(3)[6].hits == [{'level': 'Taalmaat', 'item': 'N', 'fase': None}]

    assert True
