from ..dedup import (remove_duplicates,
                     space, find_duplicates, cleantokenlist, mlux, samplesize, getfilledpausesposlist)
from ..treebankfunctions import getattval, getnodeyield
from ..sastatok import tokenize
from ..sastatoken import stringlist2tokenlist, tokenlist2stringlist
from lxml import etree
from ..exampletrees import stree

from optparse import OptionParser

# TODO: fix

teststrings = ['in de grote in de grote tuin', 'op de op de kleine schommel',
               'ik geloof geloof dat dat hij ziek is ziek is', 'hier moet niets weg',
               'Hij heeft een boek ge gekocht', 'in de grote in de grote in de grote tuin', 'in de grote in de grote in de grote in de grote tuin']
goldstrings = ['in de grote tuin', 'op de kleine schommel', 'ik geloof dat hij ziek is',
               'hier moet niets weg', 'Hij heeft een boek ge gekocht', 'in de grote tuin', 'in de grote tuin']


testgoldstrings = zip(teststrings, goldstrings)
testlists = [str.split() for str in teststrings]

testtokenlists = [stringlist2tokenlist(tl) for tl in testlists]
testgoldposlists = [[0, 1, 2], [0, 1], [1, 3, 6, 7], [],
                    [], [0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5, 6, 7, 8]]
testgoldlists = zip(testtokenlists, testgoldposlists)


def test(testgoldstrings):
    for (ts, gs) in testgoldstrings:
        tl = ts.split()
        cleantl = remove_duplicates(tl)
        cleanstr = space.join(cleantl)
        assert cleanstr == gs
        if cleanstr == gs:
            print('OK', ts, '::', cleanstr, '==', gs)
        else:
            print('NO', ts, '::', cleanstr, '!=', gs)


def tokentest(testgoldlists):
    for (tokenlist, goldlist) in testgoldlists:
        tobedeleted = sorted(find_duplicates(tokenlist))
        stringlist = [token.word for token in tokenlist]
        instring = space.join(stringlist)
        print('input:', instring)
        if sorted(tobedeleted) == sorted(goldlist):
            print('OK:', tobedeleted, '==', goldlist)
        else:
            print('NO:', tobedeleted, '!=', goldlist)
        print('output:', cleantokenlist(tokenlist, tobedeleted))


def hitprint(wordnodes):
    for wnode in wordnodes:
        theword = getattval(wnode, 'word')
        thepos = getattval(wnode, 'end')
        print('{}:{}'.format(thepos, theword), end=space)
    print()


def streefiletest(filename):
    fulltree = etree.parse(filename)
    stree = fulltree.getroot()
    samplesizenodes = samplesize(stree)
    print('A045, samplesize')
    hitprint(samplesizenodes)
    mluxnodes = mlux(stree)
    print('A029, MLU')
    hitprint(mluxnodes)


filledpausestestdata = [
    ('Op euh eventien zeventien okt ja  oktober is onze ja',
     'Op eventien zeventien okt ja  oktober is onze ja'),
    ('dan heeft het allemaal gebeurd', 'dan heeft het allemaal gebeurd'),
    ('en daar heeft euh  n de euh', 'en daar heeft  n de '),
    ('ik weet niet wat daar ge gebeurd is ',
     'ik weet niet wat daar ge gebeurd is '),
    ('ik heb nog euh de half euh de euh van de euh voor de euh',
     'ik heb nog de half  de van de  voor de ')
]

fpandmlutestdata = [
    ('Op euh eventien zeventien okt ja  oktober is onze ja',
     'Op  zeventien   oktober is onze '),
    ('dan heeft het allemaal gebeurd', 'dan heeft het allemaal gebeurd'),
    ('en daar heeft euh  n de euh', 'en daar heeft  de '),
    ('ik weet niet wat daar ge gebeurd is ', 'ik weet niet wat daar gebeurd is '),
    ('ik heb nog euh de half euh de euh van de euh voor de euh',
     'ik heb nog de half  de   voor de '),
]

streestrings = {}
strees = {}

