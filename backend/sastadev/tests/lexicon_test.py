from sastadev.lexicon import informlexicon


def test_lexicon():
    testwords = ['stukkies', 'jochie', 'gevalt', 'stukjes', 'gevallen', 'mouwe', 'mouwen', 'gaatie', 'gaat', 'ie']
    for w in testwords:
        print(w, informlexicon(w))
