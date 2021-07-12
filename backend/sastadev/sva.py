from lxml import etree
from sastadev.treebankfunctions import (getattval, inverted, getheadof, getdetof, copymodifynode,
                                        simpleshow, nominal, rbrother, lbrother, indextransform, getlemma)
from sastadev.lexicon import getinflforms, informlexiconpos, getwordposinfo, pvinfl2dcoi
from sastadev.metadata import mkSASTAMeta, bpl_node
from sastadev.sastatoken import Token
from sastadev import SDLOGGER
from sastadev.tokenmd import TokenListMD

debug = False

nominalpts = ['n', 'vnw', 'tw']
nominalisablepts = ['adj', 'ww']

normalsentencexpath = """.//node[@pt="ww" and  @wvorm="pv" and
       parent::node[(@cat="smain" or @cat="sv1") and
           parent::node[@cat="top" and count(node[@cat or  @pt!="let"])=1]]]"""

normalwhqsentencexpath = """
//node[@pt="ww" and  @wvorm="pv" and
       parent::node[( @cat="sv1") and
           parent::node[@cat="whq" and
               parent::node[@cat="top" and count(node[@cat or  @pt!="let"])=1]]]]"""

abnormalobj2sentencexpath = """.//node[@pt="ww" and  @wvorm="pv" and
       parent::node[node[@rel="obj2" and (@pt="vnw" or @word="zij")]]]
"""

abnormalobj2xpath = """.//node[@rel="obj2" and (@pt="vnw" or @word="zij")
        and parent::node[node[@pt="ww" and @wvorm="pv"]]]"""

subjxpath = """.//node[@rel="su" and parent::node[node[@pt="ww" and @wvorm="pv"]]]"""

zijsgnodestringtemplate = """
        <node begin="{begin}" case="nom" def="def" end="{end}" frame="pronoun(nwh,thi,both,de,nom,def)" gen="de"
        genus="fem" getal="ev"  lcat="np" lemma="zij" naamval="nomin" num="both" pdtype="pron"
        per="thi" persoon="3v" pos="pron" postag="VNW(pers,pron,nomin,vol,3v,ev,fem)" pt="vnw"
        rel="{rel}" rnum="sg" root="zij" sense="zij" status="vol" vwtype="pers" wh="nwh" word="zij"/>
"""

zesgnodestringtemplate = """
        <node begin="{begin}" case="both" def="def" end="{end}" frame="pronoun(nwh,thi,both,de,both,def,wkpro)" gen="de"
        genus="fem" getal="ev"  lcat="np" lemma="ze" naamval="stan" num="both" pdtype="pron" per="thi" persoon="3"
        pos="pron" postag="VNW(pers,pron,stan,red,3,ev,fem)" pt="vnw" rel="{rel}" rnum="sg" root="ze"
        sense="ze" special="wkpro" status="red" vwtype="pers" wh="nwh" word="ze"/>
"""

zeplnodestringtemplate = """

      <node begin="{begin}" case="both" def="def" end="{end}" frame="pronoun(nwh,thi,both,de,both,def,wkpro)" gen="de"
      getal="mv"  lcat="--" lemma="ze" naamval="stan" num="both" pdtype="pron" per="thi" persoon="3" pos="pron"
      postag="VNW(pers,pron,stan,red,3,mv)" pt="vnw" rel="{rel}" root="ze" sense="ze"
      special="wkpro" status="red" vwtype="pers" wh="nwh" word="ze"/>

"""


jenodestringtemplate = """<node begin="{begin}" case="both" def="def" end="{end}"
frame="pronoun(nwh,je,sg,de,both,def,wkpro)" gen="de" getal="ev"  lcat="np" lemma="je" naamval="nomin"
num="sg" pdtype="pron" per="je" persoon="2v" pos="pron" postag="VNW(pers,pron,nomin,red,2v,ev)"
pt="vnw" rel="{rel}" rnum="sg" root="je" sense="je" special="wkpro" status="red" vwtype="pers" wh="nwh" word="je"/>
"""