streestrings[1] = """<alpino_ds version="1.6">
  <parser cats="2" skips="0" />
  <node begin="0" cat="top" end="22" id="0" rel="top">
    <node begin="0" end="1" frame="--" genus="zijd" getal="ev" graad="basis" his="skip" id="1" lcat="--" lemma="Uh" naamval="stan" ntype="eigen" pos="--" postag="N(eigen,ev,basis,zijd,stan)" pt="n" rel="--" root="Uh" sense="Uh" word="Uh"/>
    <node begin="1" end="2" frame="determiner(een)" his="skip" id="2" infl="een" lcat="--" lemma="een" lwtype="onbep" naamval="stan" npagr="agr" pos="det" postag="LID(onbep,stan,agr)" pt="lid" rel="--" root="een" sense="een" word="een"/>
    <node begin="2" end="3" frame="--" genus="zijd" getal="ev" graad="basis" his="skip" id="3" lcat="--" lemma="uh" naamval="stan" ntype="soort" pos="--" postag="N(soort,ev,basis,zijd,stan)" pt="n" rel="--" root="uh" sense="uh" word="uh"/>
    <node begin="3" end="4" frame="determiner(een)" his="skip" id="4" infl="een" lcat="--" lemma="een" lwtype="onbep" naamval="stan" npagr="agr" pos="det" postag="LID(onbep,stan,agr)" pt="lid" rel="--" root="een" sense="een" word="een"/>
    <node begin="4" end="5" frame="determiner(een)" his="skip" id="5" infl="een" lcat="--" lemma="een" lwtype="onbep" naamval="stan" npagr="agr" pos="det" postag="LID(onbep,stan,agr)" pt="lid" rel="--" root="een" sense="een" word="een"/>
    <node begin="6" end="7" frame="--" genus="zijd" getal="ev" graad="basis" his="skip" id="6" lcat="--" lemma="uh" naamval="stan" ntype="soort" pos="--" postag="N(soort,ev,basis,zijd,stan)" pt="n" rel="--" root="uh" sense="uh" word="uh"/>
    <node begin="7" end="8" frame="--" genus="zijd" getal="ev" graad="basis" his="skip" id="7" lcat="--" lemma="uh" naamval="stan" ntype="soort" pos="--" postag="N(soort,ev,basis,zijd,stan)" pt="n" rel="--" root="uh" sense="uh" word="uh"/>
    <node begin="9" end="10" frame="--" genus="zijd" getal="ev" graad="basis" his="skip" id="8" lcat="--" lemma="uh" naamval="stan" ntype="soort" pos="--" postag="N(soort,ev,basis,zijd,stan)" pt="n" rel="--" root="uh" sense="uh" word="uh"/>
    <node begin="12" end="13" frame="--" genus="zijd" getal="ev" graad="basis" his="skip" id="9" lcat="--" lemma="uh" naamval="stan" ntype="soort" pos="--" postag="N(soort,ev,basis,zijd,stan)" pt="n" rel="--" root="uh" sense="uh" word="uh"/>
    <node begin="5" cat="du" end="21" id="10" rel="--">
      <node begin="5" case="both" def="indef" end="6" frame="pronoun(nwh,thi,sg,both,both,indef,strpro)" gen="both" his="normal" his_1="normal" id="11" lcat="np" lemma="één" num="sg" numtype="hoofd" per="thi" pos="pron" positie="vrij" postag="TW(hoofd,vrij)" pt="tw" rel="dp" rnum="sg" root="één" sense="één" special="strpro" wh="nwh" word="een"/>
      <node begin="8" cat="conj" end="21" id="12" rel="dp">
        <node begin="11" conjtype="neven" end="12" frame="conj(en)" his="normal" his_1="normal" id="13" lcat="vg" lemma="en" pos="vg" postag="VG(neven)" pt="vg" rel="crd" root="en" sense="en" word="en"/>
        <node begin="13" end="14" frame="tag" his="normal" his_1="normal" id="14" lcat="advp" lemma="ja" pos="tag" postag="TSW()" pt="tsw" rel="cnj" root="ja" sense="ja" word="ja"/>
        <node begin="8" cat="np" end="21" id="15" rel="cnj">
          <node begin="8" end="9" frame="determiner(een)" his="normal" his_1="normal" id="16" infl="een" lcat="detp" lemma="een" lwtype="onbep" naamval="stan" npagr="agr" pos="det" postag="LID(onbep,stan,agr)" pt="lid" rel="det" root="een" sense="een" word="een"/>
          <node begin="10" end="11" frame="noun(het,count,sg)" gen="het" genus="onz" getal="ev" graad="basis" his="normal" his_1="normal" id="17" lcat="np" lemma="ongeluk" naamval="stan" ntype="soort" num="sg" pos="noun" postag="N(soort,ev,basis,onz,stan)" pt="n" rel="hd" rnum="sg" root="ongeluk" sense="ongeluk" word="ongeluk"/>
          <node begin="14" cat="pp" end="21" id="18" rel="mod">
            <node begin="14" end="15" frame="preposition(met,[mee,[en,al]])" his="normal" his_1="normal" id="19" lcat="pp" lemma="met" pos="prep" postag="VZ(init)" pt="vz" rel="hd" root="met" sense="met" vztype="init" word="met"/>
            <node begin="15" cat="np" end="21" id="20" rel="obj1">
              <node begin="15" end="16" frame="determiner(de)" his="normal" his_1="normal" id="21" infl="de" lcat="detp" lemma="de" lwtype="bep" naamval="stan" npagr="rest" pos="det" postag="LID(bep,stan,rest)" pt="lid" rel="det" root="de" sense="de" word="de"/>
              <node begin="16" end="17" frame="noun(de,count,sg)" gen="de" genus="zijd" getal="ev" graad="basis" his="normal" his_1="normal" id="22" lcat="np" lemma="motor" naamval="stan" ntype="soort" num="sg" pos="noun" postag="N(soort,ev,basis,zijd,stan)" pt="n" rel="hd" rnum="sg" root="motor" sense="motor" word="motor"/>
              <node begin="17" cat="pp" end="20" id="23" rel="mod">
                <node begin="17" end="18" frame="preposition(in,[])" his="normal" his_1="normal" id="24" lcat="pp" lemma="in" pos="prep" postag="VZ(init)" pt="vz" rel="hd" root="in" sense="in" vztype="init" word="in"/>
                <node begin="18" cat="np" end="20" id="25" rel="obj1">
                  <node begin="18" buiging="zonder" end="19" frame="determiner(het,nwh,mod)" his="normal" his_1="normal" id="26" infl="het" lcat="detp" lemma="ieder" naamval="stan" npagr="evon" pdtype="det" pos="det" positie="prenom" postag="VNW(onbep,det,stan,prenom,zonder,evon)" pt="vnw" rel="det" root="ieder" sense="ieder" vwtype="onbep" wh="nwh" word="ieder"/>
                  <node begin="19" end="20" frame="noun(both,count,sg)" gen="both" genus="onz" getal="ev" graad="basis" his="normal" his_1="normal" id="27" lcat="np" lemma="geval" naamval="stan" ntype="soort" num="sg" pos="noun" postag="N(soort,ev,basis,onz,stan)" pt="n" rel="hd" rnum="sg" root="geval" sense="geval" word="geval"/>
                </node>
              </node>
              <node begin="20" end="21" frame="postnp_adverb" his="normal" his_1="normal" id="28" lcat="advp" lemma="dus" pos="adv" postag="BW()" pt="bw" rel="mod" root="dus" sense="dus" special="postnp" word="dus"/>
            </node>
          </node>
        </node>
      </node>
    </node>
    <node begin="21" end="22" frame="--" genus="zijd" getal="ev" graad="basis" his="skip" id="29" lcat="--" lemma="uh" naamval="stan" ntype="soort" pos="--" postag="N(soort,ev,basis,zijd,stan)" pt="n" rel="--" root="uh" sense="uh" word="uh"/>
  </node>
  <sentence sentid="8">Uh een uh een een een uh uh een uh ongeluk en uh ja met de motor in ieder geval dus uh</sentence>
<metadata>
<meta type="text" name="charencoding" value="UTF8" />
<meta type="text" name="childage" value="" />
<meta type="text" name="childmonths" value="" />
<meta type="text" name="comment" value="##META text samplenaam = ASTA-06" />
<meta type="text" name="session" value="ASTA_sample_06" />
<meta type="text" name="origutt" value="Uh een uh een een een uh uh een uh ongeluk en uh ja met de motor in ieder geval dus uh" />
<meta type="text" name="parsefile" value="Unknown_corpus_ASTA_sample_06_u00000000013.xml" />
<meta type="text" name="speaker" value="PMA" />
<meta type="int" name="uttendlineno" value="28" />
<meta type="int" name="uttid" value="8" />
<meta type="int" name="uttstartlineno" value="28" />
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
<meta type="text" name="xsid" value="8" />
<meta type="int" name="uttno" value="13" />
</metadata>
</alpino_ds>
"""

