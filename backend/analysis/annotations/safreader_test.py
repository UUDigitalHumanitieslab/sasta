import os.path as op
from operator import itemgetter

import pytest
from analysis.annotations.safreader import SAFReader, get_word_levels
from analysis.query.run import query_transcript
from pandas import DataFrame
from pytest_lazyfixture import lazy_fixture


@pytest.mark.parametrize("method, transcript, filedir, samplenum", [
    (lazy_fixture("tarsp_method"), lazy_fixture("tarsp_transcript"), lazy_fixture("cha_testfiles_dir"), 5),
    (lazy_fixture("asta_method"), lazy_fixture("asta_transcript"), lazy_fixture("cha_testfiles_dir"), 16)
]
)
def test_read_saf(method, transcript, filedir, samplenum):
    true_results, _ = query_transcript(transcript, method, annotate=True, zc_embed=method.category.zc_embeddings)
    assert not true_results.annotationinput

    reader = SAFReader(op.join(filedir, f'sample_{samplenum}_SAF.xlsx'), method, transcript)
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
        for word in annos:
            true_word = next((w for w in true_annos if w.index == word.index), None)
            hits = sorted(word.hits, key=itemgetter('level', 'item'))
            if true_word:
                true_hits = sorted(true_word.hits, key=itemgetter('level', 'item'))
                assert hits == true_hits
            else:
                # if the true_word is not found (unaligned empty), make sure it didnt miss anything
                assert hits == []

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


def test_wordlevels():
    data = {'level': map(str.lower, ['Utt', 'QA', 'SZ', 'Grammaticale Fout', 'Commentaar']),
            'word1': [1, None, 'X', 'V, BvBB', 'Hier staat wat commentaar']}
    df_in = DataFrame.from_dict(data)

    word_levels = get_word_levels(df_in)
    assert word_levels == ['qa', 'sz', 'grammaticale fout']


def test_read_saf_comments(tarsp_method, tarsp_transcript, cha_testfiles_dir):
    reader = SAFReader(op.join(cha_testfiles_dir, 'sample_5_SAF_with_comments.xlsx'), tarsp_method, tarsp_transcript)
    sent = reader.document.utterances[3]
    assert sent.words[1].comment == 'Ik vind hier iets van.'
    assert sent.words[2].comment == '1'
    assert sent.words[3].comment == 'En hier misschien ook wel iets van'
