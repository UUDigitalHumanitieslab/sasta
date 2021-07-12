from .Sziplus import getnodecount
from .treebankfunctions import getattval

noimplemmas = {'hoeven', 'moeten', 'mogen', 'kunnen', 'hebben', 'willen', 'hebben', 'zitten'}
noimpwords = {'ben', 'bent', 'is', 'zijn'}
impmodlemmas = {'eens', 'maar'}


impquery = '''
.//node[@cat="sv1" and
    not(node[@rel="su"]) and
    node[@rel="hd" and @pt="ww" and @pvtijd="tgw" and @pvagr="ev"
         and @wvorm="pv" and
         not(contains(@frame,"modal")) and
         (not(@lemma="zijn") or @word="wees" or @word="weest") and
         (not(contains(@lemma,"moeten") or contains(@lemma,"hoeven") or
              contains(@lemma,"zullen") or contains(@lemma,"kunnen") or
              contains(@lemma,"mogen") or @lemma="hebben" or contains(@lemma, "_hebben")
             )
         )
        ]
     ]
'''

# //node[@cat="sv1" and
#    count(node)<=2 and
#    (not(node[@rel="su"]) or (node[@rel="su" and @lemma="jij"])) and
#    node[@rel="hd" and @pt="ww" and @pvtijd="tgw" and @pvagr="ev"
#         and @wvorm="pv" and
#         not(contains(@frame,"modal")) and
#         @lemma!="hoeven" and @lemma!="moeten" and @lemma!="kunnen" and @lemma !="mogen" and @lemma!="hebben" and @lemma!="zitten" and @word!="ben" and
#         (@stype="imparative" or ../node[@rel="mod" and (@lemma="eens" or @lemma="maar")])  ] ]


ynquery = '''
.//node[@cat="sv1" and
    node[@rel="hd" and @pt="ww" and @pvtijd !="conj" and @stype="ynquestion" ] and
    node[@rel="su" ]
 ]
'''


'''
//node[@cat="sv1" and
    node[@rel="hd" and @pt="ww" and @pvtijd !="conj" and @stype="ynquestion" and number(@begin) < ../node[@rel="su" ]/number(@begin)] and
    node[@rel="su" and @lemma!="ik"]  and
    not(node[@rel="vc"]) and
    not(node[@rel="mod" and (@lemma="maar" or @lemma="eens")]) and
    count(node) <=3]
'''


def ynwi(syntree, ncf):
    results = []
    cands = syntree.xpath(ynquery)
    # print('#cands', len(cands))
    ok = True
    for cand in cands:
        hds = cand.xpath('node[@rel="hd"]')
        sus = cand.xpath('node[@rel="su"]')
        modlemmas = set(cand.xpath('node[@rel="mod"]/@lemma'))

        for hd in hds:
            for su in sus:
                suend = getattval(su, 'end')
                hdend = getattval(hd, 'end')
                hdpvtijd = getattval(hd, 'pvtijd')
                hdpvagr = getattval(hd, 'pvagr')
                hdlemma = getattval(hd, 'lemma')
                hdword = getattval(hd, 'words')
                hdpotimp = (hdpvtijd == 'tgw' and hdpvagr == 'ev' and (hdlemma != 'zijn' or hdword == 'wees'))
                ok = ok and (hdend < suend)
                # print('ok=', ok)
                # noimpmodlemmas = modlemmas.intersection(impmodlemmas)
                # print('noimpmodlemmas', noimpmodlemmas)
                # ok = ok and ((not hdpotimp) or noimpmodlemmas == {})
                # print ('hdpotimp',hdpotimp)
                # print('modlemmas', modlemmas)
                # print('ok=', ok)
                thenodecount = getnodecount(cand)
                # print('thenodecount', thenodecount)
                ok = ok and ncf(thenodecount)
                # print('ok=', ok)
                if ok:
                    results.append(cand)
    return results


def wondx(syntree):
    results = ynwi(syntree, lambda x: 2 <= x <= 3)
    return results


def wond4(syntree):
    results = ynwi(syntree, lambda x: x == 4)
    return results


def wond5plus(syntree):
    results = ynwi(syntree, lambda x: x >= 5)
    return results


def impwi(syntree, nodecounts):
    results = []
    cands = syntree.xpath(impquery)
    ok = True
    for cand in cands:
        hds = cand.xpath('node[@rel="hd"]')
        modlemmas = set(cand.xpath('node[@rel="mod"]/@lemma'))
        # print('modlemmas', modlemmas)

        for hd in hds:
            lemma = getattval(hd, 'lemma')
            ok = ok and (lemma not in noimplemmas)
            # print('ok=', ok)
            word = getattval(hd, 'word')
            ok = ok and (word not in noimpwords)
            # print('ok=', ok)
            stype = getattval(hd, 'stype')
            ok = ok and (stype == 'imparative' or (modlemmas.intersection(impmodlemmas) != {}))
            # print('ok=', ok)

        thenodecount = getnodecount(cand)
        ok = ok and thenodecount in nodecounts
        # print('ok=', ok)
        if ok:
            results.append(cand)
    return results


def wx(syntree):
    results = impwi(syntree, {1, 2})
    return results


def wxy(syntree):
    results = impwi(syntree, {3})
    return results


def wxyz(syntree):
    results = impwi(syntree, {4})
    return results


def wxyz5(syntree):
    results = impwi(syntree, {5})
    return results
