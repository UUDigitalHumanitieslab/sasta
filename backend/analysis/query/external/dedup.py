# TODO:
# - prefixes
# sort tests

from optparse import OptionParser
import os
from lxml import etree

from . import compounds
from .exampletrees import stree
from .lexicon import informlexicon
from .sastatok import tokenize
from .sastatoken import stringlist2tokenlist, tokenlist2stringlist
from .stringfunctions import deduplicate
from .treebankfunctions import getattval, getnodeyield, lastmainclauseof

# testfilename = 'testfile.txt'
# testfile = open(testfilename, 'w', encoding='utf8')

incomplete_zijn = '''
// node[node[ @rel = "hd" and @lemma="zijn"] and
        not (node[ @rel="predc" or @rel="vc" or @rel="ld" or ( @rel="mod" and @lemma="er") or
             node[ @rel = "mod" and node[ @rel = "hd" and (@lemma="voor")]]
           ])
         and count(. // node[ @ pt]) < 6
       ]
'''

incomplete_hebben = '''
//node[node[@rel="hd" and @lemma="hebben"] and 
       (not(node[@rel="obj1" or @rel="vc" or @rel="svp"]) )
        
       and count(.//node[@pt]) < 6
      ]
'''

incomplete_eentw = '''
//node[node[(@rel!="det" and @rel!="hd" and @rel!="mwp" and @rel!="--") and @lemma="één"] and not(node[@lemma="er"])]
'''

incompletexpaths = [incomplete_hebben, incomplete_zijn, incomplete_eentw]

space = ' '

janeenouset = set()
janeenouset = {'ja', 'nee', 'nou'}


def onvolledig(stree):
    results = []
    if incomplete(stree):
        results += [stree]
    return results


def incomplete(stree):
    result = False
    for query in incompletexpaths:
        if result:
            break
        else:
            allmatches = stree.xpath(query)
            matches = [m for m in allmatches if m == lastmainclauseof(stree)]
            result = matches != []
    return result


def incompletetreeleaves(stree):
    results = []
    for query in incompletexpaths:
        allmatches = stree.xpath("." + query)
        matches = [m for m in allmatches if m != lastmainclauseof(stree)]
        for m in matches:
            results += getnodeyield(m)
    return results


def findcorrections(nodelist):
    wordlist = [getattval(n, 'word') for n in nodelist]
    resultlist = []
    lnodelist = len(nodelist)
    for i in range(lnodelist-1):
        n1 = nodelist[i]
        n2 = nodelist[i+1]
        if getattval(n1, 'pt') == getattval(n2, 'pt'):
            resultlist.append((n1, n2))
    return resultlist


def isxxx(node):
    theword = getattval(node, 'word')
    result = theword.lower() == 'xxx'
    return result


def isfilledpausenode(n):
    theword = getattval(n, 'word')
    result = isfilledpause(theword)
    return result


def getfilledpausenodes(nodelist):
    resultlist = [n for n in nodelist if isfilledpausenode(n)]
    return resultlist


def infilledpauses(word):
    return (word in filledpauseslexicon)


def isfilledpause(word):
    lcword = word.lower()
    if infilledpauses(lcword):
        result = True
    else:
        swords = deduplicate(lcword, infilledpauses)
        if (swords != []):
            result = True
        else:
            result = False
    return result


def getfilledpausesposlist(tokenlist):
    results = []
    for token in tokenlist:
        if isfilledpause(token.word):
            results.append(token.pos)
    return results


def remove_duplicates(wl):
    stop = False
    result = wl
    lwl = len(wl)
    ml = lwl // 2
    tobedeleted = []
    for curlen in range(ml, 0, -1):
        for startpos in range(0, lwl-2*curlen+1, 1):
            if isduplicate(wl[startpos:startpos+curlen], wl[startpos+curlen:startpos + 2 * curlen]):
                newwl = wl[:startpos] + wl[startpos+curlen:]
                result = remove_duplicates(newwl)
                stop = True
                break
        if stop:
            break
    return result


def find_duplicates(wl):  # applies to a token list
    stop = False
    result = wl
    lwl = len(wl)
    ml = lwl // 2
    result = []
    for curlen in range(ml, 0, -1):
        for startpos in range(0, lwl-2*curlen+1, 1):
            if istokenduplicate(wl[startpos:startpos+curlen], wl[startpos+curlen:startpos + 2 * curlen]):
                result = [wl[p].pos for p in range(startpos, startpos+curlen)]
                newwl = wl[:startpos] + wl[startpos+curlen:]
                result += find_duplicates(newwl)
                stop = True
                break
        if stop:
            break
    return result


