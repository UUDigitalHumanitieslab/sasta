import os
from copy import deepcopy

from lxml import etree
from sastadev import SD_DIR, SDLOGGER, compounds
from sastadev.lexicon import informlexicon
from sastadev.sastatoken import Token
from sastadev.stringfunctions import deduplicate
from sastadev.treebankfunctions import (all_lower_consonantsnode,
                                        asta_recognised_wordnode, getattval,
                                        getnodeyield, lastmainclauseof)

nodetype = etree._Element

positionatt = 'end'


class DupInfo:
    def __init__(self, longdups=dict(), shortdups=dict(), icsws=[]):
        self.longdups = longdups
        self.shortdups = shortdups
        self.icsws = icsws  # nodes for words in incomplete sentences

    def __str__(self):
        result = str(self.longdups) + ';' + str(self.shortdups) + str(self.icsws)
        return result

    def merge(self, dupinfo):
        newdupinfo = deepcopy(self)
        newdupinfo.longdups = dictmerge(self.longdups, dupinfo.longdups)
        newdupinfo.shortdups = dictmerge(self.shortdups, dupinfo.shortdups)
        newdupinfo.icsws = self.icsws + dupinfo.icsws
        return newdupinfo

    def get_chaintail(self, i):
        if i in self.shortdups:
            result = self.get_chaintail(self.shortdups[i])
        elif i in self.longdups:
            result = self.get_chaintail(self.longdups[i])
        else:
            result = i
        return result


def dictmerge(dict1, dict2):
    newdict = deepcopy(dict1)
    for el in dict2:
        if el in newdict:
            if newdict[el] != dict2[el]:
                SDLOGGER.error('Conflicting values for {}: {}: {} not included'.format(el, newdict[el], dict2[el]))
            else:
                SDLOGGER.warning('Duplicate values for {}: {} = {}'.format(el, newdict[el], dict2[el]))
        else:
            newdict[el] = dict2[el]
    return newdict


normalisedict = {'c': 'k'}

unwantedtokenlist = ['-', '--', '#', '–']

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


def getposition(nort):
    if nort is None:
        result = None
    elif isinstance(nort, Token):
        result = nort.pos
    elif isinstance(nort, nodetype):
        result = getattval(nort, positionatt)
    else:
        result = ('??')
    return result


def getword(nort):
    if nort is None:
        result = ''
    elif isinstance(nort, Token):
        result = nort.word
    elif isinstance(nort, nodetype):
        result = getattval(nort, 'word')
    else:
        result = '**'
    return result


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
    for i in range(lnodelist - 1):
        n1 = nodelist[i]
        n2 = nodelist[i + 1]
        if getattval(n1, 'pt') == getattval(n2, 'pt'):
            resultlist.append((n1, n2))
    return resultlist


def isxxx(node):
    theword = getword(node)
    result = theword.lower() == 'xxx'
    return result


def isfilledpausenort(nort):
    theword = getword(nort)
    result = isfilledpause(theword)
    return result


def getfilledpauses(nortlist):
    resultlist = [tok for tok in nortlist if isfilledpausenort(tok)]
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


def getfilledpausesposlist(nortlist):
    results = []
    for token in nortlist:
        theword = getword(token)
        if isfilledpause(theword):
            thepos = getposition(token)
            results.append(thepos)
    return results


def remove_duplicates(wl):
    stop = False
    result = wl
    lwl = len(wl)
    ml = lwl // 2
    tobedeleted = []
    for curlen in range(ml, 0, -1):
        for startpos in range(0, lwl - 2 * curlen + 1, 1):
            if isduplicate(wl[startpos:startpos + curlen], wl[startpos + curlen:startpos + 2 * curlen]):
                newwl = wl[:startpos] + wl[startpos + curlen:]
                result = remove_duplicates(newwl)
                stop = True
                break
        if stop:
            break
    return result


def isnortsubstring(n1, n2):
    w1 = getword(n1)
    w2 = getword(n2)
    lcw1 = w1.lower()
    lcw2 = w2.lower()
    result = lcw1 in lcw2 and len(w1) / len(w2) > 0.5
    return result