hetnodestringtemplate = """<node begin="{begin}" end="{end}" frame="determiner(het,nwh,nmod,pro,nparg,wkpro)"
genus="onz" getal="ev"  infl="het" lcat="np" lemma="het" naamval="stan" pdtype="pron" persoon="3"
pos="det" postag="VNW(pers,pron,stan,red,3,ev,onz)" pt="vnw" rel="{rel}" rnum="sg" root="het"
sense="het" status="red" vwtype="pers" wh="nwh" word="het"/>
"""

tnodestringtemplate = """<node begin="{begin}" end="{end}" frame="determiner(het,nwh,nmod,pro,nparg,wkpro)"
genus="onz" getal="ev"  infl="het" lcat="np" lemma="het" naamval="stan" pdtype="pron" persoon="3" pos="det"
postag="VNW(pers,pron,stan,red,3,ev,onz)" pt="vnw" rel="{rel}" rnum="sg" root="het" sense="het"
status="red" vwtype="pers" wh="nwh" word="'t"/>
"""

usgnodestringtemplate = """
        <node begin="{begin}" case="both" def="def" end="{end}" frame="pronoun(nwh,u,sg,de,both,def)"
        gen="de" getal="ev"  lcat="np" lemma="u" naamval="nomin" num="sg" pdtype="pron" per="u" persoon="2b"
        pos="pron" postag="VNW(pers,pron,nomin,vol,2b,ev)" pt="vnw" rel="{rel}" rnum="sg" root="u" sense="u"
        status="vol" vwtype="pers" wh="nwh" word="u"/>
"""

jullienodestringtemplate = """
        <node begin="{begin}" case="both" def="def" end="{end}" frame="pronoun(nwh,je,pl,de,both,def)" gen="de"
        getal="mv"  lcat="np" lemma="jullie" naamval="stan" num="pl" pdtype="pron" per="je" persoon="2v" pos="pron"
        postag="VNW(pers,pron,stan,nadr,2v,mv)" pt="vnw" rel="{rel}" rnum="pl" root="jullie" sense="jullie"
        status="nadr" vwtype="pers" wh="nwh" word="jullie"/>
"""

wetenwistnodetemplate = """
        <node begin="{begin}" end="{end}" frame="verb(hebben,past(sg),transitive)"  infl="sg" lcat="smain"
        lemma="weten" pos="verb" postag="WW(pv,verl,ev)" pt="ww" pvagr="ev" pvtijd="verl" rel="{rel}"
        root="weet" sc="transitive" sense="weet"  tense="past" word="wist" wvorm="pv"/>

"""

wetenwistennodetemplate = """
        <node begin="{begin}" end="{end}" frame="verb(hebben,past(pl),transitive)"  infl="pl" lcat="smain"
        lemma="weten" pos="verb" postag="WW(pv,verl,mv)" pt="ww" pvagr="mv" pvtijd="verl" rel="{rel}"
        root="weet" sc="transitive" sense="weet"  tense="past" word="wisten" wvorm="pv"/>

"""

zijnwasnodetemplate = """
        <node begin="{begin}" end="{end}" frame="verb(unacc,past(sg),copula)"  infl="sg" lcat="smain" lemma="zijn"
        pos="verb" postag="WW(pv,verl,ev)" pt="ww" pvagr="ev" pvtijd="verl" rel="{rel}" root="ben" sc="copula"
        sense="ben"  tense="past" word="was" wvorm="pv"/>

"""

zijnwarennodetemplate = """
        <node begin="{begin}" end="{end}" frame="verb(unacc,past(pl),copula)" infl="pl" lcat="smain" lemma="zijn"
        pos="verb" postag="WW(pv,verl,mv)" pt="ww" pvagr="mv" pvtijd="verl" rel="{rel}" root="ben" sc="copula"
        sense="ben"  tense="past" word="waren" wvorm="pv"/>

"""

pvnodestringtemplate = """
<node begin="{begin}" end="{end}"  lemma="{lemma}" pos="verb" postag="{postag}" pt="ww" pvagr="{pvagr}"
 pvtijd="{pvtijd}"  word="{word}" wvorm="{wvorm}"/>
"""

precedingjequerytemplate = ".//node[@word='je' and @end='{nounbegin}']"