streestrings[2] = """
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
"""

streestrings[3] = """
<alpino_ds version="1.6">
  <parser cats="1" skips="0" />
  <node begin="0" cat="top" end="8" id="0" rel="top">
    <node begin="0" cat="du" end="8" id="1" rel="--">
      <node begin="0" cat="mwu" end="2" his="normal" his_1="decap" his_1_1="normal" id="2" mwu_root="ja ja" mwu_sense="ja ja" rel="tag">
        <node begin="0" end="1" frame="tag" id="3" lcat="advp" lemma="ja" pos="tag" postag="TSW()" pt="tsw" rel="mwp" root="ja" sense="ja" word="Ja"/>
        <node begin="1" end="2" frame="tag" id="4" lcat="advp" lemma="ja" pos="tag" postag="TSW()" pt="tsw" rel="mwp" root="ja" sense="ja" word="ja"/>
      </node>
      <node begin="2" cat="smain" end="8" id="5" rel="nucl">
        <node begin="2" case="nom" def="def" end="3" frame="pronoun(nwh,fir,sg,de,nom,def)" gen="de" getal="ev" his="normal" his_1="normal" id="6" lcat="np" lemma="ik" naamval="nomin" num="sg" pdtype="pron" per="fir" persoon="1" pos="pron" postag="VNW(pers,pron,nomin,vol,1,ev)" pt="vnw" rel="su" rnum="sg" root="ik" sense="ik" status="vol" vwtype="pers" wh="nwh" word="ik"/>
        <node begin="3" end="4" frame="verb(hebben,sg1,transitive_ndev)" his="normal" his_1="normal" id="7" infl="sg1" lcat="smain" lemma="hebben" pos="verb" postag="WW(pv,tgw,ev)" pt="ww" pvagr="ev" pvtijd="tgw" rel="hd" root="heb" sc="transitive_ndev" sense="heb" stype="declarative" tense="present" word="heb" wvorm="pv"/>
        <node begin="4" end="5" frame="tmp_adverb" his="normal" his_1="normal" id="8" lcat="advp" lemma="nu" pos="adv" postag="BW()" pt="bw" rel="mod" root="nu" sense="nu" special="tmp" word="nu"/>
        <node aform="base" begin="5" end="6" frame="adjective(pred(adv))" his="normal" his_1="normal" id="9" infl="pred" lcat="ap" lemma="wel" pos="adj" postag="BW()" pt="bw" rel="mod" root="wel" sense="wel" vform="adj" word="wel"/>
        <node begin="6" cat="np" end="8" id="10" rel="obj1">
          <node begin="6" end="7" frame="determiner(een)" his="normal" his_1="normal" id="11" infl="een" lcat="detp" lemma="een" lwtype="onbep" naamval="stan" npagr="agr" pos="det" postag="LID(onbep,stan,agr)" pt="lid" rel="det" root="een" sense="een" word="een"/>
          <node begin="7" end="8" frame="noun(het,count,sg)" gen="het" genus="onz" getal="ev" graad="basis" his="normal" his_1="normal" id="12" lcat="np" lemma="gezin" naamval="stan" ntype="soort" num="sg" pos="noun" postag="N(soort,ev,basis,onz,stan)" pt="n" rel="hd" rnum="sg" root="gezin" sense="gezin" word="gezin"/>
        </node>
      </node>
    </node>
  </node>
  <sentence sentid="28">Ja ja ik heb nu wel een gezin</sentence>
<metadata>
<meta type="text" name="charencoding" value="UTF8" />
<meta type="text" name="childage" value="" />
<meta type="text" name="childmonths" value="" />
<meta type="text" name="comment" value="##META text samplenaam = ASTA-06" />
<meta type="text" name="session" value="ASTA_sample_06" />
<meta type="text" name="origutt" value="Ja ja ik heb nu wel een gezin " />
<meta type="text" name="parsefile" value="Unknown_corpus_ASTA_sample_06_u00000000041.xml" />
<meta type="text" name="speaker" value="PMA" />
<meta type="int" name="uttendlineno" value="76" />
<meta type="int" name="uttid" value="28" />
<meta type="int" name="uttstartlineno" value="76" />
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
<meta type="text" name="xsid" value="28" />
<meta type="int" name="uttno" value="41" />
</metadata>
</alpino_ds>
"""