def find_substringduplicates2(wl):
    dupmapping = dict()
    result = []
    lwl = len(wl)
    for i in range(lwl - 1):
        curtoken = wl[i]
        nexttoken = wl[i + 1]
        curlcword = getword(curtoken).lower()
        if isnortsubstring(curtoken, nexttoken) and not (informlexicon(curlcword)):
            duppos = getposition(curtoken)
            origpos = getposition(nexttoken)
            dupmapping[duppos] = origpos
            result.append(curtoken)
    alldupinfo = DupInfo(dupmapping, dict())
    return result, alldupinfo


def find_simpleduplicates2(wl):
    dupmapping = dict()
    result = []
    lwl = len(wl)
    for i in range(lwl - 1):
        if isnortduplicate([wl[i]], [wl[i + 1]]):
            duppos = getposition(wl[i])
            origpos = getposition(wl[i + 1])
            dupmapping[duppos] = origpos
            result.append(wl[i])
    alldupinfo = DupInfo(dupmapping, dict())
    return result, alldupinfo


def find_duplicates(wl):
    result, _ = find_duplicates2(wl)
    return result


def find_duplicates2(wl):  # applies to a sequence of Lassy word nodes or token nodes
    dupmapping = dict()
    alldupinfo = DupInfo()
    stop = False
    result = wl
    lwl = len(wl)
    ml = lwl // 2
    result = []
    for curlen in range(ml, 0, -1):
        for startpos in range(0, lwl - 2 * curlen + 1, 1):
            if isnortduplicate(wl[startpos:startpos + curlen], wl[startpos + curlen:startpos + 2 * curlen]):
                result = [wl[p] for p in range(startpos, startpos + curlen)]
                for p in range(startpos, startpos + curlen):
                    duppos = getposition(wl[p])
                    origpos = getposition(wl[p + curlen])
                    dupmapping[duppos] = origpos
                    alldupinfo = DupInfo(dupmapping, dict())
                newwl = wl[:startpos] + wl[startpos + curlen:]
                restresult, restdupinfo = find_duplicates2(newwl)
                result += restresult
                alldupinfo = alldupinfo.merge(restdupinfo)

                stop = True
                break
        if stop:
            break
    return result, alldupinfo


def find_janeenouduplicates(wl):
    result, _ = find_janeenouduplicates2(wl)
    return result


def find_janeenouduplicates2(wl):
    resultlist = []
    dupmapping = dict()
    lwl = len(wl)
    for i in range(lwl - 1):
        wlip = getposition(wl[i])
        wli1p = getposition(wl[i + 1])
        wliw = getword(wl[i])
        wli1w = getword(wl[i + 1])
        lcwliw = wliw.lower()
        lcwli1w = wli1w.lower()
        if lcwliw in janeenouset and lcwliw == lcwli1w:
            resultlist.append(wl[i])
            dupmapping[wlip] = wli1p
    dupinfo = DupInfo(longdups=dupmapping, shortdups=dict())
    return resultlist, dupinfo


def normalisestring(str1):
    result = ''
    for ch in str1:
        if ch in normalisedict:
            repl = normalisedict[ch]
            result += repl
        else:
            result += ch
    return result


def isnortduplicate(tlist1, tlist2):
    result = True
    ltlist1 = len(tlist1)
    ltlist2 = len(tlist2)
    result = ltlist1 == ltlist2
    if result:
        for i in range(ltlist1):
            lcword1 = getword(tlist1[i]).lower()
            lcword2 = getword(tlist2[i]).lower()
            nlcword1 = normalisestring(lcword1)
            nlcword2 = normalisestring(lcword2)
            result = result and ((nlcword1 == nlcword2) or nlcword2.startswith(nlcword1))
    return result


def findjaneenou(nortlist):
    resultlist = []
    for node in nortlist:
        theword = getword(node)
        lctheword = theword.lower()
        if lctheword in janeenouset:
            resultlist.append(node)
    return resultlist


def isduplicate(wlist1, wlist2):
    result = wlist1 == wlist2
    return result


def cleantokenlist(tokenlist, tobedeleted):
    cleanlist = [t for t in tokenlist if getposition(t) not in tobedeleted]
    cleanstrlist = [getword(t) for t in cleanlist]
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
    result, _ = mlux2(stree)
    return result


