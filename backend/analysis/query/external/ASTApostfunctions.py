from collections import Counter

from .treebankfunctions import getattval

lpad = 3
zero = '0'
astamaxwordcount = 300


def sumctr(ctr):
    result = sum(ctr.values())
    return result


def wordcountperutt(allresults, _):
    if 'A046' in allresults.coreresults and 'A045' in allresults.coreresults:
        wordcounts = allresults.coreresults['A046']
        ignorewordcounts = allresults.coreresults['A045']
        result = wordcounts - ignorewordcounts
    else:
        result = Counter()
    return result


def finietheidsindex(allresults, _):
    okpvs = allresults.coreresults['A024'] if 'A024' in allresults.coreresults else Counter()
    subpvs = allresults.coreresults['A032'] if 'A032' in allresults.coreresults else Counter()
    delpvs = allresults.coreresults['A033'] if 'A033' in allresults.coreresults else Counter()
    tijdfoutpvs = allresults.coreresults['A041'] if 'A041' in allresults.coreresults else Counter()
    foutepvs = subpvs + delpvs + tijdfoutpvs
    okpvcount = sumctr(okpvs)
    foutepvcount = sumctr(foutepvs)
    if okpvcount + foutepvcount == 0:
        result = 0
    else:
        result = okpvcount / (okpvcount + foutepvcount)
    return result


def countwordsandcutoff(allresults, _):
    result = (None, 0)
    if 'A047' in allresults.postresults:
        paddedlist = []
        for key, val in allresults.postresults['A047'].items():
            paddedkey = key.rjust(lpad, zero)
            paddedlist.append((paddedkey, val))
        sortedlist = sorted(paddedlist)
        wc = 0
        for key, val in sortedlist:
            if wc + val > astamaxwordcount:
                result = (key, wc)
                break
            else:
                wc += val
                result = (None, wc)
    return result


def KMcount(allresults, _):
    Kcount = sumctr(allresults.coreresults['A013']) if 'A013' in allresults.coreresults else 0
    Mcount = sumctr(allresults.coreresults['A020']) if 'A020' in allresults.coreresults else 0
    result = Kcount + Mcount
    return result


def getlemmas(allresults, _):
    allmatches = allresults.allmatches
    allresults.postresults['A046'] = Counter()
    for el in allmatches:
        (qid, uttid) = el
        if qid in ['A021', 'A018']:
            for amatch in allmatches[el]:
                # theword = normalizedword(amatch[0])
                theword = getattval(amatch[0], 'lemma')
                allresults.postresults['A046'].update([(theword, uttid)])
    return allresults