streestrings[4] = """
<alpino_ds version="1.6">
  <parser cats="1" skips="0" />
  <node begin="0" cat="top" end="8" id="0" rel="top">
    <node begin="0" cat="du" end="8" id="1" rel="--">
      <node begin="0" cat="mwu" end="2" his="normal" his_1="decap" his_1_1="normal" id="2" mwu_root="ja ja" mwu_sense="ja ja" rel="tag">
        <node begin="0" end="1" frame="tag" id="3" lcat="advp" lemma="ja" pos="tag" postag="TSW()" pt="tsw" rel="mwp" root="ja" sense="ja" word="Ja"/>
        <node begin="1" end="2" frame="tag" id="4" lcat="advp" lemma="ja" pos="tag" postag="TSW()" pt="tsw" rel="mwp" root="ja" sense="ja" word="ja"/>
      </node>
      <node begin="2" cat="smain" end="8" id="5" rel="nucl">
        <node begin="2" case="nom" def="def" end="3" frame="pronoun(nwh,fir,sg,de,nom,def)" gen="de" getal="ev" his="normal" his_1="normal" id="6" lcat="np" lemma="ik" naamval="nomin" num="sg" pdtype="pron" per="fir" persoon="1" pos="pron" postag="VNW(pers,pron,nomin,vol,1,ev)" pt="vnw" rel="su" rnum="sg" root="ik" sense="ik" status="vol" vwtype="pers" wh="nwh" word="xxx"/>
        <node begin="3" end="4" frame="verb(hebben,sg1,transitive_ndev)" his="normal" his_1="normal" id="7" infl="sg1" lcat="smain" lemma="hebben" pos="verb" postag="WW(pv,tgw,ev)" pt="ww" pvagr="ev" pvtijd="tgw" rel="hd" root="heb" sc="transitive_ndev" sense="heb" stype="declarative" tense="present" word="heb" wvorm="pv"/>
        <node begin="4" end="5" frame="tmp_adverb" his="normal" his_1="normal" id="8" lcat="advp" lemma="nu" pos="adv" postag="BW()" pt="bw" rel="mod" root="nu" sense="nu" special="tmp" word="nu"/>
        <node aform="base" begin="5" end="6" frame="adjective(pred(adv))" his="normal" his_1="normal" id="9" infl="pred" lcat="ap" lemma="wel" pos="adj" postag="BW()" pt="bw" rel="mod" root="wel" sense="wel" vform="adj" word="wel"/>
        <node begin="6" cat="np" end="8" id="10" rel="obj1">
          <node begin="6" end="7" frame="determiner(een)" his="normal" his_1="normal" id="11" infl="een" lcat="detp" lemma="een" lwtype="onbep" naamval="stan" npagr="agr" pos="det" postag="LID(onbep,stan,agr)" pt="lid" rel="det" root="een" sense="een" word="een"/>
          <node begin="7" end="8" frame="noun(het,count,sg)" gen="het" genus="onz" getal="ev" graad="basis" his="normal" his_1="normal" id="12" lcat="np" lemma="gezin" naamval="stan" ntype="soort" num="sg" pos="noun" postag="N(soort,ev,basis,onz,stan)" pt="n" rel="hd" rnum="sg" root="gezin" sense="gezin" word="gezin"/>
        </node>
      </node>
    </node>
  </node>
  <sentence sentid="28">Ja ja ik heb nu wel een gezin</sentence>
<metadata>
<meta type="text" name="charencoding" value="UTF8" />
<meta type="text" name="childage" value="" />
<meta type="text" name="childmonths" value="" />
<meta type="text" name="comment" value="##META text samplenaam = ASTA-06" />
<meta type="text" name="session" value="ASTA_sample_06" />
<meta type="text" name="origutt" value="Ja ja ik heb nu wel een gezin " />
<meta type="text" name="parsefile" value="Unknown_corpus_ASTA_sample_06_u00000000041.xml" />
<meta type="text" name="speaker" value="PMA" />
<meta type="int" name="uttendlineno" value="76" />
<meta type="int" name="uttid" value="28" />
<meta type="int" name="uttstartlineno" value="76" />
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
<meta type="text" name="xsid" value="28" />
<meta type="int" name="uttno" value="41" />
</metadata>
</alpino_ds>
"""


