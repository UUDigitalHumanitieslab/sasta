from lxml import etree

streexml = {}
stree = {}

streexml[1] = '''
<alpino_ds version="1.3" id="Tarvb2-22.xml">
  <node begin="0" cat="top" end="8" id="0" rel="top" highlight="yes">
    <node begin="0" cat="whq" end="7" id="1" rel="--" highlight="yes">
      <node begin="0" case="both" def="indef" end="1" frame="pronoun(ywh,thi,sg,het,both,indef,nparg)" gen="het" getal="ev" id="2" index="1" lcat="np" lemma="wat" naamval="stan" num="sg" pdtype="pron" per="thi" persoon="3o" pos="pron" postag="VNW(vb,pron,stan,vol,3o,ev)" pt="vnw" rel="whd" rnum="sg" root="wat" sense="wat" special="nparg" status="vol" vwtype="vb" wh="ywh" word="wat" highlight="yes"/>
      <node begin="0" cat="sv1" end="7" id="3" rel="body" highlight="yes">
        <node begin="1" end="2" frame="verb('hebben/zijn',pl,modifier(aux(inf)))" id="4" infl="pl" lcat="sv1" lemma="moeten" pos="verb" postag="WW(pv,tgw,mv)" pt="ww" pvagr="mv" pvtijd="tgw" rel="hd" root="moet" sc="modifier(aux(inf))" sense="moet" stype="whquestion" tense="present" word="moeten" wvorm="pv" highlight="yes"/>
        <node begin="2" case="nom" def="def" end="3" frame="pronoun(nwh,fir,pl,de,nom,def,wkpro)" gen="de" getal="mv" id="5" index="2" lcat="np" lemma="we" naamval="nomin" num="pl" pdtype="pron" per="fir" persoon="1" pos="pron" postag="VNW(pers,pron,nomin,red,1,mv)" pt="vnw" rel="su" rnum="pl" root="we" sense="we" special="wkpro" status="red" vwtype="pers" wh="nwh" word="we" highlight="yes"/>
        <node begin="0" cat="inf" end="7" id="6" rel="vc" highlight="yes">
          <node begin="0" end="1" id="7" index="1" rel="obj1" highlight="yes"/>
          <node begin="2" end="3" id="8" index="2" rel="su" highlight="yes"/>
          <node begin="3" cat="pp" end="6" id="9" rel="mod" highlight="yes">
            <node begin="3" end="4" frame="preposition(met,[mee,[en,al]])" id="10" lcat="pp" lemma="met" pos="prep" postag="VZ(init)" pt="vz" rel="hd" root="met" sense="met" vztype="init" word="met" highlight="yes"/>
            <node begin="4" cat="np" end="6" id="11" rel="obj1" highlight="yes">
              <node begin="4" buiging="zonder" end="5" frame="determiner(de,nwh,nmod,pro,nparg)" id="12" infl="de" lcat="detp" lemma="die" naamval="stan" npagr="rest" pdtype="det" pos="det" positie="prenom" postag="VNW(aanw,det,stan,prenom,zonder,rest)" pt="vnw" rel="det" root="die" sense="die" vwtype="aanw" wh="nwh" word="die" highlight="yes"/>
              <node begin="5" end="6" frame="noun(de,count,sg)" gen="de" genus="zijd" getal="ev" graad="basis" id="13" lcat="np" lemma="stuk_kies" naamval="stan" ntype="soort" num="sg" pos="noun" postag="N(soort,ev,basis,zijd,stan)" pt="n" rel="hd" rnum="sg" root="stuk_kies" sense="stuk_kies" word="stukkies" highlight="yes"/>
            </node>
          </node>
          <node begin="6" buiging="zonder" end="7" frame="verb(hebben,inf(no_e),transitive_ndev)" id="14" infl="inf(no_e)" lcat="inf" lemma="doen" pos="verb" positie="vrij" postag="WW(inf,vrij,zonder)" pt="ww" rel="hd" root="doe" sc="transitive_ndev" sense="doe" word="doen" wvorm="inf" highlight="yes"/>
        </node>
      </node>
    </node>
    <node begin="7" end="8" frame="punct(vraag)" id="15" lcat="punct" lemma="?" pos="punct" postag="LET()" pt="let" rel="--" root="?" sense="?" special="vraag" word="?" highlight="yes"/>
  </node>
  <sentence sentid="22 ">wat moeten we met die stukkies doen ?</sentence>
  <metadata/>
</alpino_ds>
'''


