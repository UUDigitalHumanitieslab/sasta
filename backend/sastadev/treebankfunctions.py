'''
various treebank functions
'''

import re
from copy import copy, deepcopy

from lxml import etree
from sastadev import SDLOGGER

from .lexicon import informlexicon, informlexiconpos, isa_namepart
from .namepartlexicon import isa_namepart_uc
from .stringfunctions import allconsonants


class Metadata:
    '''
    contains 3 elements, each a string: type, name, value
    '''

    def __init__(self, thetype, thename, thevalue):
        self.type = thetype
        self.name = thename
        self.value = thevalue

    def md2PEP(self):
        result = '##META {} {} = {}'.format(self.type, self.name, self.value)
        return result

    def md2XMLElement(self):
        result = etree.Element('meta', type=self.type, name=self.name, value=self.value)
        return result


min_sasta_length = 9
sasta_short_length = 4

space = ' '
vertbar = '|'
compoundsep = '_'


# next 3 derived from the alpino dtd
allrels = ['hdf', 'hd', 'cmp', 'sup', 'su', 'obj1', 'pobj1', 'obj2', 'se', 'pc', 'vc', 'svp', 'predc', 'ld', 'me',
           'predm', 'obcomp', 'mod', 'body', 'det', 'app', 'whd', 'rhd', 'cnj', 'crd', 'nucl', 'sat', 'tag', 'dp',
           'top', 'mwp', 'dlink', '--']

allcats = ['smain', 'np', 'ppart', 'ppres', 'pp', 'ssub', 'inf', 'cp', 'du', 'ap', 'advp', 'ti', 'rel', 'whrel',
           'whsub', 'conj', 'whq', 'oti', 'ahi', 'detp', 'sv1', 'svan', 'mwu', 'top', 'cat', 'part']

allpts = ['let', 'spec', 'bw', 'vg', 'lid', 'vnw', 'tw', 'ww', 'adj', 'n', 'tsw', 'vz']

clausecats = ['smain', 'ssub', 'inf', 'cp', 'ti', 'rel', 'whrel', 'whsub', 'whq', 'oti', 'ahi', 'sv1', 'svan']

trueclausecats = ['smain', 'cp', 'rel', 'whrel', 'whsub', 'whq', 'sv1', 'svan']

complrels = ['su', 'obj1', 'pobj1', 'obj2', 'se', 'pc', 'vc', 'svp', 'predc', 'ld']

mainclausecats = ['smain', 'whq', 'sv1']

pluralcrds = [('en',)]

hwws_tijd = ['hebben', 'zijn', 'zullen']
hwws_aspect = ['gaan', 'komen', 'zijn', 'blijven', 'zitten', 'liggen', 'lopen', 'staan']
hwws_voice = ['worden', 'zijn']
hwws_modal = ['kunnen', 'zullen', 'mogen', 'moeten', 'willen', 'hoeven', 'horen', 'behoren']
hwws_caus = ['doen', 'laten']
hwws_circum = ['doen']

tarsp_auxverbs = set(hwws_tijd + hwws_aspect + hwws_voice + hwws_modal + hwws_caus + hwws_circum)

# uttidquery = "//meta[@name='uttid']/@value"
sentidxpath = './/sentence/@sentid'

# altquery = "//meta[@name='alt']/@value"
metaquerytemplate = "//meta[@name='{}']/@value"
sentencexpathquery = "//sentence/text()"

uniquecounter = 0

countattvalxpathtemplate = 'count(.//node[@{att}="{val}"])'
countcompoundxpath = 'count(.//node[contains(@lemma, "_")])'


def countav(stree, att, val):
    countattvalxpath = countattvalxpathtemplate.format(att=att, val=val)
    result = stree.xpath(countattvalxpath)
    return result


def modalinv(node):
    infl = getattval(node, 'infl')
    result = infl == 'modal_inv'
    return result


