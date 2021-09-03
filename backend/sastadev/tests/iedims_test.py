import csv

from sastadev import lexicon
from sastadev.iedims import (bigfilesep, getbaseinlexicon, getjeformsnolex,
                             slash)

testset = [('cluppie', ['clubje', 'clupje']), ('bakkie', ['bakje']), ('dakkie', ['dakje']), ('darmpie', ['darmpje']),
           ('doppie', ['dopje']), ('rapie', ['raapje']), ('huisie', ['huisje']), ('kassie', ['kasje', 'kastje']),
           ('vrachie', ['vrachje', 'vrachtje']),
           ('dorpie', ['dorpje']), ('verfie', ['verfje']), ('fessie', ['fesje', 'fezje']), ('vessie', ['vestje']),
           ('feessie', ['feestje']), ('beessie', ['beestje']), ('meissie', ['meisje'])]

testlexicon = ['clubje', 'bakje', 'dakje', 'darmpje', 'dopje', 'raapje', 'huisje',
               'kasje', 'kastje', 'vrachtje', 'dorpje', 'verfje', 'fezje', 'vestje', 'feestje', 'beestje', 'meisje']


def localtest(theregex, replaces, testlist):
    for (w, g) in testlist:
        m = theregex.match(w)
        for repl in replaces:
            r = theregex.sub(repl, w)
            if r == g:
                print('OK: {}:{}'.format(w, r))
            else:
                print('NOT OK: {} yields {} but it should be {}'.format(w, r, g))


def readbigtestset(infilename):
    results = []
    with open(infilename, mode='r', encoding='utf8') as infile:
        myreader = csv.reader(infile, delimiter=bigfilesep)
        rowctr = 0
        for row in myreader:
            rowctr += 1
            if rowctr == 1:
                continue   # skip the header
            newpair = (row[0], [row[2]])
            results.append(newpair)
    return results


def report(results, ieform, jeforms, logfile):
    aresultinlexiconfound = False
    aresultOK = False
    if ieform in jeforms:
        print('OK: {}:{}'.format(ieform, ieform), file=logfile)
    else:
        for result in results:
            if result in jeforms:
                aresultOK = True
                if lexicon.informlexicon(result):
                    aresultinlexiconfound = True
                    print('OK: {}:{}'.format(ieform, result), file=logfile)
                elif ieform != result:
                    base = getbaseinlexicon(result)
                    if base is not None:
                        aresultinlexiconfound = True
                        print('OK: {}:{} ({} in lexicon)'.format(ieform, result, base), file=logfile)
                    else:
                        print('replacement for {} not in lexicon: {}'.format(ieform, result), file=logfile)
        if not aresultOK:
            print('NOT OK: {} : {}; should be: {}'.format(ieform, slash.join(results), slash.join(jeforms)), file=logfile)
        elif not aresultinlexiconfound:
            print('No replacements for: {} : {} found in the lexicon'.format(ieform, slash.join(results)), file=logfile)


def test_iedims():
    #    debugresults = getjeformsnolex('hachje')
    debugresults = getjeformsnolex('schoffie')
    testfilename = 'iediminutives/iedimsgold2.csv'
    bigtestset = readbigtestset(testfilename)
    testset = bigtestset
    logfilename = 'iediminutives/iedims.log'
    logfile = open(logfilename, 'w', encoding='utf8')
    for (ieform, jeforms) in testset:
        results = getjeformsnolex(ieform)
        report(results, ieform, jeforms, logfile)
