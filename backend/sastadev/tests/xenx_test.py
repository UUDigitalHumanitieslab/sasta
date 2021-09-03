from lxml import etree

from sastadev.treebankfunctions import getyield
from sastadev.xenx import xenx

teststr = {}

teststr[1] = '''
<alpino_ds version="1.6">
  <parser cats="1" skips="0" />
  <node begin="0" cat="top" end="5" id="0" rel="top">
    <node begin="0" cat="smain" end="4" id="1" rel="--">
      <node begin="0" case="nom" def="def" end="1" frame="pronoun(nwh,thi,sg,de,nom,def)" gen="de" genus="masc" getal="ev" his="normal" his_1="normal" id="2" lcat="np" lemma="hij" naamval="nomin" num="sg" pdtype="pron" per="thi" persoon="3" pos="pron" postag="VNW(pers,pron,nomin,vol,3,ev,masc)" pt="vnw" rel="su" rnum="sg" root="hij" sense="hij" status="vol" vwtype="pers" wh="nwh" word="hij"/>
      <node begin="1" end="2" frame="verb(hebben,modal_not_u,intransitive)" his="normal" his_1="normal" id="3" infl="modal_not_u" lcat="smain" lemma="willen" pos="verb" postag="WW(pv,tgw,ev)" pt="ww" pvagr="ev" pvtijd="tgw" rel="hd" root="wil" sc="intransitive" sense="wil" stype="declarative" tense="present" word="wil" wvorm="pv"/>
      <node begin="2" end="3" frame="adverb" his="normal" his_1="normal" id="4" lcat="advp" lemma="niet" pos="adv" postag="BW()" pt="bw" rel="mod" root="niet" sense="niet" word="niet"/>
      <node begin="3" end="4" frame="loc_adverb" his="normal" his_1="normal" id="5" lcat="advp" lemma="buiten" pos="adv" postag="VZ(fin)" pt="vz" rel="mod" root="buiten" sense="buiten" special="loc" vztype="fin" word="buiten"/>
    </node>
    <node begin="4" end="5" frame="punct(punt)" his="normal" his_1="normal" id="6" lcat="punct" lemma="." pos="punct" postag="LET()" pt="let" rel="--" root="." sense="." special="punt" word="."/>
  </node>
  <sentence sentid="9">hij wil niet buiten .</sentence>
<metadata>
<meta type="text" name="charencoding" value="UTF8" />
<meta type="text" name="childage" value="4;6" />
<meta type="int" name="childmonths" value="54" />
<meta type="text" name="comment" value="##META text title = Tarsp_01" />
<meta type="text" name="session" value="Tarsp_01" />
<meta type="text" name="origutt" value="hij wil niet buiten." />
<meta type="text" name="parsefile" value="Unknown_corpus_Tarsp_01_u00000000009.xml" />
<meta type="text" name="speaker" value="CHI" />
<meta type="int" name="uttendlineno" value="24" />
<meta type="int" name="uttid" value="9" />
<meta type="int" name="uttstartlineno" value="24" />
<meta type="text" name="name" value="chi" />
<meta type="text" name="SES" value="" />
<meta type="text" name="age" value="4;6" />
<meta type="text" name="custom" value="" />
<meta type="text" name="education" value="" />
<meta type="text" name="group" value="" />
<meta type="text" name="language" value="nld" />
<meta type="int" name="months" value="54" />
<meta type="text" name="role" value="Target_Child" />
<meta type="text" name="sex" value="male" />
<meta type="text" name="xsid" value="9" />
<meta type="int" name="uttno" value="9" />
</metadata>
</alpino_ds>
'''