def getcompoundcount(stree):
    result = stree.xpath(countcompoundxpath)
    return result


def copymodifynode(node, dct):
    newnode = copy(node)
    for att in dct:
        newnode.attrib[att] = dct[att]
    return newnode


def myfind(tree, query):
    list = tree.xpath(query)
    if list == []:
        return None
    else:
        return list[0]


def getmeta(syntree, attname, treebank=True):
    prefix = "." if treebank else ""
    thequery = prefix + metaquerytemplate.format(attname)
    result = getqueryresult(syntree, xpathquery=thequery)
    return result


def normalizedword(stree):
    if stree is None:
        result = None
    elif 'pt' in stree.attrib:
        theword = getattval(stree, 'word')
        thelemma = getattval(stree, 'lemma')
        if theword is None or theword == '':
            result = None
        elif thelemma is None or thelemma == '':
            result = theword.lower()
        else:
            if theword[0].isupper() and thelemma[0].isupper():
                result = theword
            else:
                result = theword.lower()
    else:
        result = None
    return result


def mkproper(astring):
    result = astring.rjust(4, '0')
    return result


def getproperuttid(syntree):
    global uniquecounter
    result1 = getmeta(syntree, 'uttid')
    if result1 is not None:
        result = 'U' + mkproper(result1)
    else:
        result1 = getsentid(syntree)
        if result1 is not None:
            result = 'S' + mkproper(result1)
        else:
            uniquecounter += 1
            result1 = str(uniquecounter)
            result = 'C' + mkproper(result1)
    return result


def ismainclausenode(node):
    nodecat = getattval(node, 'cat')
    catok = nodecat in mainclausecats
    if nodecat == 'sv1':
        parentnode = parent(node)
        parentnodecat = getattval(parentnode, 'cat')
        sv1ok = parentnodecat not in ['whq', 'cp', 'rel', 'whrel', 'whsub']
        result = sv1ok
    else:
        result = catok
    return result


def getuttid(syntree):
    result = getmeta(syntree, 'uttid')
    if result is None:
        result = getsentid(syntree)
        if result is None:
            result = '0'
    return result


def getxsid(syntree):
    result = getmeta(syntree, 'xsid')
    if result is None:
        result = '0'
    return result


def getaltid(syntree):
    result = getmeta(syntree, 'alt')
    return result


def noxpathsentid(syntree):
    results = []
    if syntree is not None:
        for child in syntree:
            if child.tag == 'sentence':
                if 'sentid' in child.attrib:
                    results = [child.attrib['sentid']]
    return results


def getsentid(syntree):
    result = getqueryresult(syntree, noxpathquery=noxpathsentid)
    return result


def lastconstituentof(stree):
    curlastend = 0
    topnodes = stree.xpath('.//node[@cat="top"]')
    topnode = topnodes[0]
    for child in topnode:
        if 'cat' in child.attrib:
            childend = int(getattval(child, 'end'))
            if childend > curlastend:
                result = child
                curlastend = childend
    return result


def getsentence(syntree, treebank=True):
    prefix = "." if treebank else ""
    thequery = prefix + sentencexpathquery
    result = getqueryresult(syntree, xpathquery=thequery)
    return result


def lastmainclauseof(stree):
    topnodes = stree.xpath('.//node[@cat="top"]')
    curlastmainclause = None
    if topnodes != []:
        topnode = topnodes[0]
        for child in topnode:
            curlastmainclause = reclastmainclauseof(child, curlastmainclause)
    return curlastmainclause


def reclastmainclauseof(node, current):
    if node is None:
        result = current
    elif ismainclausenode(node):
        currentend = int(getattval(current, 'end')) if current is not None else 0
        nodeend = int(getattval(node, 'end'))
        if nodeend > currentend:
            result = node
        else:
            result = current
    else:
        for child in node:
            current = reclastmainclauseof(child, current)
        result = current
    return result