streestrings[5] = """
<alpino_ds version="1.6">
  <parser cats="1" skips="0" />
  <node begin="0" cat="top" end="8" id="0" rel="top">
    <node begin="2" end="3" frame="--" genus="zijd" getal="ev" graad="basis" his="skip" id="1" lcat="--" lemma="uhm" naamval="stan" ntype="soort" pos="--" postag="N(soort,ev,basis,zijd,stan)" pt="n" rel="--" root="uhm" sense="uhm" word="uhm"/>
    <node begin="0" cat="du" end="8" id="2" rel="--">
      <node begin="0" end="1" frame="tag" his="normal" his_1="enumeration" id="3" lcat="advp" lemma="O" pos="tag" postag="TSW()" pt="tsw" rel="tag" root="O" sense="O" word="O"/>
      <node begin="1" cat="du" end="8" id="4" rel="nucl">
        <node begin="1" end="2" frame="tag" his="normal" his_1="normal" id="5" lcat="advp" lemma="oke" pos="tag" postag="TSW()" pt="tsw" rel="tag" root="oke" sense="oke" word="oke"/>
        <node begin="3" cat="du" end="8" id="6" rel="nucl">
          <node begin="3" end="4" frame="adverb" getal="ev" his="normal" his_1="normal" id="7" lcat="advp" lemma="wat" naamval="stan" pdtype="pron" persoon="3o" pos="adv" postag="VNW(onbep,pron,stan,vol,3o,ev)" pt="vnw" rel="dp" root="wat" sense="wat" status="vol" vwtype="onbep" word="wat"/>
          <node begin="4" cat="whrel" end="8" id="8" rel="dp">
            <node begin="4" case="both" def="indef" end="5" frame="pronoun(ywh,thi,sg,het,both,indef,nparg)" gen="het" getal="ev" his="normal" his_1="normal" id="9" index="1" lcat="np" lemma="wat" naamval="stan" num="sg" pdtype="pron" per="thi" persoon="3o" pos="pron" postag="VNW(vb,pron,stan,vol,3o,ev)" pt="vnw" rel="rhd" rnum="sg" root="wat" sense="wat" special="nparg" status="vol" vwtype="vb" wh="ywh" word="wat"/>
            <node begin="4" cat="ssub" end="8" id="10" rel="body">
              <node begin="4" end="5" id="11" index="1" rel="su"/>
              <node begin="6" end="7" frame="verb(unacc,sg_heeft,aux_psp_zijn)" his="normal" his_1="normal" id="12" infl="sg_heeft" lcat="ssub" lemma="zijn" pos="verb" postag="WW(pv,tgw,ev)" pt="ww" pvagr="ev" pvtijd="tgw" rel="hd" root="ben" sc="aux_psp_zijn" sense="ben" tense="present" word="is" wvorm="pv"/>
              <node begin="4" cat="ppart" end="8" id="13" rel="vc">
                <node begin="4" end="5" id="14" index="1" rel="su"/>
                <node begin="5" end="6" frame="er_vp_adverb" getal="getal" his="normal" his_1="normal" id="15" lcat="advp" lemma="er" naamval="stan" pdtype="adv-pron" persoon="3" pos="adv" postag="VNW(aanw,adv-pron,stan,red,3,getal)" pt="vnw" rel="mod" root="er" sense="er" special="er" status="red" vwtype="aanw" word="er"/>
                <node begin="7" buiging="zonder" end="8" frame="verb(unacc,psp,intransitive)" his="normal" his_1="normal" id="16" infl="psp" lcat="ppart" lemma="gebeuren" pos="verb" positie="vrij" postag="WW(vd,vrij,zonder)" pt="ww" rel="hd" root="gebeur" sc="intransitive" sense="gebeur" word="gebeurd" wvorm="vd"/>
              </node>
            </node>
          </node>
        </node>
      </node>
    </node>
  </node>
  <sentence sentid="2">O oke uhm wat wat er is gebeurd</sentence>
<metadata>
<meta type="text" name="charencoding" value="UTF8" />
<meta type="text" name="childage" value="" />
<meta type="text" name="childmonths" value="" />
<meta type="text" name="comment" value="##META text samplenaam = ASTA-06" />
<meta type="text" name="session" value="ASTA_sample_06" />
<meta type="text" name="origutt" value="O oke uhm wat wat er is gebeurd" />
<meta type="text" name="parsefile" value="Unknown_corpus_ASTA_sample_06_u00000000004.xml" />
<meta type="text" name="speaker" value="PMA" />
<meta type="int" name="uttendlineno" value="13" />
<meta type="int" name="uttid" value="2" />
<meta type="int" name="uttstartlineno" value="13" />
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
<meta type="text" name="xsid" value="2" />
<meta type="int" name="uttno" value="4" />
</metadata>
</alpino_ds>
"""

