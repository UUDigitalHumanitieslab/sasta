import os

from sastadev import SD_DIR
from sastadev.deregularise import (correctionfilename, getcorrections,
                                   makeparadigm, tab)


def test_deregularise():
    # read the irregular verbs

    irregverbfilename = 'DutchIrregularVerbs.tsv'
    irregverbfile = open(irregverbfilename, 'r', encoding='utf8')

    forms = {}
    for line in irregverbfile:
        if line[-1] == '\n':
            line = line[:-1]
        row = line.split(tab)
        forms[row[0]] = row

    irregverbfile.close()

    correction = {}
    # initialisatie
    for el in forms:
        triples = makeparadigm(el, forms)
        # (regularpastsg, regularpastpl, pastparticiple, pastpartwithe, wrongpastpart, wrongpastpart2, wrongpastpart2a, wrongenpastpart) = regular
        # (goodpastsg, goodpastpl, goodpastpart, goodpastpartwithe, goodpastpart, goodpastpart, goodpastpart, goodpastpart) = goodforms

        # print(el, stem, stemFS, takesge, regularpastsg, regularpastpl, pastparticiple, pastpartwithe, wrongpastpart)

        # fill the lookup table

        for wrong, meta, good in triples:
            if good != wrong:
                correction[wrong] = good, meta

        # if goodpastsg != regularpastsg:
        #     correction[regularpastsg] = goodpastsg
        # if goodpastpl != regularpastpl:
        #     correction[regularpastpl] = goodpastpl
        # if goodpastpart != pastparticiple:
        #     correction[pastparticiple] = goodpastpart
        # if goodpastpartwithe != pastpartwithe:
        #     correction[pastpartwithe] = goodpastpartwithe
        # if goodpastpart != wrongpastpart:
        #     correction[wrongpastpart] = goodpastpart
        # if goodpastpart != wrongpastpart2:
        #     correction[wrongpastpart2] = goodpastpart
        # if goodpastpart != wrongpastpart2a:
        #     correction[wrongpastpart2a] = goodpastpart
        # if goodpastpart != wrongenpastpart:
        #     correction[wrongenpastpart] = goodpastpart

        # test
        uniquewords = {w for (w, _, _) in triples}
        for w in uniquewords:
            for corrected, meta in getcorrections(w, correction):
                print(w, corrected, meta)

    for wrong, good in [('daan', 'gedaan'), ('vervald', 'vervallen'), ('opgevald', 'opgevallen'),
                        ('overvald', 'overvallen'), ('oververvald', 'oververvallen'), ('gevalt', 'gevallen')]:
        cands = getcorrections(wrong, correction)
        if cands == []:
            print('WRONG', wrong, '', good)
        for cand, m in cands:
            if cand == good:
                print('OK', wrong, cand, good, m)
            else:
                print('WRONG', wrong, cand, good, m)

    testlist = ['kijken', 'gaan', 'eten']
    for el in testlist:
        triples = makeparadigm(el, forms)
        # (regularpastsg, regularpastpl, pastparticiple, pastpartwithe, wrongpastpart, wrongpastpart2, wrongpastpart2a, wrongenpastpart) = regular
        # (goodpastsg, goodpastpl, goodpastpart, goodpastpartwithe, goodpastpart, goodpastpart1, goodpastpart2, goodpastpart3) = goodforms
        uniquewords = {w for (w, _, _) in triples}
        for (w, _, _) in triples:
            for corrected, m in getcorrections(w, correction):
                print(w, corrected, m)
    for w in ['aaneengeloopt', 'gekijken', 'gekeekt', 'uitgekijken', 'uitgekeekt']:
        for corrected, m in getcorrections(w, correction):
            print(w, corrected, m)

    correctionfile = open(os.path.join(SD_DIR, correctionfilename), 'w', encoding='utf8')
    for w in correction:
        print(w, correction[w][0], correction[w][1], sep=tab, file=correctionfile)