streexml[2] = '''
<alpino_ds version="1.6" id="ASTA_06-ASTA_sample_06_001.xml">
  <parser cats="2" skips="0"/>
  <node begin="0" cat="top" end="6" id="0" rel="top" highlight="yes">
    <node begin="0" cat="du" end="6" id="1" rel="--" highlight="yes">
      <node begin="0" cat="smain" end="2" id="2" rel="dp" highlight="yes">
        <node begin="0" end="1" frame="determiner(het,nwh,nmod,pro,nparg)" getal="ev" his="normal" his_1="decap" his_1_1="normal" id="3" infl="het" lcat="np" lemma="dat" naamval="stan" pdtype="pron" persoon="3o" pos="det" postag="VNW(aanw,pron,stan,vol,3o,ev)" pt="vnw" rel="su" rnum="sg" root="dat" sense="dat" status="vol" vwtype="aanw" wh="nwh" word="Dat" highlight="yes"/>
        <node begin="1" end="2" frame="verb(unacc,sg_heeft,intransitive)" his="normal" his_1="normal" id="4" infl="sg_heeft" lcat="smain" lemma="zijn" pos="verb" postag="WW(pv,tgw,ev)" pt="ww" pvagr="ev" pvtijd="tgw" rel="hd" root="ben" sc="intransitive" sense="ben" stype="declarative" tense="present" word="is" wvorm="pv" highlight="yes"/>
      </node>
      <node begin="2" cat="smain" end="6" id="5" rel="dp" highlight="yes">
        <node begin="2" end="3" frame="determiner(het,nwh,nmod,pro,nparg)" getal="ev" his="normal" his_1="normal" id="6" infl="het" lcat="np" lemma="dat" naamval="stan" pdtype="pron" persoon="3o" pos="det" postag="VNW(aanw,pron,stan,vol,3o,ev)" pt="vnw" rel="obj1" rnum="sg" root="dat" sense="dat" status="vol" vwtype="aanw" wh="nwh" word="dat" highlight="yes"/>
        <node begin="3" end="4" frame="verb(hebben,sg,transitive)" his="normal" his_1="normal" id="7" infl="sg" lcat="smain" lemma="weten" pos="verb" postag="WW(pv,tgw,ev)" pt="ww" pvagr="ev" pvtijd="tgw" rel="hd" root="weet" sc="transitive" sense="weet" stype="declarative" tense="present" word="weet" wvorm="pv" highlight="yes"/>
        <node begin="4" case="nom" def="def" end="5" frame="pronoun(nwh,fir,sg,de,nom,def)" gen="de" getal="ev" his="normal" his_1="normal" id="8" lcat="np" lemma="ik" naamval="nomin" num="sg" pdtype="pron" per="fir" persoon="1" pos="pron" postag="VNW(pers,pron,nomin,vol,1,ev)" pt="vnw" rel="su" rnum="sg" root="ik" sense="ik" status="vol" vwtype="pers" wh="nwh" word="ik" highlight="yes"/>
        <node begin="5" end="6" frame="adverb" his="normal" his_1="normal" id="9" lcat="advp" lemma="niet" pos="adv" postag="BW()" pt="bw" rel="mod" root="niet" sense="niet" word="niet" highlight="yes"/>
      </node>
    </node>
  </node>
  <sentence sentid="1">Dat is dat weet ik niet</sentence>
  <metadata>
    <meta type="text" name="charencoding" value="UTF8"/>
    <meta type="text" name="childage" value=""/>
    <meta type="text" name="childmonths" value=""/>
    <meta type="text" name="comment" value="##META text samplenaam = ASTA-06"/>
    <meta type="text" name="session" value="ASTA_sample_06"/>
    <meta type="text" name="origutt" value="Dat is dat weet ik niet"/>
    <meta type="text" name="parsefile" value="Unknown_corpus_ASTA_sample_06_u00000000002.xml"/>
    <meta type="text" name="speaker" value="PMA"/>
    <meta type="int" name="uttendlineno" value="10"/>
    <meta type="int" name="uttid" value="1"/>
    <meta type="int" name="uttstartlineno" value="10"/>
    <meta type="text" name="name" value="pma"/>
    <meta type="text" name="SES" value=""/>
    <meta type="text" name="age" value=""/>
    <meta type="text" name="custom" value=""/>
    <meta type="text" name="education" value=""/>
    <meta type="text" name="group" value=""/>
    <meta type="text" name="language" value="nld"/>
    <meta type="text" name="months" value=""/>
    <meta type="text" name="role" value="Other"/>
    <meta type="text" name="sex" value=""/>
    <meta type="text" name="xsid" value="1"/>
    <meta type="int" name="uttno" value="2"/>
  </metadata>
</alpino_ds>
'''

for el in streexml:
    stree[el] = etree.fromstring(streexml[el])
