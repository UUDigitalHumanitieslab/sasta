from collections import defaultdict
from copy import copy, deepcopy

from lxml import etree
from sastadev import PARSE_FUNC, SDLOGGER
from sastadev.cleanCHILDEStokens import cleantext
from sastadev.corrector import getcorrections
from sastadev.lexicon import de, dets, known_word
from sastadev.metadata import Meta, bpl_node, bpl_none, bpl_word
from sastadev.sva import phicompatible
from sastadev.targets import get_mustbedone
from sastadev.treebankfunctions import (countav, find1, getattval,
                                        getcompoundcount, getnodeyield,
                                        getsentid, getyield, myfind,
                                        showflatxml, simpleshow,
                                        transplant_node)
from sastadev.sastatok import sasta_tokenize

corr0, corr1, corrn = '0', '1', 'n'
validcorroptions = [corr0, corr1, corrn]

space = ' '
origuttxpath = './/meta[@name="origutt"]/@value'
uttidxpath = './/meta[@name="uttid"]/@value'
metadataxpath = './/metadata'

contextualproperties = ['rel', 'index', 'positie']

errorwbheader = ['Sample', 'User1', 'User2', 'User3'] + \
                ['Status', 'Uttid', 'Origutt', 'Origsent'] + \
                ['altid', 'altsent', 'penalty', 'dpcount', 'dhyphencount', 'dimcount', 'compcount', 'supcount',
                 'compoundcount', 'unknownwordcount', 'sucount', 'svaokcount', 'deplusneutcount', 'goodcatcount']


def get_origandparsedas(metadatalist):
    parsed_as = None
    origutt = None
    for meta in metadatalist:
        if parsed_as is None or origutt is None:
            key = meta.attrib['name']
            if key == 'parsed_as':
                parsed_as = meta.attrib['value']
            if key == 'origutt':
                origutt = meta.attrib['value']
    return origutt, parsed_as


def mkmetarecord(meta, origutt, parsed_as):
    if meta is None:
        return None, []
    key = meta.attrib['name']
    if meta.tag == 'xmeta':
        if meta.attrib['source'] in ['CHAT', 'SASTA']:
            newmetarecord = [meta.attrib['name'], meta.attrib['value'], meta.attrib['source'], meta.attrib['cat'],
                             meta.attrib['subcat'], origutt, parsed_as]
            return key, newmetarecord
        else:
            return key, []
    else:
        return key, []


def updateerrordict(errordict, uttid, oldtree, newtree):
    metadatalist = newtree.find(metadataxpath)
    if metadatalist is not None:
        origutt, parsed_as = get_origandparsedas(metadatalist)

        for meta in metadatalist:
            key, newmetarecord = mkmetarecord(meta, origutt, parsed_as)
            if key is not None and newmetarecord != []:
                errordict[key].append([uttid] + newmetarecord)
    return errordict


def correcttreebank(treebank, targets, method, corr=corrn):
    allorandalts = []
    errordict = defaultdict(list)
    if corr == corr0:
        return treebank, errordict, allorandalts
    else:
        newtreebank = etree.Element('treebank')
        errorlogrows = []
        for stree in treebank:
            uttid = getuttid(stree)
            mustbedone = get_mustbedone(stree, targets)
            if mustbedone:
                # to implement
                newstree, orandalts = correct_stree(stree, method, corr)
                if newstree is not None:
                    errordict = updateerrordict(errordict, uttid, stree, newstree)
                    newtreebank.append(newstree)
                    allorandalts.append(orandalts)
                else:
                    newtreebank.append(stree)
            else:
                newtreebank.append(stree)

        return newtreebank, errordict, allorandalts


def contextualise(node1, node2):
    '''
    copies the contextually determined properties of node2 to node1
    :param node1:
    :param node2:
    :return: adapted version of node1
    '''
    newnode = copy(node1)
    for prop in contextualproperties:
        if prop in node2.attrib:
            newnode.attrib[prop] = node2.attrib[prop]
    return newnode