def mlux2(stree):
    resultnodelist = []
    alldupinfo = DupInfo()
    tokennodelist = getnodeyield(stree)
    excludednodes, dupinfo = samplesize2(stree)
    cleantokennodelist = [n for n in tokennodelist if n not in excludednodes]
    alldupinfo = alldupinfo.merge(dupinfo)

    # remove all if xxx occurs No this should not be done here
    # xxxfound = any([isxxx(n) for n in cleantokennodelist])
    # if xxxfound:
    #    resultnodelist = cleantokennodelist
    # else:
    if True:

        # remove unknown words
        unknown_words = [n for n in cleantokennodelist if not(asta_recognised_wordnode(n))]
        resultnodelist += unknown_words
        cleantokennodelist = [n for n in cleantokennodelist if n not in unknown_words]

        # ASTA sec 6.3 p. 11
        # remove ja nee nou
        janeenoulist = findjaneenou(cleantokennodelist)
        resultnodelist += janeenoulist
        cleantokennodelist = [n for n in cleantokennodelist if n not in janeenoulist]
        # remove false starts maybe word + nee / of nee / eh word; of w of pos1 w of pos1
        # remove of nee

        # remove tsw incl goh och hé oke
        tswnodes = [n for n in cleantokennodelist if getattval(n, 'pt') == 'tsw']
        resultnodelist += tswnodes
        cleantokennodelist = [n for n in cleantokennodelist if n not in tswnodes]

        # simple duplicates
        dupnodelist, dupinfo = find_simpleduplicates2(cleantokennodelist)
        resultnodelist += dupnodelist
        alldupinfo = alldupinfo.merge(dupinfo)
        cleantokennodelist = [n for n in cleantokennodelist if n not in dupnodelist]

        # for debugging
        # print(showtns(cleantokennodelist))
        dupnodelist, dupinfo = find_duplicates2(cleantokennodelist)
        resultnodelist += dupnodelist
        alldupinfo = alldupinfo.merge(dupinfo)
        cleantokennodelist = [n for n in cleantokennodelist if n not in dupnodelist]

        # find prefix herhalingen >= 50%
        def cond(x, y):
            return len(cleanwordofnort(x)) / len(cleanwordofnort(y)) > 0.5
        prefixnodes, dupinfo = getprefixwords2(cleantokennodelist, cond)
        resultnodelist += prefixnodes
        alldupinfo = alldupinfo.merge(dupinfo)
        cleantokennodelist = [n for n in cleantokennodelist if n not in prefixnodes]

        # find unknown words that are a substring of their successor
        substringnodes, dupinfo = find_substringduplicates2(cleantokennodelist)
        alldupinfo = alldupinfo.merge(dupinfo)
        cleantokennodelist = [n for n in cleantokennodelist if n not in prefixnodes]

        # corrections = findcorrections(cleantokennodelist)
        # if corrections != []:
        #    cleanwordlist = [getattval(n, 'word') for n in cleantokennodelist]
        #    print(space.join(cleanwordlist), file=testfile)
        # for (w, corr) in corrections:
        #    print('--', getattval(w, 'word'), getattval(corr, 'word'), file=testfile)

        # remove dus als stopwoordje

        # remove words that consist of consonants only
        resultnodelist = [n for n in resultnodelist if not(all_lower_consonantsnode(n))]

        # remove words in incomplete sentences
        isws = incompletetreeleaves(stree)
        pureisws = [n for n in isws if n in cleantokennodelist]
        resultnodelist += pureisws
        alldupinfo.icsws = pureisws
        cleantokenlist = [n for n in cleantokennodelist if n not in pureisws]
    return resultnodelist, alldupinfo


def getrepeatedtokens(tokenlist, repeatingtokens):
    '''

    :param tokenlist:
    :param repeatingtokens: list of tokens that are repeating a token in tokenlist
    :return: dictionary of repeatingtoken: repeatedtoken pair
    '''
    repeatedtokens = {}
    ltokenlist = len(tokenlist)
    for i in range(ltokenlist):
        if tokenlist[i] in repeatingtokens:
            repeatedtokens[tokenlist[i]] = tokenlist[i + 1]
    return repeatedtokens


def cleanwordofnort(token):
    word = getword(token)
    result = cleanwordof(word)
    return result


def cleanwordof(word):
    lcword = word.lower()
    return lcword


def isnortprefixof(node1, node2):
    w1 = getword(node1)
    cw1 = cleanwordof(w1)
    w2 = getword(node2)
    cw2 = cleanwordof(w2)
    result = isprefixof(cw1, cw2)
    return result


