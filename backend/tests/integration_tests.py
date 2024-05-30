from analysis.query.query_transcript import run_sastacore


def test_analysis(db, all_transcripts):
    '''Make sure all of the test files can be analysed'''

    for t in all_transcripts:
        results = run_sastacore(t, t.corpus.default_method)
        assert results
