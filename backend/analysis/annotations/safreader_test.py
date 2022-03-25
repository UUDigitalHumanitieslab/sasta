from operator import itemgetter
from pandas import DataFrame, Series
import pytest
import os.path as op

from analysis.query.run import query_transcript
from analysis.annotations.safreader import SAFReader
from analysis.annotations.safreader import get_word_levels


@pytest.mark.django_db
def test_read_saf(tarsp_method, tarsp_transcript, cha_testfiles_dir):
    true_results, _ = query_transcript(tarsp_transcript, tarsp_method, annotate=True, zc_embed=tarsp_method.category.zc_embeddings)
    reader = SAFReader(op.join(cha_testfiles_dir, 'sample_1_SAF.xlsx'), tarsp_method)

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


def test_wordlevels():
    data = {'level': map(str.lower, ['Utt', 'QA', 'SZ', 'Grammaticale Fout', 'Commentaar']),
            'word1': [1, None, 'X', 'V, BvBB', 'Hier staat wat commentaar']}
    df_in = DataFrame.from_dict(data)

    word_levels = get_word_levels(df_in)
    assert word_levels == ['qa', 'sz', 'grammaticale fout']


@pytest.mark.django_db
def test_read_saf_comments(tarsp_method, cha_testfiles_dir):
    reader = SAFReader(op.join(cha_testfiles_dir, 'sample_1_SAF_with_comments.xlsx'), tarsp_method)
    sent = reader.document.utterances[0]
    assert sent.words[0].comment == 'Ik vind hier iets van.'
    assert sent.words[1].comment == '1'
    assert sent.words[2].comment == 'En hier misschien ook wel iets van'