def isprefixof(cw1, cw2):
    ncw1 = normalisestring(cw1)
    ncw2 = normalisestring(cw2)
    result = ncw1 != ncw2 and ncw2.startswith(ncw1)
    return result


def getprefixwords(wlist, cond):
    result, _ = getprefixwords2(wlist, cond)
    return result


def getprefixwords2(wlist, cond):
    resultlist = []
    dupmapping = dict()
    lwlist = len(wlist) - 1
    tokenctr = lwlist
    while tokenctr > 0:
        repctr = tokenctr - 1
        while repctr >= 0 and isnortprefixof(wlist[repctr], wlist[tokenctr]):
            if cond(wlist[repctr], wlist[tokenctr]):
                resultlist.append(wlist[repctr])
                reppos = getposition(wlist[repctr])
                tokenpos = getposition(wlist[tokenctr])
                dupmapping[reppos] = tokenpos
            repctr -= 1
        tokenctr = repctr
    dupinfo = DupInfo(dict(), dupmapping)
    return resultlist, dupinfo


def isnamenort(node):
    theword = getword(node)
    result = theword[0].lower() != theword[0]
    return result


compoundxpath = './/node[@his="compound"]'
wordxpath = './/node[@pt and @pt!="let"]'


def neologisme(stree):
    results = []
    thecompounds = stree.xpath(compoundxpath)
    unknowncompounds = [c for c in thecompounds if getattval(c, 'word') not in compounds.compounds]

    results += unknowncompounds

    # exclude filledpauses, exclude names, misspellings, deviant pronunciations, ......
    allwordnodes = stree.xpath(wordxpath)
    wordnodes = [wn for wn in allwordnodes if len(getattval(wn, 'word')) > 5 and (not isnamenort(wn))]
    unknownwordnodes = [wn for wn in wordnodes if not informlexicon(getattval(wn, 'word').lower())]

    results += unknownwordnodes

    return results


def getunwantedtokens(nortlist):
    results = []
    for nort in nortlist:
        nortword = getword(nort)
        if nortword in unwantedtokenlist:
            results.append(nort)
    return results


def samplesize(stree):
    result, _ = samplesize2(stree)
    return result


def samplesize2(stree):
    ''''
    yields the tokens to be excluded from the samplesize
    based on ASTA4 eVersie sec 3, p. 7-8
    plus a dupinfo containing a duplicate mapping word in pos x is a repeat of the word in position y
    '''

    resultlist = []
    alldupinfo = DupInfo()
    # get the token nodes in sequence
    tokennodelist = getnodeyield(stree)
    # hitprint(tokennodelist)

    # throw out unwanted symbols - -- # etc
    unwantedtokens = getunwantedtokens(tokennodelist)
    resultlist += unwantedtokens
    tokennodelist = [n for n in tokennodelist if n not in unwantedtokens]

    # find filledpauses and interjections
    filledpausenodes = getfilledpauses(tokennodelist)
    resultlist += filledpausenodes
    tokennodelist = [n for n in tokennodelist if n not in filledpausenodes]

    # find duplicatenode repetitions of ja, nee, nou
    janeenouduplicatenodes, dupinfo = find_janeenouduplicates2(tokennodelist)
    resultlist += janeenouduplicatenodes
    tokennodelist = [n for n in tokennodelist if n not in janeenouduplicatenodes]
    alldupinfo = alldupinfo.merge(dupinfo)

    # temporarily remove ja nee nou to get the write short repetitions
    janeenoutokens = findjaneenou(tokennodelist)
    temptokennodelist = [n for n in tokennodelist if n not in janeenoutokens]

    # find prefix herhalingen < 50%
    def cond(x, y):
        return len(cleanwordofnort(x)) / len(cleanwordofnort(y)) <= 0.5
    prefixnodes, dupinfo = getprefixwords2(temptokennodelist, cond)
    resultlist += prefixnodes
    tokennodelist = [n for n in tokennodelist if n not in prefixnodes]
    alldupinfo = alldupinfo.merge(dupinfo)

    return resultlist, alldupinfo


# initialize filledpauseslexicon
filledpauseslexicon = set()
filledpausesfilename = os.path.join(SD_DIR, 'filledpauseslexicon', 'filledpauseslexicon.txt')
filledpausesfile = open(filledpausesfilename, 'r', encoding='utf8')
for word in filledpausesfile:
    cleanword = word.strip()
    filledpauseslexicon.add(cleanword)