def getrelchildof(node, rel):
    '''
    gets the first child node with rel=rel under a node.
    It should always return a word node (so should have a pt attribute; it does not deal properly with conjunction
    :return: node with grammatical relation rel
    '''
    if node is None:
        return None
    for child in node:
        chrel = getattval(child, 'rel')
        if chrel == rel:
            return child
    return None


def getheadof(node):
    return getrelchildof(node, 'hd')


def getdetof(node):
    return getrelchildof(node, 'det')


def getfirstconjunctof(node):
    return getrelchildof(node, 'cnj')


def getextendedheadof(node):
    result1 = getheadof(node)
    if result1 is None:
        result2 = getfirstconjunctof(node)
        if result2 is not None:
            if 'cat' in result2.attrib:
                result = getheadof(result2)
            else:
                result = result2
        else:
            print('here it goes wrong')
            pass

    else:
        result = result1
    return result


persons = ['persoon', '3p', '3m', '3v', '3o', '3', '2v', '2b', '2', '1']
numbers = ['getal', 'ev', 'mv']
genders = ['genus', 'onz', 'zijd', 'fem', 'masc']


def valmerge(v1, v2, vallist):
    '''
    presupposes that v1 and v2 occur in the vallist
    :param v1:
    :param v2:
    :param vallist:
    :return:
    '''
    v1ind = vallist.index(v1)
    v2ind = vallist.index(v2)
    newind = max(v1ind, v2ind)
    result = vallist[newind]
    return result


def phimax(v1, v2):
    if v1 in persons and v2 in persons:
        result = valmerge(v1, v2, persons)
    elif v1 in numbers and v2 in numbers:
        result = valmerge(v1, v2, numbers)
    elif v1 in genders and v2 in genders:
        result = valmerge(v1, v2, genders)
    else:
        SDLOGGER.error('Phimax: Illegal or incompatible value combination: V1={}, v2={}'.format(v1, v2))
        result = v1
    return result


def merge(phi1, phi2):
    (p1, n1, g1) = phi1
    (p2, n2, g2) = phi2
    result = (phimax(p1, p2), phimax(n1, n2), phimax(g1, g2))
    return result


def getconjphi(node):
    crd = tuple(node.xpath('node[@rel="crd"]'))
    conjs = node.xpath('node[@rel="cnj"]')
    conjphis = [getphi(conj) for conj in conjs]
    startphi = ('3', 'getal', 'genus')
    curphi = startphi
    for conjphi in conjphis:
        curphi = merge(curphi, conjphi)
    if crd in pluralcrds:
        (p, n, g) = curphi
        curphi = (p, 'mv', g)
    return curphi


def getlemma(node):
    if node is None:
        result = ''
    elif 'cat' in node.attrib:
        nodecat = getattval(node, 'cat')
        if nodecat == 'conj':
            result = ''
        elif nodecat == 'mwu':
            result = ''
        else:
            hnode = getheadof(node)
            result = getlemma(hnode)
    elif 'pt' in node.attrib:
        result = getattval(node, 'lemma')
    else:
        result = ''
    return result


def getphi(node):
    if node is None:
        return None
    elif 'cat' in node.attrib:
        nodecat = getattval(node, 'cat')
        if nodecat == 'conj':
            result = getconjphi(node)
            return result
        elif nodecat == 'mwu':
            result = ('3', 'getal', 'genus')
            return result
        else:
            hnode = getheadof(node)
            result = getphi(hnode)
            return result
    elif 'pt' in node.attrib:
        if 'persoon' in node.attrib:
            person = getattval(node, 'persoon')
        else:
            person = '3'
        if 'getal' in node.attrib:
            number = getattval(node, 'getal')
        else:
            number = 'ev'
        if 'genus' in node.attrib:
            gender = getattval(node, 'genus')
        else:
            gender = 'genus'
        result = (person, number, gender)
        return result