def findfirst(nodelist, att, values):
    '''

    :param nodelist: list of nodes
    :param att: attribute
    :param values: valueset
    :return: the leftmost node for which the value of the attribute att is contained in valueset
    '''
    result = None
    for node in nodelist:
        nodeatt = getattval(node, att)
        if nodeatt in values:
            result = node
            break
    return result


def getnode(nodetemplate, sourcenode):
    sourcenodebegin = getattval(sourcenode, 'begin')
    sourcenodeend = getattval(sourcenode, 'end')
    sourcenoderel = getattval(sourcenode, 'rel')
    nodestring = nodetemplate.format(begin=sourcenodebegin, end=sourcenodeend, rel=sourcenoderel)
    result = etree.fromstring(nodestring)
    return result


def replaceverb(vnode):
    '''
    replaces nodes for less frequent verb forms by their more frequent counterparts
    :param vnode: node for a verb
    :return: a node for a verb
    '''
    vnodeword = getattval(vnode, 'word').lower()
    vnodelemma = getattval(vnode, 'lemma')
    if vnodeword == 'wist' and vnodelemma == 'wissen':
        result = getnode(wetenwistnodetemplate, vnode)
    elif vnodeword == 'wisten' and vnodelemma == 'wissen':
        result = getnode(wetenwistennodetemplate, vnode)
    elif vnodeword == 'was' and vnodelemma == 'wassen':
        result = getnode(zijnwasnodetemplate, vnode)
    elif vnodeword == 'waren' and vnodelemma == 'waren':
        result = getnode(zijnwarennodetemplate, vnode)
    else:
        result = vnode
    return result


def ptsubjcheck(child):
    results = []
    childpt = getattval(child, 'pt')
    childspecial = getattval(child, 'special')
    childword = getattval(child, 'word').lower()
    childlemma = getattval(child, 'lemma')
    childrel = getattval(child, 'rel')
    childbegin = getattval(child, 'begin')
    childend = getattval(child, 'end')

    if childlemma == 'het' and childrel in ['--']:
        results.append(child)
    elif childword == 'zij' and childpt == 'ww':
        zijsgnodestring = zijsgnodestringtemplate.format(begin=childbegin, end=childend, rel=childrel)
        zijsgnode = etree.fromstring(zijsgnodestring)
        results.append(zijsgnode)
    elif childpt in nominalpts and childspecial != "er_loc":
        results.append(child)
    elif childpt in nominalisablepts and getattval(child, 'positie') == 'nom':
        results.append(child)
    return results


def getpotsubjs(tree):
    results = []
    for child in tree:
        if 'pt' in child.attrib:
            childpt = getattval(child, 'pt')
            childcase = getattval(child, 'naamval')
            childvwtype = getattval(child, 'vwtype')
            childword = getattval(child, 'word').lower()
            if childword == 'zij':
                zijnode = getnode(zijsgnodestringtemplate, child)
                results.append(zijnode)
            # elif childword == 'ze':  # uitgezte want het levert fouten op
            #    zenode = getnode(zesgnodestringtemplate, child)
            #    results.append(zenode)
            elif childpt == 'vnw' and childvwtype == 'pers' and childcase == 'obl' and childword not in ['je']:
                pass  # exclude pronouns such as me, hem, mij, etc as subjects
            else:
                results += ptsubjcheck(child)
        elif 'cat' in child.attrib:
            childcat = getattval(child, 'cat')
            childrel = getattval(child, 'rel')
            if childcat == 'np':
                childhead = getheadof(child)
                if 'pt' in childhead.attrib:
                    childheadpt = getattval(childhead, 'pt')
                    childheadword = getattval(childhead, 'word')
                    if childheadpt == 'ww' or (childheadpt == 'n' and childheadword == 'waren'):
                        childdet = getdetof(child)
                        childdetbegin = getattval(child, 'begin')
                        childdetend = getattval(child, 'end')
                        childdetword = getattval(childdet, 'word').lower()
                        if childdetword == 'je':
                            jenode = getnode(jenodestringtemplate, childdet)
                            results.append(jenode)
                        elif childdetword == 'het':
                            hetnode = getnode(hetnodestringtemplate, childdet)
                            results.append(hetnode)
                        elif childdetword == "'t":
                            tnode = getnode(tnodestringtemplate, childdet)
                            results.append(tnode)
                    else:
                        childresults = ptsubjcheck(childhead)
                        results += childresults
                else:
                    childresults = getpotsubjs(child)  # here something should be done for coordinations
                    results += childresults
                # results.append(child)
            elif childcat in ['pp', 'inf', 'ppart'] and childrel not in ['dp', '--']:
                pass
            else:
                childresults = getpotsubjs(child)
                results += childresults
    return results