def find_duplicatenodes(wl):  # applies to a sequence of Lassy word nodes
    stop = False
    result = wl
    lwl = len(wl)
    ml = lwl // 2
    result = []
    for curlen in range(ml, 0, -1):
        for startpos in range(0, lwl-2*curlen+1, 1):
            if istokennodeduplicate(wl[startpos:startpos+curlen], wl[startpos+curlen:startpos + 2 * curlen]):
                result = [wl[p] for p in range(startpos, startpos+curlen)]
                newwl = wl[:startpos] + wl[startpos+curlen:]
                result += find_duplicatenodes(newwl)
                stop = True
                break
        if stop:
            break
    return result


def find_janeenouduplicatenodes(wl):
    resultlist = []
    lwl = len(wl)
    for i in range(lwl-1):
        wliw = getattval(wl[i], 'word')
        wli1w = getattval(wl[i+1], 'word')
        lcwliw = wliw.lower()
        lcwli1w = wli1w.lower()
        if lcwliw in janeenouset and lcwliw == lcwli1w:
            resultlist.append(wl[i])
    return resultlist


def istokennodeduplicate(tlist1, tlist2):
    result = True
    ltlist1 = len(tlist1)
    ltlist2 = len(tlist2)
    result = ltlist1 == ltlist2
    if result:
        for i in range(ltlist1):
            lcword1 = getattval(tlist1[i], 'word').lower()
            lcword2 = getattval(tlist2[i], 'word').lower()
            result = result and (lcword1 == lcword2)
    return result


def istokenduplicate(tlist1, tlist2):
    result = True
    ltlist1 = len(tlist1)
    ltlist2 = len(tlist2)
    result = ltlist1 == ltlist2
    if result:
        for i in range(ltlist1):
            result = result and (tlist1[i].word == tlist2[i].word)
    return result


def findjaneenou(tokennodelist):
    resultlist = []
    for node in tokennodelist:
        theword = getattval(node, 'word')
        lctheword = theword.lower()
        if lctheword in janeenouset:
            resultlist.append(node)
    return resultlist


def isduplicate(wlist1, wlist2):
    result = wlist1 == wlist2
    return result


def cleantokenlist(tokenlist, tobedeleted):
    cleanlist = [t for t in tokenlist if t.pos not in tobedeleted]
    cleanstrlist = [t.word for t in cleanlist]
    cleanstr = space.join(cleanstrlist)
    return cleanstr


def correct(stree):
    correct1xpath = './/node[@cat="top" and node[(@cat="smain" or @cat="sv1" or @cat="whq" or @cat="whsub")] and  count(node[@cat])=1]'
    correct2xpath = './/node[@cat="top" and node[@cat="du" and node[@rel="dlink" or @rel="tag"] and node[(@cat="smain" or @cat="sv1" or @cat="whq" or @cat="whsub") and @rel="nucl"] ]]'
    correct3xpath = './/node[@cat="top" and node[@cat="du" and node[@cat="conj" and count(node[(@cat="smain" or @cat="sv1" or @cat="whq"  or @cat="whsub")])>1] ]]'
    correct4xpath = './/node[@cat="top" and  node[@cat="conj" and count(node[(@cat="smain" or @cat="sv1" or @cat="whq"  or @cat="whsub")])>1] ]'
    correct5xpath = './/node[@cat="top" and  node[@cat="du" and count(node)=2 and node[@rel="dp" or @rel="tag" and @end<../node[@rel="nucl"]/@end] and node[(@cat="smain" or @cat="sv1" or @cat="whq")]] ]'
    matches1 = stree.xpath(correct1xpath)
    matches2 = stree.xpath(correct2xpath)
    matches3 = stree.xpath(correct3xpath)
    matches4 = stree.xpath(correct4xpath)
    matches5 = stree.xpath(correct5xpath)
    matches = matches1 + matches2 + matches3 + matches4 + matches5
    results = []
    for m in matches:
        if not incomplete(m):
            results.append(m)
    return results