def inverted(thesubj, thepv):
    subjphi = getphi(thesubj)
    if subjphi is None:
        return False
    (subjperson, subjnumber, subjgender) = getphi(thesubj)
    tense = getattval(thepv, 'pvtijd')
    subjbegin = getattval(thesubj, 'begin')
    subjlemma = getattval(thesubj, 'lemma')
    pvend = getattval(thepv, 'end')
    inversion = '2' == subjperson[0] and tense == 'tgw' and subjnumber in ['ev', 'getal'] and \
                pvend == subjbegin and subjlemma in ['jij', 'je']  # getal added for je
    return inversion


def getattval(node, att):
    if node is None:
        result = ''
    elif att in node.attrib:
        result = node.attrib[att]
    else:
        result = ''
    return result


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def number2intstring(numberstr):
    if is_number(numberstr):
        result = str(int(numberstr))
    else:
        result = numberstr
    return result


def getqueryresult(syntree, xpathquery=None, noxpathquery=None):
    if syntree is None:
        result = None
    else:
        if xpathquery is not None:
            results = syntree.xpath(xpathquery)
        elif noxpathquery is not None:
            results = noxpathquery(syntree)
        else:
            results = []
        if len(results) == 0:
            result = None
        elif len(results) > 1:
            result1 = results[0]
            result = number2intstring(result1)
            # issue a warning
        elif len(results) == 1:
            result1 = results[0]
            result = number2intstring(result1)
    return result


def getnodeyield(syntree):
    resultlist = []
    for node in syntree.iter():
        if 'pt' in node.attrib or 'pos' in node.attrib:
            resultlist.append(node)
    sortedresultlist = sorted(resultlist, key=lambda x: int(getattval(x, 'end')))
    return sortedresultlist


def getyield(syntree):  # deze herformuleren in termen van getnodeyield na testen
    resultlist = []
    if syntree is None:
        theyield = []
    else:
        for node in syntree.iter():
            if 'pt' in node.attrib or 'pos' in node.attrib:
                if 'word' in node.attrib and 'end' in node.attrib:
                    newel = (node.attrib['word'], int(node.attrib['end']))
                    resultlist.append(newel)
                else:
                    if 'word' not in node.attrib:
                        SDLOGGER.error('No word in pt or pos node')
                    if 'end' not in node.attrib:
                        SDLOGGER.error('No end in pt or pos node')
                    for el in node.attrib:
                        SDLOGGER.info('{}\t{}'.format(el, node.attrib[el]))
        sortedresultlist = sorted(resultlist, key=lambda x: x[1])
        theyield = [w for (w, _) in sortedresultlist]
    return theyield


def parent(node):
    pnodes = node.xpath('parent::node')
    if pnodes == []:
        result = None
    else:
        result = pnodes[0]
    return result


def is_left_sibling(node1, node2):
    sameparent = parent(node1) == parent(node2)
    node1_end = getattval(node1, 'end')
    node2_end = getattval(node2, 'end')
    result = sameparent and node1_end < node2_end
    return result


def get_left_siblings(node):
    thesiblings = node.xpath('../node')
    theleftsiblings = [s for s in thesiblings if is_left_sibling(s, node)]
    return theleftsiblings


def getmarkedutt(m, syntree):
    thewordlist = getyield(syntree)
    thepositions = getwordpositions(m, syntree)
    themarkedyield = getmarkedyield(thewordlist, thepositions)
    yieldstr = space.join(themarkedyield)
    return yieldstr


def mark(str):
    result = '*' + str + '*'
    return result


def getwordpositions(matchtree, syntree):
    # nothing special needs to be done for index nodes since they also have begin and end
    positions = []
    for node in matchtree.iter():
        if 'end' in node.attrib:
            positions.append(node.attrib['end'])
    result = [int(p) for p in positions]
    return result