def getpvs(tokensmd, tree, uttid):
    pvs = tree.xpath(".//node[@pt='ww' and @wvorm='pv' and @word!='zij' and @word !='kijk']")  # we exclude the conjunctive 'zij'
    # if we do not find a finite verb we analyse an infinitive as if it is a finite verb
    if pvs == []:
        pvs = tree.xpath(".//node[@pt='ww' and @wvorm='inf']")
        if pvs != []:
            thepv = pvs[0]
            rb = rbrother(thepv, tree)
            lb = lbrother(thepv, tree)
            lblemma = getattval(lb, 'lemma')
            lbrel = getattval(lb, 'rel')
            if nominal(rb) or getattval(rb, 'pt') == 'lid' or (lblemma in ['je', 'het'] and lbrel == 'det'):
                pass
            else:
                pvs = []
# originally: but I do not understand it
#            if nominal(rb):
#                pvs = []
#            if not(lblemma in ['je', 'het'] and lbrel == 'det'):
#                pvs = []
        if debug and pvs != []:
            print('pv instead of infinitive')
            simpleshow(tree)

    # if we still did not find anything, try nouns that are also a verb form but restrict to cases
    # with possessive je present, or with verb zij present
    if pvs == []:
        nouns = tree.xpath(".//node[@pt='n' or @pt='adj']")
        zijverbs = tree.xpath(".//node[@pt='ww' and @word='zij']")
        for noun in nouns:
            nounword = getattval(noun, 'word')
            nounpt = getattval(noun, 'pt')
            nounstr = nounword.lower()
            nounbegin = getattval(noun, 'begin')
            nounend = getattval(noun, 'end')
            zijverbfound = zijverbs != []
            precedingjequery = precedingjequerytemplate.format(nounbegin=nounbegin)
            precedingjes = tree.xpath(precedingjequery)
            precedingjefound = precedingjes != []
            wistfound = nounstr == 'wist'
            if not(zijverbfound or precedingjefound or wistfound):
                continue
            if informlexiconpos(nounstr, 'ww'):
                cands = getwordposinfo(nounstr, 'ww')
                if cands == []:
                    pvs = []
                else:
                    if debug:
                        print('pv instead of noun or adj')
                        simpleshow(tree)
                    first = cands[0]
                    (pos, dehet, infl, lemma) = first
                    dcoi_infl = pvinfl2dcoi(nounstr, infl, lemma)
                    (wvorm, pvtijd, pvagr) = dcoi_infl
                    postag = 'WW({wvorm}, {pvtijd}, {pvagr})'.format(wvorm='pv', pvtijd=pvtijd, pvagr=pvagr)
                    pvnodestring = pvnodestringtemplate.format(lemma=lemma, word=nounstr, postag=postag, wvorm=wvorm,
                                                               pvagr=pvagr, pvtijd=pvtijd, begin=nounbegin, end=nounend)
                    pvnode = etree.fromstring(pvnodestring)
                    pvs.append(pvnode)
    return pvs


def zijnimperativeok(vnode):
    vnodelemma = getattval(vnode, 'lemma')
    vnodeword = getattval(vnode, 'word').lower()
    vnodestype = getattval(vnode, 'stype')
    if vnodestype != 'imparative':
        result = True
    elif vnodelemma != 'zijn':
        result = True
    elif vnodeword in ['wees', 'weest']:
        result = True
    else:
        result = False
    return result


