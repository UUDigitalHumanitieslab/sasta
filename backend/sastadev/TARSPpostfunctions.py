'''
defines functions for the TARSP post part of the methods
'''
from collections import Counter

from sastadev.treebankfunctions import getmeta
from sastadev.query import core_process


OndVC = 'T071'
OndWVC = 'T076'
OndWBVC = 'T075'

vuqueryids = ['T094', 'T095', 'T096', 'T150']
tarsp_clausetypes = ['mededelende zin', 'vragen', 'gebiedende wijs']
excludedqids = ['T039', 'T048', 'T049', 'T052']   # TARSP p. 21: hè, Into, Inversie, Kop
gofase_minthreshold = 0.05  # 5% p21 Tarsp 2005


def getqueriesbystage(queries):
    results = {}
    for qid in queries:
        if queries[qid].subcat.lower() in tarsp_clausetypes and qid not in excludedqids:
            stage = queries[qid].fase
            if stage in results:
                results[stage].append(qid)
            else:
                results[stage] = [qid]
    return results


def vutotaal(allresults, _):
    scores = []
    for qid in vuqueryids:
        if qid in allresults.coreresults:
            scores.append(allresults.coreresults[qid])
        else:
            scores.append(Counter())
#    scores = [allresults.coreresults[qid] for qid in vuqueryids]
    counts = [len(s) for s in scores]
    result = sum(counts)
    return result


def gtotaal(allresults, _):
    Atotaal = 0
    vutotaal = allresults.postresults['T151']
    Gtotaal = allresults.uttcount - Atotaal - vutotaal
    return Gtotaal


def countutts(acounter):
    '''
    input parameter acounter: Counter()
    returns sum of the lengths of the values for each key in acounter
    '''
    result = 0
    for k in acounter:
        result += acounter[k]
    return result


def getuttcountsbystage(queriesbystage, allresults):
    uttcounts = {}
    for stage in queriesbystage:
        uttcounts[stage] = 0
        for qid in queriesbystage[stage]:
            if qid in allresults.coreresults:
                uttcounts[stage] += countutts(allresults.coreresults[qid])
    return uttcounts


def getstage(uttcounts, allresults):
    cands = []
    gtotaal = allresults.postresults['T152']
    for el in uttcounts:
        if uttcounts[el] / gtotaal >= gofase_minthreshold:
            cands.append(el)
    if cands == []:
        result = 1
    else:
        result = max(cands)
    return result


def gofase(allresults, thequeries):
    result = 0
    queriesbystage = getqueriesbystage(thequeries)
    uttcounts = getuttcountsbystage(queriesbystage, allresults)
    result = getstage(uttcounts, allresults)

    return result


def genpfi(stage, allresults, allqueries):
    theqids = [qid for qid in allqueries if allqueries[qid].fase == stage and allqueries[qid].process == core_process
               and allqueries[qid].special1 != 'star2']
    coreresults = allresults.coreresults
    scoredqids = [qid for qid in theqids if qid in coreresults and len(coreresults[qid]) > 0]
    # OndVC
    if OndWVC in theqids or OndWBVC in scoredqids:
        scoredqids.append(OndVC)
    # XNeg
    # OndB
    # VCW
    # BX
    result = len(scoredqids)
    return result


def pf2(allresults, allqueries):
    return genpfi(2, allresults, allqueries)


def pf3(allresults, allqueries):
    return genpfi(3, allresults, allqueries)


def pf4(allresults, allqueries):
    return genpfi(4, allresults, allqueries)


def pf5(allresults, allqueries):
    return genpfi(5, allresults, allqueries)


def pf6(allresults, allqueries):
    return genpfi(6, allresults, allqueries)


def pf7(allresults, allqueries):
    return genpfi(7, allresults, allqueries)


def pf(allresults, allqueries):
    postresults = allresults.postresults
    result = sum([postresults['T154'], postresults['T155'], postresults['T158'],
                  postresults['T159'], postresults['T160'], postresults['T161']])
    return result


def getname(allresults, allqueries):
    result = getmeta('name')
    return result


def getchildage(allresults, allqueries):
    result = ''
    return result