def getmarkedyield(wordlist, positions):
    pos = 1
    resultlist = []
    for w in wordlist:
        if pos in positions:
            resultlist.append(mark(w))
        else:
            resultlist.append(w)
        pos += 1
    return resultlist


def addmetadata(stree, meta):
    '''
    adds  meta of class Metadata to stree
    :param stree:
    :param meta: type Metadata
    :return: stree
    '''
    if stree is None:
        result = stree
    elif meta is None:
        result = stree
    else:
        metadatanodes = stree.xpath('//metadata')
        if metadatanodes == []:
            metadatanode = etree.Element('metadata')
            stree.append(metadatanode)
        else:
            metadatanode = metadatanodes[0]  # we append to the first metadata node if there would be multiple (which should not be the case)
        metadatanode.append(meta)
        result = stree
    return result


def iswordnode(thenode):
    result = 'pt' in thenode.attrib or 'pos' in thenode.attrib
    return result


def istrueclausalnode(thenode):
    thenodecat = getattval(thenode, 'cat')
    result1 = thenodecat in trueclausecats
    if result1:
        ssubfound = False
        for child in thenode:
            if getattval(child, 'cat') == 'ssub':
                ssubfound = True
                break
        result = ssubfound
    else:
        result = False
    return result


def iscompound(node):
    lemma = getattval(node, 'lemma')
    result = compoundsep in lemma
    return result


def isdiminutive(node):
    graad = getattval(node, 'graad')
    result = graad == 'dim'
    return result


def issubstantivised_verb(node):
    nodept = getattval(node, 'pt')
    nodepositie = getattval(node, 'positie')
    result = nodept == 'ww' and nodepositie == 'nom'
    return result


def getsiblings(node):
    parent = node.getparent()
    siblings = [n for n in parent if n != node]
    return siblings


def showtn(tokennode):
    '''requires the node to be a node for a token (word)'''
    if tokennode is None:
        result = ''
    else:
        word = getattval(tokennode, 'word')
        position = getattval(tokennode, 'end')
        result = position + word
    return result


def showtns(tokennodelist):
    result = space.join([showtn(tn) for tn in tokennodelist])
    return result


def all_lower_consonantsnode(node):
    word = getattval(node, 'word')
    result = all([c.islower() for c in word])
    result = result and allconsonants(word)
    return result


def sasta_long(node):
    word = getattval(node, 'word')
    result = len(word) >= min_sasta_length
    return result


def spec_noun(node):
    pt = getattval(node, 'pt')
    pos = getattval(node, 'pos')
    frame = getattval(node, 'frame')
    word = getattval(node, 'word')
    result = (pt == 'spec' and (pos == 'name' or frame.startswith('proper_name')))
    result = result and word[0].isupper()
    return result


def is_duplicate_spec_noun(node):
    siblings = getsiblings(node)
    result = True
    word = getattval(node, 'word')
    lcword = word.lower()
    for sibling in siblings:
        siblingword = getattval(sibling, 'word')
        lcsiblingword = siblingword.lower()
        result = result and lcword == lcsiblingword
    return result


def asta_recognised_nounnode(node):
    if issubstantivised_verb(node):
        pos = 'ww'
    else:
        pos = 'n'
    result = sasta_pseudonym(node)
    result = result or spec_noun(node)
    result = result or is_duplicate_spec_noun(node)
    result = result or sasta_long(node)
    result = result or recognised_wordnodepos(node, pos)
    result = result or recognised_lemmanodepos(node, pos)
    result = result and not(all_lower_consonantsnode(node))
    result = result and not(short_nucl_n(node))
    return result


def asta_recognised_wordnode(node):
    result = sasta_pseudonym(node)
    result = result or spec_noun(node)
    result = result or is_duplicate_spec_noun(node)
    result = result or sasta_long(node)
    result = result or recognised_wordnode(node)
    result = result or recognised_lemmanode(node)
    result = result and not(all_lower_consonantsnode(node))
    result = result and not(short_nucl_n(node))
    return result