def getsvacorrectedutt(snode, thepv, tokens, metadata):
    newtokens = []
    pvbegin = getattval(thepv, 'begin')
    inversion = inverted(snode, thepv)
    newpv = getpvform(snode, thepv, inversion)
    if newpv is None:
        results = []
    else:
        newpos = int(pvbegin)
        newtoken = Token(newpv, newpos)
        for token in tokens:
            if token.pos != newpos:
                newtokens.append(token)
            else:
                oldtoken = token
                newtokens.append(newtoken)
                meta = mkSASTAMeta(oldtoken, newtoken, name='GrammarError', value='SVAerror', cat='Error',
                                   backplacement=bpl_node)
                metadata.append(meta)

        results = [TokenListMD(newtokens, metadata)]
    return results


def getsvacorrections(tokensmd, rawtree, uttid):
    tree = indextransform(rawtree)
    tokens = tokensmd.tokens
    metadata = tokensmd.metadata
    ltokens = len(tokens)
    newtokens = []

    pvs = getpvs(tokensmd, tree, uttid)
    abnormalobj2matches = tree.xpath(abnormalobj2sentencexpath)
    if len(pvs) != 1:
        results = []
    elif (tree.xpath(normalsentencexpath) != [] and abnormalobj2matches == []) or \
            tree.xpath(normalwhqsentencexpath) != []:
        thesubjs = tree.xpath(subjxpath)
        if thesubjs != []:
            thesubj = thesubjs[0]
        else:
            thesubj = None
        prednode = getcopulapredicate(tree)
        if prednode is not None:
            thesubj = prednode
        thepv = pvs[0]
        if thesubj is not None:
            if phicompatible(thesubj, thepv):
                results = []
            else:
                results = getsvacorrectedutt(thesubj, thepv, tokens, metadata)
        else:
            results = []  # hier rekening houden met imperatieven!
    else:
        potsubjs = []
        rawpv = pvs[0]
        thepv = replaceverb(rawpv)
        pvstype = getattval(thepv, 'stype')
        if abnormalobj2matches != []:
            potsubjs = tree.xpath(abnormalobj2xpath)
        if potsubjs == []:
            potsubjs = getpotsubjs(tree)
        if potsubjs == []:
            results = []
        else:
            nominativenode = findfirst(potsubjs, 'naamval', {'nomin'})
            if nominativenode is not None:
                thesubj = nominativenode
            # next left out because dealt with in a different way
            #   elif pvstype == 'imparative' and zijnimperativeok(thepv) and not modalinv(thepv):
            #       sunode = findfirst(potsubjs, 'rel', {'su'})
            #      if sunode is not None:
            #          thesubj = sunode
            #      else:
            #          sunode = findfirst(potsubjs, 'lemma', {'je', 'jij', 'jullie', 'u'})
            #          if sunode is not None:
            #              thesubj = sunode
            #          else:
            #              thepvend = getattval(thepv, 'end')
            #              jenodestring = jenodestringtemplate.format(begin=thepvend, end=thepvend, rel='su' )
            #              jenode = etree.fromstring(jenodestring)
            #              thesubj = jenode
            else:
                sortedpotsubjs = sorted(potsubjs, key=lambda x: getattval(x, 'end'))
                thesubj = sortedpotsubjs[0]
            thesubjlemma = getattval(thesubj, 'lemma')
            if thesubjlemma == 'u':
                usgnode = getnode(usgnodestringtemplate, thesubj)
                thesubj = usgnode
            thesubjpersoon = getattval(thesubj, 'persoon')
            if thesubjpersoon == 'persoon':
                thesubj = copymodifynode(thesubj, {'persoon': '3'})
            if phicompatible(thesubj, thepv):
                results = []
            else:
                results = getsvacorrectedutt(thesubj, thepv, tokens, metadata)

    return results


