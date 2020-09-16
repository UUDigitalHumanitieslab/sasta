'''
various treebank functions

'''

import sys
import logging

logger = logging.getLogger('sasta')
from lxml import etree

class Metadata:
    '''
    contains 3 elements, each a string type, name, value
    '''
    def __init__(thetype, thename, thevalue):
        self.type = thetype
        self.name = thename
        self.value = thevalue
    def md2PEP(self):
        result = '##META {} {} = {}'.format(self.type, self.name, self.value)
        return result
    def md2XMLElement(self):
        result = etree.Element('meta', type=self.type, name=self.name, value=self.value)
        return result


space = ' '

allrels = ['hdf', 'hd', 'cmp', 'sup', 'su', 'obj1', 'pobj1', 'obj2', 'se', 'pc', 'vc', 'svp', 'predc', 'ld', 'me', 'predm', 'obcomp', 'mod', 'body', 'det', 'app', 'whd', 'rhd', 'cnj', 'crd', 'nucl', 'sat', 'tag', 'dp', 'top', 'mwp', 'dlink', '--']

allcats =  ['smain', 'np', 'ppart', 'pp', 'ssub', 'inf', 'cp', 'du', 'ap', 'advp', 'ti', 'rel', 'whrel', 'whsub', 'conj', 'whq', 'oti', 'ahi', 'detp', 'sv1', 'svan', 'mwu', 'top']

clausecats = ['smain',  'ssub', 'inf', 'cp',  'ti', 'rel', 'whrel', 'whsub',  'whq', 'oti', 'ahi',  'sv1', 'svan']

trueclausecats = ['smain',  'cp',   'rel', 'whrel', 'whsub',  'whq',    'sv1', 'svan']

complrels = ['su', 'obj1', 'pobj1', 'obj2', 'se', 'pc', 'vc', 'svp', 'predc', 'ld']

mainclausecats = ['smain', 'whq', 'sv1']


#uttidquery = ".//meta[@name='uttid']/@value"
sentidquery = ".//sentence[@name='sentid']/@value"
#altquery = ".//meta[@name='alt']/@value"
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
        elif thelemma is None or thelemma =='':
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
        sv1ok =  parentnodecat not in ['whq', 'cp', 'rel', 'whrel', 'whsub']
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
            ##issue a warning
        elif len(results) == 1:
            result1 = results[0]
            result = number2intstring(result1)
    return result


def getnodeyield(syntree):
    resultlist= []
    for node in syntree.iter():
        if 'pt' in node.attrib or 'pos' in node.attrib:
            resultlist.append(node)
    sortedresultlist = sorted(resultlist, key=lambda x: int(getattval(x, 'end')))
    return sortedresultlist

def getyield(syntree):  #deze herformuleren in termen van getnodeyield na testen
    resultlist = []
    if syntree is None:
        theyield = []
    else:
        for node in syntree.iter():
            if 'pt' in node.attrib or 'pos' in node.attrib:
                if 'word' in node.attrib and 'end'in node.attrib:
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
    return theleftsibling


def getmarkedutt(m, syntree):
    thewordlist = getyield(syntree)
    thepositions = getwordpositions(m, syntree)
    themarkedyield = getmarkedyield(thewordlist, thepositions)
    yieldstr = space.join(themarkedyield)
    return yieldstr

def mark(str):
    result = '*'+ str + '*'
    return result

def getwordpositions(matchtree, syntree):
    #nothing special needs to be done for index nodes since they also have begin and end
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