def sasta_short(inval):
    result = len(inval) <= sasta_short_length
    return result


def short_nucl_n(node):
    pt = getattval(node, 'pt')
    rel = getattval(node, 'rel')
    word = getattval(node, 'word')
    result = pt == 'n' and rel == 'nucl' and sasta_short(word)
    return result


sasta_pseudonyms = ['NAAM', 'VOORNAAM', 'ACHTERNAAM', 'ZIEKENHUIS', 'STRAAT', 'PLAATS', 'PLAATSNAAM', 'KIND', 'BEROEP', 'OPLEIDING']
pseudonym_patternlist = [r'^{}\d?$'.format(el) for el in sasta_pseudonyms]
pseudonym_pattern = vertbar.join(pseudonym_patternlist)
pseudonymre = re.compile(pseudonym_pattern)


def sasta_pseudonym(node):
    word = getattval(node, 'word')
    match = pseudonymre.match(word)
    result = match is not None
    return result


def recognised_wordnodepos(node, pos):
    word = getattval(node, 'word')
    lcword = word.lower()
    result = informlexiconpos(word, pos) or informlexiconpos(lcword, pos) or \
        iscompound(node) or isdiminutive(node) or isa_namepart_uc(word)
    return result


def recognised_wordnode(node):
    word = getattval(node, 'word')
    lcword = word.lower()
    result = informlexicon(word) or informlexicon(lcword) or iscompound(node) or isdiminutive(node) or isa_namepart(word)
    return result


def recognised_lemmanode(node):
    lemma = getattval(node, 'lemma')
    result = informlexicon(lemma)
    return result


def recognised_lemmanodepos(node, pos):
    lemma = getattval(node, 'lemma')
    result = informlexiconpos(lemma, pos)
    return result


nodeformat = '{}/{}{}'
nodeformatplus = nodeformat + '['


def simpleshow(stree, showchildren=True, newline=True):
    simpleshow2(stree, showchildren)
    if newline:
        print()


def simpleshow2(stree, showchildren=True):
    rel = getattval(stree, 'rel')
    cat = getattval(stree, 'cat')
    index = getattval(stree, 'index')
    indexstr = ':' + index if index != '' else ''
    begin = getattval(stree, 'begin')
    end = getattval(stree, 'end')
    theformat = nodeformatplus if showchildren else nodeformat
    if cat != '':
        print(theformat.format(rel, cat, indexstr), end=' ')
        if showchildren:
            for child in stree:
                simpleshow2(child)
            print(']', end=' ')
        else:
            print('{}-{}'.format(begin, end))
    elif getattval(stree, 'pt') != '':
        print(nodeformat.format(rel, showtn(stree), indexstr), end=' ')
    elif getattval(stree, 'pos') != '':
        print(nodeformat.format(rel, showtn(stree), indexstr), end=' ')
    else:
        index = getattval(stree, 'index')
        if index != '':
            print(nodeformat.format(rel, '', indexstr), end=' ')
        else:
            # print('top', end=' ')
            for child in stree:
                simpleshow2(child)
            # print(']', end=' ')


def showflatxml(elem):
    '''

    :param elem: xml element
    :return: string that represents the element and its immediate children
    '''
    start = '<{}>'.format(elem.tag)
    end = '</{}>'.format(elem.tag)
    middle = ['<{}/>'.format(child.tag) for child in elem]
    middlestr = space.join(middle)
    result = start + middlestr + end
    return result


def uniquenodes(nodelist):
    '''

    :param nodelist: list of nodes all from a single syntactic structure
    :return: nodelist without duplicates. Two nodes are considered duplicates if the begin and end attributes are identical
    '''
    done = []
    resultlist = []
    for node in nodelist:
        begin = getattval(node, 'begin')
        end = getattval(node, 'end')
        cover = begin, end
        if cover not in done:
            resultlist.append(node)
            done.append(cover)
    return resultlist