teststr[2] = '''
<alpino_ds version="1.6">
  <parser cats="1" skips="0" />
  <node begin="0" cat="top" end="10" id="0" rel="top">
    <node begin="0" cat="sv1" end="9" id="1" rel="--">
      <node begin="0" end="1" frame="verb(hebben,sg1,intransitive)" his="normal" his_1="normal" id="2" infl="sg1" lcat="sv1" lemma="emmeren" pos="verb" postag="WW(pv,tgw,ev)" pt="ww" pvagr="ev" pvtijd="tgw" rel="hd" root="emmer" sc="intransitive" sense="emmer" stype="topic_drop" tense="present" word="emmer" wvorm="pv"/>
      <node begin="1" end="2" frame="loc_adverb" his="normal" his_1="normal" id="3" lcat="advp" lemma="mee" pos="adv" postag="BW()" pt="bw" rel="mod" root="mee" sense="mee" special="loc" word="mee"/>
      <node begin="2" cat="conj" end="9" id="4" rel="mod">
        <node begin="2" cat="pp" end="5" id="5" rel="cnj">
          <node begin="2" end="3" frame="preposition(voor,[aan,door,uit,[in,de,plaats]])" his="normal" his_1="normal" id="6" lcat="pp" lemma="voor" pos="prep" postag="VZ(init)" pt="vz" rel="hd" root="voor" sense="voor" vztype="init" word="voor"/>
          <node begin="3" cat="np" end="5" id="7" rel="obj1">
            <node begin="3" end="4" frame="determiner(de)" his="normal" his_1="normal" id="8" infl="de" lcat="detp" lemma="de" lwtype="bep" naamval="stan" npagr="rest" pos="det" postag="LID(bep,stan,rest)" pt="lid" rel="det" root="de" sense="de" word="de"/>
            <node begin="4" end="5" frame="noun(het,count,pl)" gen="het" getal="mv" graad="basis" his="normal" his_1="normal" id="9" lcat="np" lemma="varken" ntype="soort" num="pl" pos="noun" postag="N(soort,mv,basis)" pt="n" rel="hd" rnum="pl" root="varken" sense="varken" word="varkens"/>
          </node>
        </node>
        <node begin="5" conjtype="neven" end="6" frame="conj(en)" his="normal" his_1="normal" id="10" lcat="vg" lemma="en" pos="vg" postag="VG(neven)" pt="vg" rel="crd" root="en" sense="en" word="en"/>
        <node begin="6" cat="pp" end="9" id="11" rel="cnj">
          <node begin="6" end="7" frame="preposition(voor,[aan,door,uit,[in,de,plaats]])" his="normal" his_1="normal" id="12" lcat="pp" lemma="voor" pos="prep" postag="VZ(init)" pt="vz" rel="hd" root="voor" sense="voor" vztype="init" word="voor"/>
          <node begin="7" cat="np" end="9" id="13" rel="obj1">
            <node begin="7" end="8" frame="determiner(de)" his="normal" his_1="normal" id="14" infl="de" lcat="detp" lemma="de" lwtype="bep" naamval="stan" npagr="rest" pos="det" postag="LID(bep,stan,rest)" pt="lid" rel="det" root="de" sense="de" word="de"/>
            <node begin="8" end="9" frame="noun(het,count,pl)" gen="het" getal="mv" graad="dim" his="normal" his_1="normal" id="15" lcat="np" lemma="poes" ntype="soort" num="pl" pos="noun" postag="N(soort,mv,dim)" pt="n" rel="hd" rnum="pl" root="poes_DIM" sense="poes_DIM" word="poesjes"/>
          </node>
        </node>
      </node>
    </node>
    <node begin="9" end="10" frame="punct(punt)" his="normal" his_1="normal" id="16" lcat="punct" lemma="." pos="punct" postag="LET()" pt="let" rel="--" root="." sense="." special="punt" word="."/>
  </node>
  <sentence sentid="10">emmer mee voor de varkens en voor de poesjes .</sentence>
<metadata>
<meta type="text" name="charencoding" value="UTF8" />
<meta type="text" name="childage" value="4;6" />
<meta type="int" name="childmonths" value="54" />
<meta type="text" name="comment" value="##META text title = Tarsp_01" />
<meta type="text" name="session" value="Tarsp_01" />
<meta type="text" name="origutt" value="emmer mee voor de varkens en voor de poesjes." />
<meta type="text" name="parsefile" value="Unknown_corpus_Tarsp_01_u00000000010.xml" />
<meta type="text" name="speaker" value="CHI" />
<meta type="int" name="uttendlineno" value="26" />
<meta type="int" name="uttid" value="10" />
<meta type="int" name="uttstartlineno" value="26" />
<meta type="text" name="name" value="chi" />
<meta type="text" name="SES" value="" />
<meta type="text" name="age" value="4;6" />
<meta type="text" name="custom" value="" />
<meta type="text" name="education" value="" />
<meta type="text" name="group" value="" />
<meta type="text" name="language" value="nld" />
<meta type="int" name="months" value="54" />
<meta type="text" name="role" value="Target_Child" />
<meta type="text" name="sex" value="male" />
<meta type="text" name="xsid" value="10" />
<meta type="int" name="uttno" value="10" />
</metadata>
</alpino_ds>
'''