streestrings[6] = """
<alpino_ds version="1.6">
  <parser cats="3" skips="5" />
  <node begin="0" cat="top" end="13" id="0" rel="top">
    <node begin="0" end="1" frame="--" genus="zijd" getal="ev" graad="basis" his="skip" id="1" lcat="--" lemma="uhm" naamval="stan" ntype="soort" pos="--" postag="N(soort,ev,basis,zijd,stan)" pt="n" rel="--" root="uhm" sense="uhm" word="uhm"/>
    <node begin="4" end="5" frame="determiner(de)" his="skip" id="2" infl="de" lcat="--" lemma="de" lwtype="bep" naamval="stan" npagr="rest" pos="det" postag="LID(bep,stan,rest)" pt="lid" rel="--" root="de" sense="de" word="de"/>
    <node begin="5" end="6" frame="determiner(de)" his="skip" id="3" infl="de" lcat="--" lemma="de" lwtype="bep" naamval="stan" npagr="rest" pos="det" postag="LID(bep,stan,rest)" pt="lid" rel="--" root="de" sense="de" word="de"/>
    <node begin="6" end="7" frame="--" genus="zijd" getal="ev" graad="basis" his="skip" id="4" lcat="--" lemma="uh" naamval="stan" ntype="soort" pos="--" postag="N(soort,ev,basis,zijd,stan)" pt="n" rel="--" root="uh" sense="uh" word="uh"/>
    <node begin="7" end="8" frame="determiner(de)" his="robust_skip" id="5" infl="de" lcat="--" lemma="de" lwtype="bep" naamval="stan" npagr="rest" pos="det" postag="LID(bep,stan,rest)" pt="lid" rel="--" root="de" sense="de" word="de"/>
    <node begin="8" end="9" frame="--" genus="zijd" getal="ev" graad="basis" his="robust_skip" id="6" lcat="--" lemma="uh" naamval="stan" ntype="soort" pos="--" postag="N(soort,ev,basis,zijd,stan)" pt="n" rel="--" root="uh" sense="uh" word="uh"/>
    <node begin="1" cat="du" end="10" id="7" rel="--">
      <node begin="1" case="nom" def="def" end="2" frame="pronoun(nwh,fir,sg,de,nom,def)" gen="de" getal="ev" his="normal" his_1="normal" id="8" lcat="np" lemma="ik" naamval="nomin" num="sg" pdtype="pron" per="fir" persoon="1" pos="pron" postag="VNW(pers,pron,nomin,vol,1,ev)" pt="vnw" rel="dp" rnum="sg" root="ik" sense="ik" status="vol" vwtype="pers" wh="nwh" word="ik"/>
      <node begin="2" cat="smain" end="4" id="9" rel="dp">
        <node begin="2" case="nom" def="def" end="3" frame="pronoun(nwh,fir,sg,de,nom,def)" gen="de" getal="ev" his="normal" his_1="normal" id="10" lcat="np" lemma="ik" naamval="nomin" num="sg" pdtype="pron" per="fir" persoon="1" pos="pron" postag="VNW(pers,pron,nomin,vol,1,ev)" pt="vnw" rel="su" rnum="sg" root="ik" sense="ik" status="vol" vwtype="pers" wh="nwh" word="ik"/>
        <node begin="3" end="4" frame="verb(unacc,sg1,intransitive)" his="normal" his_1="normal" id="11" infl="sg1" lcat="smain" lemma="zijn" pos="verb" postag="WW(pv,tgw,ev)" pt="ww" pvagr="ev" pvtijd="tgw" rel="hd" root="ben" sc="intransitive" sense="ben" stype="declarative" tense="present" word="ben" wvorm="pv"/>
      </node>
      <node begin="9" buiging="met-e" case="both" def="def" end="10" frame="pronoun(nwh,thi,sg,de,both,def,strpro)" gen="de" getal-n="zonder-n" his="normal" his_1="normal" id="12" lcat="np" lemma="degeen" naamval="stan" num="sg" pdtype="det" per="thi" pos="pron" positie="nom" postag="VNW(aanw,det,stan,nom,met-e,zonder-n)" pt="vnw" rel="dp" rnum="sg" root="degeen" sense="degeen" special="strpro" vwtype="aanw" wh="nwh" word="degene"/>
    </node>
    <node begin="10" case="no_obl" end="11" frame="rel_pronoun(de,no_obl)" gen="de" getal="getal" his="robust_skip" id="13" lcat="--" lemma="die" naamval="stan" pdtype="pron" persoon="persoon" pos="pron" postag="VNW(betr,pron,stan,vol,persoon,getal)" pt="vnw" rel="--" root="die" sense="die" status="vol" vwtype="betr" wh="rel" word="die"/>
    <node begin="11" end="12" frame="--" genus="zijd" getal="ev" graad="basis" his="robust_skip" id="14" lcat="--" lemma="uhm" naamval="stan" ntype="soort" pos="--" postag="N(soort,ev,basis,zijd,stan)" pt="n" rel="--" root="uhm" sense="uhm" word="uhm"/>
    <node begin="12" end="13" frame="--" genus="zijd" getal="ev" graad="basis" his="robust_skip" id="15" lcat="--" lemma="uhm" naamval="stan" ntype="soort" pos="--" postag="N(soort,ev,basis,zijd,stan)" pt="n" rel="--" root="uhm" sense="uhm" word="uhm"/>
  </node>
  <sentence sentid="19">uhm ik ik ben de de uh de uh degene die uhm uhm</sentence>
<metadata>
<meta type="text" name="charencoding" value="UTF8" />
<meta type="text" name="childage" value="" />
<meta type="text" name="childmonths" value="" />
<meta type="text" name="comment" value="##META text samplenaam = ASTA-06" />
<meta type="text" name="session" value="ASTA_sample_06" />
<meta type="text" name="origutt" value="uhm ik ik ben de de uh de uh degene die uhm uhm " />
<meta type="text" name="parsefile" value="Unknown_corpus_ASTA_sample_06_u00000000028.xml" />
<meta type="text" name="speaker" value="PMA" />
<meta type="int" name="uttendlineno" value="54" />
<meta type="int" name="uttid" value="19" />
<meta type="int" name="uttstartlineno" value="54" />
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
<meta type="text" name="xsid" value="19" />
<meta type="int" name="uttno" value="28" />
</metadata>
</alpino_ds>
"""