streestrings = {}
streestrings[1] = '''
<alpino_ds version="1.6">
  <parser cats="1" skips="5" />
  <node begin="0" cat="top" end="8" id="0" rel="top">
    <node begin="0" conjtype="neven" end="1" frame="complementizer(root)" his="robust_skip" id="1" lcat="--" lemma="en" pos="comp" postag="VG(neven)" pt="vg" rel="--" root="en" sc="root" sense="en" word="en"/>
    <node begin="1" end="2" frame="--" genus="zijd" getal="ev" graad="basis" his="robust_skip" id="2" lcat="--" lemma="uhm" naamval="stan" ntype="soort" pos="--" postag="N(soort,ev,basis,zijd,stan)" pt="n" rel="--" root="uhm" sense="uhm" word="uhm"/>
    <node begin="2" conjtype="neven" end="3" frame="conj(en)" his="robust_skip" id="3" lcat="--" lemma="en" pos="vg" postag="VG(neven)" pt="vg" rel="--" root="en" sense="en" word="en"/>
    <node begin="3" end="4" frame="--" genus="zijd" getal="ev" graad="basis" his="robust_skip" id="4" lcat="--" lemma="uhm" naamval="stan" ntype="soort" pos="--" postag="N(soort,ev,basis,zijd,stan)" pt="n" rel="--" root="uhm" sense="uhm" word="uhm"/>
    <node begin="4" case="nom" def="def" end="5" frame="pronoun(nwh,thi,sg,de,nom,def)" gen="de" genus="masc" getal="ev" his="robust_skip" id="5" lcat="--" lemma="hij" naamval="nomin" num="sg" pdtype="pron" per="thi" persoon="3" pos="pron" postag="VNW(pers,pron,nomin,vol,3,ev,masc)" pt="vnw" rel="--" root="hij" sense="hij" status="vol" vwtype="pers" wh="nwh" word="hij"/>
    <node begin="5" cat="smain" end="8" id="6" rel="--">
      <node begin="5" case="nom" def="def" end="6" frame="pronoun(nwh,thi,sg,de,nom,def)" gen="de" genus="masc" getal="ev" his="normal" his_1="normal" id="7" lcat="np" lemma="hij" naamval="nomin" num="sg" pdtype="pron" per="thi" persoon="3" pos="pron" postag="VNW(pers,pron,nomin,vol,3,ev,masc)" pt="vnw" rel="su" rnum="sg" root="hij" sense="hij" status="vol" vwtype="pers" wh="nwh" word="hij"/>
      <node begin="6" end="7" frame="verb(unacc,sg_heeft,intransitive)" his="normal" his_1="normal" id="8" infl="sg_heeft" lcat="smain" lemma="zijn" pos="verb" postag="WW(pv,tgw,ev)" pt="ww" pvagr="ev" pvtijd="tgw" rel="hd" root="ben" sc="intransitive" sense="ben" stype="declarative" tense="present" word="is" wvorm="pv"/>
      <node begin="7" end="8" frame="adverb" his="normal" his_1="normal" id="9" lcat="advp" lemma="nogal" pos="adv" postag="BW()" pt="bw" rel="mod" root="nogal" sense="nogal" word="nogal"/>
    </node>
  </node>
  <sentence sentid="32">en uhm en uhm hij hij is nogal</sentence>
<metadata>
<meta type="text" name="charencoding" value="UTF8" />
<meta type="text" name="childage" value="" />
<meta type="text" name="childmonths" value="" />
<meta type="text" name="comment" value="##META text samplenaam = ASTA-06" />
<meta type="text" name="session" value="ASTA_sample_06" />
<meta type="text" name="origutt" value="en uhm en uhm hij hij is nogal " />
<meta type="text" name="parsefile" value="Unknown_corpus_ASTA_sample_06_u00000000046.xml" />
<meta type="text" name="speaker" value="PMA" />
<meta type="int" name="uttendlineno" value="85" />
<meta type="int" name="uttid" value="32" />
<meta type="int" name="uttstartlineno" value="85" />
<meta type="text" name="name" value="pma" />
<meta type="text" name="SES" value="" />
<meta type="text" name="age" value="" />
<meta type="text" name="custom" value="" />
<meta type="text" name="education" value="" />
<meta type="text" name="group" value="" />
<meta type="text" name="language" value="nld" />
<meta type="text" name="months" value="" />
<meta type="text" name="role" value="Other" />
<meta type="text" name="sex" value="" />
<meta type="text" name="xsid" value="32" />
<meta type="int" name="uttno" value="46" />
</metadata>
</alpino_ds>
'''