def getindexednodesmap(stree):
    indexednodes = {}
    for node in stree.iter():
        if 'index' in node.attrib and ('pt' in node.attrib or 'cat' in node.attrib or 'pos' in node.attrib):
            theindex = node.attrib['index']
            indexednodes[theindex] = node
    return indexednodes


def nodecopy(node):
    '''
    copies a node without its children
    :param node: node, an lxml.etree Element
    :return: a node with no children, otherwise a copy of the input node
    '''
    newnode = copy(node)
    for ch in newnode:
        newnode.remove(ch)
    return newnode


def bareindexnode(node):
    result = terminal(node) and 'index' in node.attrib and 'postag' not in node.attrib and 'cat' not in node.attrib and 'pt' not in node.attrib and 'pos' not in node.attrib
    # print(props2str(get_node_props(node)), result, file=sys.stderr)
    return(result)


def terminal(node):
    result = len(node) == 0
    return(result)


def indextransform(stree):
    '''
    produces a new stree in which all index nodes are replaced by their antecedent nodes
    :param stree: input stree
    :return: stree with all index nodes replaced by the nodes of their antecedents
    '''

    indexednodesmap = getindexednodesmap(stree)

    result = indextransform2(stree, indexednodesmap)
    return result


def indextransform2(stree, indexednodesmap):
    if bareindexnode(stree):
        theindex = getattval(stree, 'index')
        therel = getattval(stree, 'rel')
        newstree = deepcopy(indexednodesmap[theindex])
        newstree.attrib['rel'] = therel
        # simpleshow(newstree)
        # print()
    else:
        newstree = nodecopy(stree)
        # simpleshow(newstree)
        # print(id(stree))
        # print(id(newstree))
        # print(len(newstree))
        # print(id(newstree.getparent()))
        # print(id(None))
        for child in stree:
            newchild = indextransform2(child, indexednodesmap)
            newstree.append(newchild)

    return newstree


def getstree(fullname):
    try:
        thefile = open(fullname, 'r', encoding='utf8')
    except FileNotFoundError as e:
        SDLOGGER.error('File not found: {}'.format(e))
        return None
    except etree.ParseError as e:
        SDLOGGER.error('Parse Error: {}; file: {}'.format(e, fullname))
        return None
    except OSError as e:
        SDLOGGER.error('OS Error: {}; file: {}'.format(e, fullname))
        return None
    except Exception:
        SDLOGGER.error('Error: Unknown error in file {}'.format(fullname))
        return None

    with thefile:
        try:
            tree = etree.parse(thefile)
        except etree.ParseError as e:
            SDLOGGER.error('Parse Error: {}; file: {}'.format(e, fullname))
            return None
        except UnicodeDecodeError as e:
            SDLOGGER.error('Unicode error: {} in file {}'.format(e, fullname))
            try:
                windowsfile = open(fullname, 'r')
                tree = etree.parse(windowsfile)
            except ValueError as e:
                SDLOGGER.error('Char Descoding Error: {}; file: {}'.format(e, fullname))
                return None
            except etree.ParseError:
                SDLOGGER.error('Parse Error: {}; file: {}'.format(e, fullname))
                return None
            else:
                return tree
        else:
            return tree


def getsentid(stree):
    sentidlist = stree.xpath(sentidxpath)
    if sentidlist == []:
        SDLOGGER.error('Missing uttid')
        uttid = 'None'
    else:
        uttid = str(sentidlist[0])
    return uttid