def getpersons(vnode):
    pvagr = getattval(vnode, 'pvagr')
    vword = getattval(vnode, 'word')
    vtense = getattval(vnode, 'pvtijd')
    if vtense == 'tgw':
        if vword in {'ben', 'heb'}:
            result = {'1', '2i'}
        elif vword in {'bent', 'hebt'}:
            result = {'2', 'u'}
        elif vword in {'is', 'heeft'}:
            result = {'3', 'u'}
        elif vword in {'kun', 'zul'}:
            result = {'2i'}
        elif vword in {'kunt', 'zult', 'wilt'}:
            result = {'2', 'u'}
        elif vword in {'mag', 'kan', 'wil', 'zal'}:
            result = {'1', '2', '2i', '3', 'u'}
        elif pvagr == 'ev':
            if vword.endswith('t'):
                result = {'1', '2', '2i', '3', 'u'}
            else:
                result = {'1', '2i'}
        elif pvagr == 'met-t':
            result = {'2', '3', 'u'}
        elif pvagr == 'mv':
            result = {'mv'}
    elif vtense == 'verl':
        if pvagr == 'ev':
            result = {'1', '2', '2i', '3', 'u'}
        elif pvagr == 'mv':
            result = {'mv'}
        else:
            result = {}
    elif vtense == '':  # for infinitives
        result = {'mv'}
    elif vtense == 'conj':
        result = {'3'}
    else:
        SDLOGGER.error('Unknown pvtijd value: {}'.format(vtense))
        result = {}
    return result


def phicompatible(snode, vnode):
    if snode is None or vnode is None:
        return False
    subjnode = snode
    subjnodelemma = getlemma(subjnode)
    inversion = inverted(subjnode, vnode)
    if subjnodelemma in ['het', 'u', 'je']:
        subjgetal = 'ev'
    else:
        subjgetal = getattval(subjnode, 'getal')
    vnodepvagr = getattval(vnode, 'pvagr')
    if subjgetal == 'mv':
        result = vnodepvagr == 'mv'
    elif subjgetal == 'getal':
        # check if the person corresponds with verbperson
        vnodepersons = getpersons(vnode)
        subjperson1 = getattval(subjnode, 'persoon')
        if subjperson1 == 'persoon':
            subjperson1 = '3'
        subjperson2 = subjperson1 if subjperson1 != '' else '3'
        subjperson = subjperson2[0]   # just the first character to deal with 2b 2v 3v 3p 30 etc
        if vnodepersons == {'mv'}:
            result = True
        elif subjperson in vnodepersons and not inversion:
            result = True
        else:
            result = False
    elif subjgetal == '':
        result = True
    elif subjgetal == 'ev':
        vnodepersons = getpersons(vnode)
        subjperson1 = getattval(subjnode, 'persoon')
        subjperson2 = subjperson1 if subjperson1 != '' else '3'
        subjperson = subjperson2[0]   # just the first character to deal with 2b 2v 3v 3p 30 etc
        if vnodepersons == {'mv'}:
            result = False
        elif subjperson in vnodepersons and not inversion:
            result = True
        elif '2i' in vnodepersons:
            subjbegin = getattval(subjnode, 'begin')
            vnodeend = getattval(vnode, 'end')
            result = subjperson == '2' and '2i' in vnodepersons and subjbegin == vnodeend and \
                subjnodelemma in ['jij', 'je']
        elif 'u' in vnodepersons:
            subjnodelemma = getattval(subjnode, 'lemma')
            result = subjnodelemma == 'u'
        else:
            if subjperson not in ['1', '2', '3']:
                subjnodelemma = getattval(subjnode, 'lemma')
                SDLOGGER.error('Unexpected value ({}) for the attribute persoon of {}'.format(subjperson, subjnodelemma))
            result = False
    else:
        subjnodelemma = getattval(subjnode, 'lemma')
        SDLOGGER.error('Unexpected value ({}) for the attribute getal of {}'.format(subjgetal, subjnodelemma))
        result = False
    return result


def getpvform(thesubj, thepv, inversion):
    '''
    find in lexicon (CELEX)the verb wordform compatible with thesubj
    :param thesubj: subject (head) node
    :param thepv: finite verb
    :param inversion: True or False
    :return:
    '''

    results = getinflforms(thesubj, thepv, inversion)
    if results != []:
        result = results[0]
    else:
        result = None
    return result


predicatesubjxpath = """//node[@rel="predc" and
       parent::node[node[@rel="su" and (@lemma="het" or @lemma="dit" or @lemma="dat")] and
                    node[@rel="hd" and @pt="ww" and @wvorm="pv"]
                   ]
    ]"""


def getcopulapredicate(tree):
    preds = tree.xpath(predicatesubjxpath)
    if preds == []:
        result = None
    else:
        result = preds[0]
    return result