def correct_stree(stree, method, corr):
    '''

    :param stree:
    :return:
    '''

    debug = False
    if debug:
        print('1:', end=': ')
        simpleshow(stree)
        print(showflatxml(stree))

    allmetadata = []
    allorandalts = []

    # uttid:
    uttid = getuttid(stree)
    sentid = getsentid(stree)

    # get the original utterance

    origutt = getorigutt(stree)
    if origutt is None:
        SDLOGGER.error('Missing origutt in utterance {}'.format(uttid))
        return stree

    # get the original metadata; these will be added later to the tree of each correction
    metadatalist = stree.xpath(metadataxpath)
    lmetadatalist = len(metadatalist)
    if lmetadatalist == 0:
        SDLOGGER.error('Missing metadata in utterance {}'.format(uttid))
    elif lmetadatalist > 1:
        SDLOGGER.error('Multiple metadata ({}) in utterance {}'.format(lmetadatalist, uttid))
    else:
        origmetadata = metadatalist[0]

    # allmetadata += origmetadata
    # clean in the tokenized manner

    cleanutt, metadata = cleantext(origutt, False)
    allmetadata += metadata
    cleanutttokens = sasta_tokenize(cleanutt)
    cleanuttwordlist = [t.word for t in cleanutttokens]

    # get corrections, given the stree

    cwmds = getcorrections(cleanutt, method, stree)

    if debug:
        print('2:', end=': ')
        simpleshow(stree)
        print(showflatxml(stree))

    ptmds = []
    for correctionwordlist, cwmdmetadata in cwmds:
        cwmdmetadata += allmetadata

        # parse the corrections
        if correctionwordlist != cleanuttwordlist:
            correction = space.join(correctionwordlist)
            cwmdmetadata += [Meta('parsed_as', correction, cat='Correction', source='SASTA')]
            newstree = PARSE_FUNC(correction)
            if newstree is None:
                newstree = stree  # is this what we want?@@
            else:
                mdcopy = deepcopy(origmetadata)
                newstree.insert(0, mdcopy)
                # copy the sentid attribute
                sentencenode = getsentencenode(newstree)
                if sentencenode is not None:
                    sentencenode.attrib['sentid'] = sentid
                if debug:
                    print(etree.tostring(newstree, pretty_print=True))

        else:
            newstree = stree

        ptmds.append((correctionwordlist, newstree, cwmdmetadata))

    # select the stree for the most promising correction
    if debug:
        print('3:', end=': ')
        simpleshow(stree)
        print(showflatxml(stree))

    if ptmds == []:
        thecorrection, orandalts = (cleanutt, stree, origmetadata), None
    elif corr in [corr1, corrn]:
        thecorrection, orandalts = selectcorrection(stree, ptmds, corr)
    else:
        SDLOGGER.error('Illegal correction value: {}. No corrections applied'.format(corr))
        thecorrection, orandalts = (cleanutt, stree, origmetadata), None

    thetree = deepcopy(thecorrection[1])

    if debug:
        print('4:', end=': ')
        simpleshow(stree)
        print(showflatxml(stree))

    # do replacements in the tree

    # resultposmeta = selectmeta('cleanedtokenpositions', allmetadata)
    # resultposlist = resultposmeta.value

    for meta in thecorrection[2]:
        if meta.backplacement == bpl_node:
            nodeend = meta.annotationposlist[-1] + 1
            newnode = thetree.find('.//node[@end="{}"]'.format(nodeend))
            oldnode = stree.find('.//node[@end="{}"]'.format(nodeend))
            if newnode is not None and oldnode is not None:
                # adapt oldnode1 for contectual features
                contextoldnode = contextualise(oldnode, newnode)
                thetree = transplant_node(newnode, contextoldnode, thetree)
        elif meta.backplacement == bpl_word:
            nodeend = meta.annotationposlist[-1] + 1
            nodexpath = './/node[@begin="{}" and @end="{}"]'.format(nodeend - 1, nodeend)
            newnode = myfind(thetree, nodexpath)
            oldnode = myfind(stree, nodexpath)
            if newnode is not None and oldnode is not None:
                if 'word' in newnode.attrib and 'word' in oldnode.attrib:
                    newnode.attrib['word'] = oldnode.attrib['word']
                else:
                    if 'word' not in oldnode.attrib:
                        SDLOGGER.error('Unexpected missing "word" attribute in utterance {}, node {}'.format(uttid, simpleshow(oldnode, showchildren=False)))
                    if 'word' not in newnode.attrib:
                        SDLOGGER.error('Unexpected missing "word" attribute in utterance {}, node {}'.format(uttid, simpleshow(oldnode, showchildren=False)))
        elif meta.backplacement == bpl_none:
            pass

    if debug:
        print('5:', end=': ')
        simpleshow(stree)
        print(showflatxml(stree))

    restoredtree = thetree

    # add the metadata to the tree
    fulltree = restoredtree

    metadata = fulltree.find('.//metadata')
    if metadata is None:
        metadata = etree.Element('metadata')
        fulltree.insert(0, metadata)

    for meta in thecorrection[2]:
        metadata.append(meta.toElement())

    # newfulltree = etree.ElementTree(fulltree)
    # outfilename = 'correctedtree_{}.xml'.format(uttid)
    # newfulltree.write(outfilename, encoding="UTF8", xml_declaration=False,
    #                pretty_print=True)

    # return this stree
    return fulltree, orandalts


def getsentencenode(stree):
    sentnodes = stree.xpath('.//sentence')
    if sentnodes == []:
        result = None
    else:
        result = sentnodes[0]
    return result


def getuttid(stree):
    uttidlist = stree.xpath(uttidxpath)
    if uttidlist == []:
        SDLOGGER.error('Missing uttid')
        uttid = 'None'
    else:
        uttid = uttidlist[0]
    return uttid