def transplant_node(node1, node2, stree):
    '''
    replace node1 by node2 in stree
    Only do so if node1 and node2 have no children and if their spans are identical
    :param node1: node to be replaced in stree
    :param node2: node to replace node1 in stree
    :param stree: tree in which the replacement takes place
    :return: None, the stree input parameter is modified
    '''
    # find the parent of node1
    # determine the index of node1
    sentid = getsentid(stree)
    parentindex = get_parentandindex(node1, stree)
    if parentindex is None:
        result = stree
    else:
        parent, index = parentindex
        # SDLOGGER.debug(simpleshow(parent))
        del parent[index]
        # SDLOGGER.debug(simpleshow(parent))
        parent.insert(index, node2)
        # SDLOGGER.debug(simpleshow(parent))
        result = stree
        # SDLOGGER.debug(simpleshow(stree))

    # adapt the sentence
    # find the sentence element's parent and its index
    sentencenode = stree.find('.//sentence')
    sentencenodeparent = sentencenode.getparent()
    sentencenodeindex = sentencenodeparent.index(sentencenode)
    del sentencenodeparent[sentencenodeindex]
    theyield = getyield(stree)
    theyieldstr = space.join(theyield)
    newsentence = etree.Element('sentence')
    newsentence.text = theyieldstr
    newsentence.attrib['sentid'] = sentid
    sentencenodeparent.insert(sentencenodeindex, newsentence)

    return stree


def get_parentandindex(node, stree):
    '''

    :param node: node to find the parent of
    :param stree: stree to find the parent of node in
    :return: (parentnode::node, index::int) or None
    '''

    nodespan = getspan(node)
    idx = 0
    for child in stree:
        childspan = getspan(child)
        if childspan == nodespan:
            return (stree, idx)
        else:
            chresult = get_parentandindex(node, child)
            if chresult is not None:
                return chresult
        idx += 1
    return None


def getspan(node):
    nodebegin = getattval(node, 'begin')
    nodeend = getattval(node, 'end')
    nodespan = (nodebegin, nodeend)
    return nodespan


def lbrother(node, tree):
    nodebegin = getattval(node, 'begin')

    def condition(n):
        return getattval(n, 'end') == nodebegin
    result = findfirstnode(tree, condition)
    return result


def rbrother(node, tree):
    nodeend = getattval(node, 'end')

    def condition(n):
        return getattval(n, 'begin') == nodeend
    result = findfirstnode(tree, condition)
    return result


def findfirstnode(tree, condition):
    if condition(tree):
        return tree
    else:
        for child in tree:
            result = findfirstnode(child, condition)
            if result is not None:
                return result
    return None


def nominal(node):
    pt = getattval(node, 'pt')
    cat = getattval(node, 'cat')
    if cat != '':
        result = cat = 'np'
    elif pt != '':
        result = pt in ['n', 'vnw']
    else:
        result = False
    return result


def decomposetree(tree):
    metadata, sentence, comments, nod, parser = None, None, None, None, None
    for child in tree:
        if child.tag == 'metadata':
            metadata = child
        elif child.tag == 'sentence':
            sentence = child
        elif child.tag == 'comments':
            comments = child
        elif child.tag == 'node':
            node = child
        elif child.tag == 'parser':
            parser = child
        else:
            SDLOGGER.error('Unknown tag encountered in tree: {}'.format(child.tag))
    return parser, metadata, node, sentence, comments


comma = ','


def str2list(liststr, sep=comma):
    bareliststr = liststr[1:-1]
    rawlist = bareliststr.split(comma)
    cleanlist = [x.strip() for x in rawlist]
    return cleanlist


def find1(tree, xpathquery):
    if tree is None:
        return None
    results = tree.xpath(xpathquery)
    if results == []:
        result = None
    else:
        result = results[0]
    return result


def getxmetatreepositions(tree, xmetaname):
    query = ".//xmeta[@name='{}']".format(xmetaname)
    xmeta = find1(tree, query)
    annposstr = xmeta.get('annotationposlist')
    annposlist = str2list(annposstr)
    cleantok = find1(tree, './/xmeta[@name="cleanedtokenpositions"]')
    tokliststr = cleantok.get('value')
    toklist = str2list(tokliststr)
    result = [str(toklist.index(pos)) for pos in annposlist]
    return result