streestrings[2] = '''
<alpino_ds version="1.6">
  <parser cats="3" skips="0" />
  <node begin="0" cat="top" end="17" id="0" rel="top">
    <node begin="0" cat="du" end="16" id="1" rel="--">
      <node begin="0" cat="smain" end="3" id="2" rel="dp">
        <node begin="0" case="nom" def="def" end="1" frame="pronoun(nwh,fir,sg,de,nom,def)" gen="de" getal="ev" his="normal" his_1="normal" id="3" lcat="np" lemma="ik" naamval="nomin" num="sg" pdtype="pron" per="fir" persoon="1" pos="pron" postag="VNW(pers,pron,nomin,vol,1,ev)" pt="vnw" rel="su" rnum="sg" root="ik" sense="ik" status="vol" vwtype="pers" wh="nwh" word="ik"/>
        <node begin="1" end="2" frame="verb(hebben,sg1,transitive_ndev)" his="normal" his_1="normal" id="4" infl="sg1" lcat="smain" lemma="hebben" pos="verb" postag="WW(pv,tgw,ev)" pt="ww" pvagr="ev" pvtijd="tgw" rel="hd" root="heb" sc="transitive_ndev" sense="heb" stype="declarative" tense="present" word="heb" wvorm="pv"/>
        <node begin="2" case="both" def="indef" end="3" frame="pronoun(nwh,thi,sg,both,both,indef,strpro)" gen="both" his="normal" his_1="normal" id="5" lcat="np" lemma="één" num="sg" numtype="hoofd" per="thi" pos="pron" positie="vrij" postag="TW(hoofd,vrij)" pt="tw" rel="obj1" rnum="sg" root="één" sense="één" special="strpro" wh="nwh" word="een"/>
      </node>
      <node begin="3" cat="smain" end="6" id="6" rel="dp">
        <node begin="3" case="nom" def="def" end="4" frame="pronoun(nwh,fir,sg,de,nom,def)" gen="de" getal="ev" his="normal" his_1="normal" id="7" lcat="np" lemma="ik" naamval="nomin" num="sg" pdtype="pron" per="fir" persoon="1" pos="pron" postag="VNW(pers,pron,nomin,vol,1,ev)" pt="vnw" rel="su" rnum="sg" root="ik" sense="ik" status="vol" vwtype="pers" wh="nwh" word="ik"/>
        <node begin="4" end="5" frame="verb(hebben,sg1,transitive_ndev)" his="normal" his_1="normal" id="8" infl="sg1" lcat="smain" lemma="hebben" pos="verb" postag="WW(pv,tgw,ev)" pt="ww" pvagr="ev" pvtijd="tgw" rel="hd" root="heb" sc="transitive_ndev" sense="heb" stype="declarative" tense="present" word="heb" wvorm="pv"/>
        <node begin="5" case="both" def="indef" end="6" frame="pronoun(nwh,thi,sg,both,both,indef,strpro)" gen="both" his="normal" his_1="normal" id="9" lcat="np" lemma="één" num="sg" numtype="hoofd" per="thi" pos="pron" positie="vrij" postag="TW(hoofd,vrij)" pt="tw" rel="obj1" rnum="sg" root="één" sense="één" special="strpro" wh="nwh" word="een"/>
      </node>
      <node begin="6" cat="smain" end="16" id="10" rel="dp">
        <node begin="6" case="nom" def="def" end="7" frame="pronoun(nwh,fir,sg,de,nom,def)" gen="de" getal="ev" his="normal" his_1="normal" id="11" lcat="np" lemma="ik" naamval="nomin" num="sg" pdtype="pron" per="fir" persoon="1" pos="pron" postag="VNW(pers,pron,nomin,vol,1,ev)" pt="vnw" rel="su" rnum="sg" root="ik" sense="ik" status="vol" vwtype="pers" wh="nwh" word="ik"/>
        <node begin="7" end="8" frame="verb(hebben,sg1,transitive_ndev)" his="normal" his_1="normal" id="12" infl="sg1" lcat="smain" lemma="hebben" pos="verb" postag="WW(pv,tgw,ev)" pt="ww" pvagr="ev" pvtijd="tgw" rel="hd" root="heb" sc="transitive_ndev" sense="heb" stype="declarative" tense="present" word="heb" wvorm="pv"/>
        <node begin="8" cat="np" end="16" id="13" rel="obj1">
          <node begin="8" end="9" frame="determiner(een)" his="normal" his_1="normal" id="14" infl="een" lcat="detp" lemma="een" lwtype="onbep" naamval="stan" npagr="agr" pos="det" postag="LID(onbep,stan,agr)" pt="lid" rel="det" root="een" sense="een" word="een"/>
          <node begin="9" end="10" frame="noun(de,count,bare_meas)" gen="de" genus="zijd" getal="ev" graad="basis" his="normal" his_1="normal" id="15" lcat="np" lemma="man" naamval="stan" ntype="soort" num="bare_meas" pos="noun" postag="N(soort,ev,basis,zijd,stan)" pt="n" rel="hd" rnum="sg" root="man" sense="man" word="man"/>
          <node begin="10" cat="rel" end="16" id="16" rel="mod">
            <node begin="10" cat="pp" end="12" id="17" index="1" rel="rhd">
              <node begin="10" end="11" frame="preposition(met,[mee,[en,al]])" his="normal" his_1="normal" id="18" lcat="pp" lemma="met" pos="prep" postag="VZ(init)" pt="vz" rel="hd" root="met" sense="met" vztype="init" word="met"/>
              <node begin="11" case="obl" end="12" frame="rel_pronoun(both,obl)" gen="both" getal="getal" his="normal" his_1="normal" id="19" lcat="np" lemma="wie" naamval="stan" pdtype="pron" persoon="3p" pos="pron" postag="VNW(vb,pron,stan,vol,3p,getal)" pt="vnw" rel="obj1" rnum="sg" root="wie" sense="wie" status="vol" vwtype="vb" wh="rel" word="wie"/>
            </node>
            <node begin="10" cat="ssub" end="16" id="20" rel="body">
              <node begin="12" case="nom" def="def" end="13" frame="pronoun(nwh,fir,sg,de,nom,def)" gen="de" getal="ev" his="normal" his_1="normal" id="21" index="2" lcat="np" lemma="ik" naamval="nomin" num="sg" pdtype="pron" per="fir" persoon="1" pos="pron" postag="VNW(pers,pron,nomin,vol,1,ev)" pt="vnw" rel="su" rnum="sg" root="ik" sense="ik" status="vol" vwtype="pers" wh="nwh" word="ik"/>
              <node begin="13" end="14" frame="verb(hebben,modal_not_u,modifier(aux(inf)))" his="normal" his_1="normal" id="22" infl="modal_not_u" lcat="ssub" lemma="willen" pos="verb" postag="WW(pv,tgw,ev)" pt="ww" pvagr="ev" pvtijd="tgw" rel="hd" root="wil" sc="modifier(aux(inf))" sense="wil" tense="present" word="wil" wvorm="pv"/>
              <node begin="10" cat="inf" end="16" id="23" rel="vc">
                <node begin="12" end="13" id="24" index="2" rel="su"/>
                <node begin="14" buiging="zonder" end="15" frame="verb(zijn,inf(no_e),aux(inf))" his="normal" his_1="normal" id="25" infl="inf(no_e)" lcat="inf" lemma="gaan" pos="verb" positie="vrij" postag="WW(inf,vrij,zonder)" pt="ww" rel="hd" root="ga" sc="aux(inf)" sense="ga" word="gaan" wvorm="inf"/>
                <node begin="10" cat="inf" end="16" id="26" rel="vc">
                  <node begin="10" end="12" id="27" index="1" rel="pc"/>
                  <node begin="12" end="13" id="28" index="2" rel="su"/>
                  <node begin="15" buiging="zonder" end="16" frame="verb(zijn,inf,pc_pp(met))" his="normal" his_1="normal" id="29" infl="inf" lcat="inf" lemma="trouwen" pos="verb" positie="vrij" postag="WW(inf,vrij,zonder)" pt="ww" rel="hd" root="trouw" sc="pc_pp(met)" sense="trouw-met" word="trouwen" wvorm="inf"/>
                </node>
              </node>
            </node>
          </node>
        </node>
      </node>
    </node>
    <node begin="16" end="17" frame="--" genus="zijd" getal="ev" graad="basis" his="skip" id="30" lcat="--" lemma="uhm" naamval="stan" ntype="soort" pos="--" postag="N(soort,ev,basis,zijd,stan)" pt="n" rel="--" root="uhm" sense="uhm" word="uhm"/>
  </node>
  <sentence sentid="29">ik heb een ik heb een ik heb een man met wie ik wil gaan trouwen uhm</sentence>
<metadata>
<meta type="text" name="charencoding" value="UTF8" />
<meta type="text" name="childage" value="" />
<meta type="text" name="childmonths" value="" />
<meta type="text" name="comment" value="##META text samplenaam = ASTA-06" />
<meta type="text" name="session" value="ASTA_sample_06" />
<meta type="text" name="origutt" value="ik heb een ik heb een ik heb een man met wie ik wil gaan trouwen uhm " />
<meta type="text" name="parsefile" value="Unknown_corpus_ASTA_sample_06_u00000000042.xml" />
<meta type="text" name="speaker" value="PMA" />
<meta type="int" name="uttendlineno" value="78" />
<meta type="int" name="uttid" value="29" />
<meta type="int" name="uttstartlineno" value="78" />
<meta type="text" name="name" value="pma" />
<meta type="text" name="SES" value="" />
<meta type="text" name="age" value="" />
<meta type="text" name="custom" value="" />
<meta type="text" name="education" value="" />
<meta type="text" name="group" value="" />
<meta type="text" name="language" value="nld" />
<meta type="text" name="months" value="" />
<meta type="text" name="role" value="Other" />
<meta type="text" name="sex" value="" />
<meta type="text" name="xsid" value="29" />
<meta type="int" name="uttno" value="42" />
</metadata>
</alpino_ds>
'''


strees = {}
for el in streestrings:
    strees[el] = etree.fromstring(streestrings[el])

def test():
    for el in strees:
        stree = strees[el]
        lmc = lastmainclauseof(stree)
        print(getmarkedutt(lmc, stree))

if __name__ == '__main__':
    test()