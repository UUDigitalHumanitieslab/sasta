import itertools

from sastadev.celexlexicon import getinflforms, getwordinfo

def celex_test():
    testwords = ['liepen', 'gevalt', 'gevallen', 'mouwen', 'stukjes', 'vaak', 'mooi', 'gouden', 'mooie', 'mooiere', 'pop', 'popje']
    for w in testwords:
        # poslist = getposlist(w)
        # lemmas = getlemmas(w)
        # infls = getinfls(w)
        # print(w, lemmas,  poslist, infls)
        graminfos = getwordinfo(w)
        for (pos, dehet, infl, lemma) in graminfos:
            print(w, lemma, pos, dehet, infl)


def celex_test2():
    testlemmas = ['aaien', 'groeien', 'hebben', 'zijn']
    testinfls = ['te1', 'te2', 'te2I', 'te3', 'tm', 've', 'vm']
    for (lemma, infl) in itertools.product(testlemmas, testinfls):
        words = getinflforms(lemma, '4', infl)
        print(lemma, infl)
        for word in words:
            print('--', word)