teststr[3] = '''
<alpino_ds version="1.6">
  <parser cats="1" skips="0" />
  <node begin="0" cat="top" end="4" id="0" rel="top">
    <node begin="0" cat="conj" end="3" id="1" rel="--">
      <node begin="0" end="1" frame="noun(het,both,sg)" gen="het" genus="onz" getal="ev" graad="basis" his="normal" his_1="normal" id="2" lcat="np" lemma="water" naamval="stan" ntype="soort" num="sg" pos="noun" postag="N(soort,ev,basis,onz,stan)" pt="n" rel="cnj" rnum="sg" root="water" sense="water" word="water"/>
      <node begin="1" conjtype="neven" end="2" frame="conj(en)" his="normal" his_1="normal" id="3" lcat="vg" lemma="en" pos="vg" postag="VG(neven)" pt="vg" rel="crd" root="en" sense="en" word="en"/>
      <node begin="2" end="3" frame="noun(de,mass,sg)" gen="de" genus="zijd" getal="ev" graad="basis" his="normal" his_1="normal" id="4" lcat="np" lemma="melk" naamval="stan" ntype="soort" num="sg" pos="noun" postag="N(soort,ev,basis,zijd,stan)" pt="n" rel="cnj" rnum="sg" root="melk" sense="melk" word="melk"/>
    </node>
    <node begin="3" end="4" frame="punct(punt)" his="normal" his_1="normal" id="5" lcat="punct" lemma="." pos="punct" postag="LET()" pt="let" rel="--" root="." sense="." special="punt" word="."/>
  </node>
  <sentence sentid="11">water en melk .</sentence>
<metadata>
<meta type="text" name="charencoding" value="UTF8" />
<meta type="text" name="childage" value="4;6" />
<meta type="int" name="childmonths" value="54" />
<meta type="text" name="comment" value="##META text title = Tarsp_01" />
<meta type="text" name="session" value="Tarsp_01" />
<meta type="text" name="origutt" value="water en melk." />
<meta type="text" name="parsefile" value="Unknown_corpus_Tarsp_01_u00000000011.xml" />
<meta type="text" name="speaker" value="CHI" />
<meta type="int" name="uttendlineno" value="28" />
<meta type="int" name="uttid" value="11" />
<meta type="int" name="uttstartlineno" value="28" />
<meta type="text" name="name" value="chi" />
<meta type="text" name="SES" value="" />
<meta type="text" name="age" value="4;6" />
<meta type="text" name="custom" value="" />
<meta type="text" name="education" value="" />
<meta type="text" name="group" value="" />
<meta type="text" name="language" value="nld" />
<meta type="int" name="months" value="54" />
<meta type="text" name="role" value="Target_Child" />
<meta type="text" name="sex" value="male" />
<meta type="text" name="xsid" value="11" />
<meta type="int" name="uttno" value="11" />
</metadata>
</alpino_ds>

'''

testtrees = {}
for el in teststr:
    testtrees[el] = etree.fromstring(teststr[el])


def test_xenx():
    for i in testtrees:
        print(i)
        results = xenx(testtrees[i])
        treeyield = getyield(testtrees[i])
        print(treeyield)
        for result in results:
            resultyield = getyield(result)
            print('--', resultyield)
