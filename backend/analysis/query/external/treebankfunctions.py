'''
various treebank functions

'''
from lxml import etree
import logging

logger = logging.getLogger('sasta')


class Metadata:
    '''
    contains 3 elements, each a string type, name, value
    '''

    def __init__(self, thetype, thename, thevalue):
        self.type = thetype
        self.name = thename
        self.value = thevalue

    def md2PEP(self):
        result = '##META {} {} = {}'.format(self.type, self.name, self.value)
        return result

    def md2XMLElement(self):
        result = etree.Element('meta', type=self.type,
                               name=self.name, value=self.value)
        return result


space = ' '

allrels = ['hdf', 'hd', 'cmp', 'sup', 'su', 'obj1', 'pobj1', 'obj2', 'se', 'pc', 'vc', 'svp', 'predc', 'ld', 'me', 'predm',
           'obcomp', 'mod', 'body', 'det', 'app', 'whd', 'rhd', 'cnj', 'crd', 'nucl', 'sat', 'tag', 'dp', 'top', 'mwp', 'dlink', '--']

allcats = ['smain', 'np', 'ppart', 'pp', 'ssub', 'inf', 'cp', 'du', 'ap', 'advp', 'ti',
           'rel', 'whrel', 'whsub', 'conj', 'whq', 'oti', 'ahi', 'detp', 'sv1', 'svan', 'mwu', 'top']

clausecats = ['smain', 'ssub', 'inf', 'cp', 'ti', 'rel',
              'whrel', 'whsub', 'whq', 'oti', 'ahi', 'sv1', 'svan']

trueclausecats = ['smain', 'cp', 'rel',
                  'whrel', 'whsub', 'whq', 'sv1', 'svan']

complrels = ['su', 'obj1', 'pobj1', 'obj2',
             'se', 'pc', 'vc', 'svp', 'predc', 'ld']

mainclausecats = ['smain', 'whq', 'sv1']


# uttidquery = ".//meta[@name='uttid']/@value"
sentidquery = ".//sentence[@name='sentid']/@value"
# altquery = ".//meta[@name='alt']/@value"
metaquerytemplate = ".//meta[@name='{}']/@value"
uniquecounter = 0


def getmeta(syntree, attname):
    thequery = metaquerytemplate.format(attname)
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
        currentend = int(getattval(current, 'end')
                         ) if current is not None else 0
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
    sortedresultlist = sorted(
        resultlist, key=lambda x: int(getattval(x, 'end')))
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
                        logger.error('No word in pt or pos node')
                    if 'end' not in node.attrib:
                        logger.error('No end in pt or pos node')
                    for el in node.attrib:
                        logger.info('{}\t{}'.format(el, node.attrib[el]))
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
            # we append to the first metadata node if there would be multiple (which should not be the case)
            metadatanode = metadatanodes[0]
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