for x in streestrings:
    strees[x] = etree.fromstring(streestrings[x])

streemluxtestlist = [(strees[1], ['2', '4', '5', '6', '14']), (strees[2], ['1', '5']), (strees[3], ['2']), (strees[4], ['2', '3', '4', '5', '6', '7', '8']),
                     (strees[5], ['2', '4']), (strees[6], ['2'])]
streesamplesizetestlist = [(strees[1], ['1', '3', '7', '8', '10', '13', '22']), (strees[2], ['2', '4']), (strees[3], ['1']), (strees[4], ['1']), (strees[5], ['1', '3']),
                           (strees[6], ['1', '5', '6', '7', '8', '9', '12', '13'])]


def report(inval, out, gold):
    sortedout = sorted(out)
    sortedgold = sorted(gold)
    if sortedout == sortedgold:
        print('OK:', inval, sortedout, '==', sortedgold)
    else:
        print('NO:', inval, sortedout, '!=', sortedgold)


def fptest():
    for (inval, gold) in filledpausestestdata:
        intokenlist = tokenize(inval)
        fpposlist = getfilledpausesposlist(intokenlist)
        outtokenlist = [t for t in intokenlist if t.pos not in fpposlist]
        goldtokenlist = tokenize(gold)
        outstringlist = tokenlist2stringlist(outtokenlist)
        goldstringlist = tokenlist2stringlist(goldtokenlist)
        report(inval, outstringlist, goldstringlist)


def streetest():
    for (stree, gold) in streemluxtestlist:
        resultnodelist = mlux(stree)
        resultposlist = [getattval(n, 'end') for n in resultnodelist]
        instrlist = [getattval(n, 'word') for n in getnodeyield(stree)]
        instr = space.join(instrlist)
        report(instr, resultposlist, gold)

    print(20 * '-')

    for (stree, gold) in streesamplesizetestlist:
        resultnodelist = samplesize(stree)
        resultposlist = [getattval(n, 'end') for n in resultnodelist]
        instrlist = [getattval(n, 'word') for n in getnodeyield(stree)]
        instr = space.join(instrlist)
        report(instr, resultposlist, gold)


def adhoctest():
    results = mlux(stree[2])
    words = [(getattval(r, 'end') + getattval(r, 'word')) for r in results]
    for w in words:
        print(w)


if __name__ == '__main__':
    # adhoctest()
    # exit(0)
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename",
                      help="Treebank File to be analysed")
    (options, args) = parser.parse_args()
    if options.filename:
        streefiletest(options.filename)
    print(20 * '-')
    streetest()
    print(20 * '-')
    fptest()
    print(20 * '-')
    test(testgoldstrings)
    print(20 * '-')
    tokentest(testgoldlists)