def getorigutt(stree):
    origuttlist = stree.xpath(origuttxpath)
    if origuttlist == []:
        origutt = None
    else:
        origutt = origuttlist[0]
    return origutt


class Alternative():
    def __init__(self, stree, altid, altsent, penalty, dpcount, dhyphencount, dimcount,
                 compcount, supcount, compoundcount, unknownwordcount, sucount, svaok, deplusneutcount, goodcatcount):
        self.stree = stree
        self.altid = altid
        self.altsent = altsent
        self.penalty = penalty
        self.dpcount = dpcount
        self.dhyphencount = dhyphencount
        self.dimcount = dimcount
        self.compcount = compcount
        self.supcount = supcount
        self.compoundcount = compoundcount
        self.unknownwordcount = unknownwordcount
        self.sucount = sucount
        self.svaok = svaok
        self.deplusneutcount = deplusneutcount
        self.goodcatcount = goodcatcount

    def alt2row(self, uttid, base, user1='', user2='', user3=''):
        therow = [base, user1, user2, user3] + \
                 ['Alternative', uttid] + 2 * [''] +\
                 [self.altid, self.altsent, self.penalty, self.dpcount, self.dhyphencount,
                  self.dimcount, self.compcount, self.supcount, self.compoundcount, self.unknownwordcount, self.sucount,
                  self.svaok, self.deplusneutcount, self.goodcatcount]
        return therow


class Original():
    def __init__(self, uttid, stree):
        self.uttid = uttid
        self.stree = stree

    def original2row(self, base, user1='', user2='', user3=''):
        origutt = getorigutt(self.stree)
        origtokenlist = getyield(self.stree)
        origsent = space.join(origtokenlist)
        therow = [base, user1, user2, user3] + \
                 ['Original', self.uttid, origutt, origsent]
        return therow


class OrigandAlts():
    def __init__(self, orig, alts, selected=None):
        self.orig = orig
        self.alts = alts  # a dictionary with altid as key
        self.selected = selected

    def OrigandAlts2rows(self, base, user1='', user2='', user3=''):
        origrow = self.orig.original2row(base, user1, user2, user3)
        altsrows = [self.alts[altid].alt2row(self.orig.uttid, base, user1, user2, user3) for altid in self.alts]
        laltsrows = len(altsrows)
        selectedrow = [base, user1, user2, user3] + \
                      ['Selected', self.orig.uttid, '', self.alts[self.selected].altsent, self.selected]
        if laltsrows > 1:
            rows = [origrow] + altsrows + [selectedrow]
        else:
            rows = []
        return rows


def getsvaokcount(nt):
    subjects = nt.xpath('.//node[@rel="su"]')
    counter = 0
    for subject in subjects:
        pv = find1(subject, '../node[@rel="hd" and @pt="ww" and @wvorm="pv"]')
        if phicompatible(subject, pv):
            counter += 1
    return counter


def getdeplusneutcount(nt):
    theyield = getnodeyield(nt)
    ltheyield = len(theyield)
    counter = 0
    for i in range(ltheyield - 1):
        node1 = theyield[i]
        node2 = theyield[i + 1]
        if getattval(node1, 'lemma') in dets[de] and getattval(node2, 'genus') == 'onz':
            counter += 1
    return counter


def selectcorrection(stree, ptmds, corr):
    # to be implemented@@
    # it is presupposed that ptmds is not []

    uttid = getuttid(stree)
    orig = Original(uttid, stree)

    altid = 0
    alts = {}
    for cw, nt, md in ptmds:
        altsent = space.join(cw)
        penalty = compute_penalty(md)
        dpcount = countav(nt, 'rel', 'dp')
        dhyphencount = countav(nt, 'rel', '--')
        dimcount = countav(nt, 'graad', 'dim')
        compcount = countav(nt, 'graad', 'comp')
        supcount = countav(nt, 'graad', 'sup')
        compoundcount = getcompoundcount(nt)
        unknownwordcount = len([w for w in nt.xpath('.//node[@pt]/@lemma') if not(known_word(w))])
        sucount = countav(nt, 'rel', 'su')
        svaokcount = getsvaokcount(nt)
        deplusneutcount = getdeplusneutcount(nt)
        goodcatcount = len([node for node in nt.xpath('.//node[@cat and (@cat!="du")]')])
        alt = Alternative(stree, altid, altsent, penalty, dpcount, dhyphencount, dimcount, compcount, supcount,
                          compoundcount, unknownwordcount, sucount, svaokcount, deplusneutcount, goodcatcount)
        alts[altid] = alt
        altid += 1
    orandalts = OrigandAlts(orig, alts)

    if corr == corr1:
        orandalts.selected = altid - 1
    else:
        # @@to be implemented@@
        orandalts.selected = altid - 1

    result = ptmds[orandalts.selected]
    return result, orandalts


def compute_penalty(md):
    totalpenalty = 0
    for meta in md:
        totalpenalty += meta.penalty
    return totalpenalty
