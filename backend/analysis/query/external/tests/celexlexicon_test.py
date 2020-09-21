from ..celexlexicon import getwordinfo

testwords = ['liepen', 'gevalt', 'gevallen', 'mouwen', 'stukjes',
             'vaak', 'mooi', 'gouden', 'mooie', 'mooiere', 'pop', 'popje']
expected = [
    [('V', 'n/a', 'vm', 'lopen')],
    [('None', 'n/a', 'te2', 'gevallen'), ('None', 'n/a', 'te3', 'gevallen')],
    [('None', '2', 'm', 'geval'), ('None', 'n/a', 'i', 'gevallen'), ('None', 'n/a', 'pv', 'gevallen'),
     ('None', 'n/a', 'tm', 'gevallen'), ('None', 'n/a', 'P', 'gevallen'), ('V', 'n/a', 'pv', 'vallen')],
    [('N', '1', 'm', 'mouw')],
    [('None', '2', 'dm', 'stukje')],
    [('N', '1', 'e', 'vaak'), ('A', 'n/a', 'P', 'vaak')],
    [('A', 'n/a', 'P', 'mooi')],
    [('A', 'n/a', 'P', 'gouden')],
    [('A', 'n/a', 'PE', 'mooi')],
    [('A', 'n/a', 'CE', 'mooi')],
    [('V', 'n/a', 'te2I', 'poppen'), ('N', '1', 'e', 'pop'),
     ('N', '1', 'e', 'pop'), ('V', 'n/a', 'te1', 'poppen')],
    [('N', '1', 'de', 'pop')],
]


def test():
    for i, w in enumerate(testwords):
        # poslist = getposlist(w)
        # lemmas = getlemmas(w)
        # infls = getinfls(w)
        # print(w, lemmas,  poslist, infls)
        graminfos = getwordinfo(w)
        assert graminfos == expected[i]
        for (pos, dehet, infl, lemma) in graminfos:
            print(w, lemma, pos, dehet, infl)