def mlux(stree):
    resultnodelist = []
    tokennodelist = getnodeyield(stree)
    excludednodes = samplesize(stree)
    cleantokennodelist = [n for n in tokennodelist if n not in excludednodes]

    # remove all if xxx occurs
    xxxfound = any([isxxx(n) for n in cleantokennodelist])
    if xxxfound:
        resultnodelist = cleantokennodelist
    else:
        resultnodelist += find_duplicatenodes(cleantokennodelist)
        # STAP sec 6.3 p. 11
        # remove ja nee nou
        cleantokennodelist = [
            n for n in cleantokennodelist if n not in resultnodelist]
        janeenoulist = findjaneenou(cleantokennodelist)
        resultnodelist += janeenoulist
        cleantokennodelist = [
            n for n in cleantokennodelist if n not in janeenoulist]
        # remove false starts maybe word + nee / of nee / eh word; of w of pos1 w of pos1
        # remove of nee

        # remove tsw incl goh och hé oke
        tswnodes = [
            n for n in cleantokennodelist if getattval(n, 'pt') == 'tsw']
        resultnodelist += tswnodes
        cleantokennodelist = [
            n for n in cleantokennodelist if n not in tswnodes]

        #corrections = findcorrections(cleantokennodelist)
        # if corrections != []:
        #    cleanwordlist = [getattval(n, 'word') for n in cleantokennodelist]
        #    print(space.join(cleanwordlist), file=testfile)
        # for (w, corr) in corrections:
        #    print('--', getattval(w, 'word'), getattval(corr, 'word'), file=testfile)

        # remove dus als stopwoordje

        # remove words in incomplete sentences
        isws = incompletetreeleaves(stree)
        pureisws = [n for n in isws if n in cleantokennodelist]
        resultnodelist += pureisws
        cleantokenlist = [n for n in cleantokennodelist if n not in pureisws]
    return resultnodelist


def cleanwordof(node):
    word = getattval(node, 'word')
    lcword = word.lower()
    return lcword


def isprefixof(node1, node2):
    cw1 = cleanwordof(node1)
    cw2 = cleanwordof(node2)
    result = cw1 != cw2 and cw2.startswith(cw1)
    return result


def markprefixwords(wlist, cond):
    resultlist = []
    lwlist = len(wlist) - 1
    tokenctr = lwlist
    while tokenctr > 0:
        repctr = tokenctr - 1
        while repctr >= 0 and isprefixof(wlist[repctr], wlist[tokenctr]):
            if cond(wlist[repctr], wlist[tokenctr]):
                resultlist.append(wlist[repctr])
            repctr -= 1
        tokenctr = repctr
    return resultlist


def isnamenode(node):
    theword = getattval(node, 'word')
    result = theword[0].lower() != theword[0]
    return result


compoundxpath = './/node[@his="compound"]'
wordxpath = './/node[@pt and @pt!="let"]'


def neologisme(stree):
    results = []
    thecompounds = stree.xpath(compoundxpath)
    unknowncompounds = [c for c in thecompounds if getattval(
        c, 'word') not in compounds.compounds]

    results += unknowncompounds

    # exclude filledpauses, exclude names, misspellings, deviant pronunciations, ......
    allwordnodes = stree.xpath(wordxpath)
    wordnodes = [wn for wn in allwordnodes if len(
        getattval(wn, 'word')) > 5 and (not isnamenode(wn))]
    unknownwordnodes = [wn for wn in wordnodes if not informlexicon(
        getattval(wn, 'word').lower())]

    results += unknownwordnodes

    return results


def samplesize(stree):
    ''''
    yields the tokens to be excluded from the samplesize
    based on ASTA4 eVersie sec 3, p. 7-8
    '''

    resultlist = []
    # get the token nodes in sequence
    tokennodelist = getnodeyield(stree)
    # hitprint(tokennodelist)

    # find filledpauses and interjections
    filledpausenodes = getfilledpausenodes(tokennodelist)
    resultlist += filledpausenodes
    tokennodelist = [n for n in tokennodelist if n not in filledpausenodes]

    # find duplicatenode repetitions of ja, nee, nou
    janeenouduplicatenodes = find_janeenouduplicatenodes(tokennodelist)
    resultlist += janeenouduplicatenodes
    tokennodelist = [
        n for n in tokennodelist if n not in janeenouduplicatenodes]

    # find prefix herhalingen < 50%
    def cond(x, y): return len(cleanwordof(x)) / len(cleanwordof(y)) < .5
    prefixnodes = markprefixwords(tokennodelist, cond)
    resultlist += prefixnodes
    tokennodelist = [n for n in tokennodelist if n not in prefixnodes]

    return resultlist


# initialize filledpauseslexicon
filledpauseslexicon = set()
programfolder = os.path.dirname(os.path.abspath(__file__))
filledpausesfilename = os.path.join(
    programfolder, r'filledpauseslexicon/filledpauseslexicon.txt')
filledpausesfile = open(filledpausesfilename, 'r', encoding='utf8')
for word in filledpausesfile:
    cleanword = word.strip()
    filledpauseslexicon.add(cleanword)
