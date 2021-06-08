from lxml import etree

from sastadev.imperatives import wond4, wondx, wx, wxyz, wxyz5, wxy, wond5plus

testtreestr = {}

testtreestr[1] = '''
  <alpino_ds version="1.3" id="TARSP_Examples_from_Schlichting-104.xml">
    <node begin="0" cat="top" end="6" id="0" rel="top">
      <node begin="0" cat="sv1" end="5" id="1" rel="--">
        <node begin="0" end="1" frame="verb(hebben,sg1,sbar)" id="2" infl="sg1" lcat="sv1" lemma="kijken" pos="verb" postag="WW(pv,tgw,ev)" pt="ww" pvagr="ev" pvtijd="tgw" rel="hd" root="kijk" sc="sbar" sense="kijk" stype="imparative" tense="present" word="kijk" wvorm="pv"/>
        <node begin="1" cat="cp" end="5" id="3" rel="vc">
          <node begin="1" conjtype="onder" end="2" frame="complementizer(of)" id="4" lcat="cp" lemma="of" pos="comp" postag="VG(onder)" pt="vg" rel="cmp" root="of" sc="of" sense="of" word="of"/>
          <node begin="2" cat="ssub" end="5" id="5" rel="body">
            <node begin="2" end="3" frame="determiner(het,nwh,nmod,pro,nparg,wkpro)" genus="onz" getal="ev" id="6" infl="het" lcat="np" lemma="het" naamval="stan" pdtype="pron" persoon="3" pos="det" postag="VNW(pers,pron,stan,red,3,ev,onz)" pt="vnw" rel="su" rnum="sg" root="het" sense="het" status="red" vwtype="pers" wh="nwh" word="het"/>
            <node aform="base" begin="3" buiging="zonder" end="4" frame="adjective(no_e(adv))" graad="basis" id="7" infl="no_e" lcat="ap" lemma="goed" pos="adj" positie="vrij" postag="ADJ(vrij,basis,zonder)" pt="adj" rel="predc" root="goed" sense="goed" vform="adj" word="goed"/>
            <node begin="4" end="5" frame="verb(unacc,sg_heeft,copula)" id="8" infl="sg_heeft" lcat="ssub" lemma="zijn" pos="verb" postag="WW(pv,tgw,ev)" pt="ww" pvagr="ev" pvtijd="tgw" rel="hd" root="ben" sc="copula" sense="ben" tense="present" word="is" wvorm="pv"/>
          </node>
        </node>
      </node>
      <node begin="5" end="6" frame="punct(uitroep)" id="9" lcat="punct" lemma="!" pos="punct" postag="LET()" pt="let" rel="--" root="!" sense="!" special="uitroep" word="!"/>
    </node>
    <sentence sentid="104">kijk of het goed is !</sentence>
    <metadata/>
  </alpino_ds>
'''


testtreestr[2] = '''
  <alpino_ds version="1.3" id="TARSP_Examples_from_Schlichting-149.xml">
    <node begin="0" cat="top" end="3" id="0" rel="top">
      <node begin="0" cat="sv1" end="2" id="1" rel="--">
        <node begin="0" end="1" frame="verb(hebben,sg1,intransitive)" id="2" infl="sg1" lcat="sv1" lemma="zien" pos="verb" postag="WW(pv,tgw,ev)" pt="ww" pvagr="ev" pvtijd="tgw" rel="hd" root="zie" sc="intransitive" sense="zie" stype="imparative" tense="present" word="zie" wvorm="pv"/>
        <node begin="1" end="2" frame="adverb" id="3" lcat="advp" lemma="maar" pos="adv" postag="BW()" pt="bw" rel="mod" root="maar" sense="maar" word="maar"/>
      </node>
      <node begin="2" end="3" frame="punct(uitroep)" id="4" lcat="punct" lemma="!" pos="punct" postag="LET()" pt="let" rel="--" root="!" sense="!" special="uitroep" word="!"/>
    </node>
    <sentence sentid="149">zie maar !</sentence>
    <metadata/>
  </alpino_ds>
'''


testtreestr[3] = '''

  <alpino_ds version="1.3" id="TARSP_Examples_from_Schlichting-151.xml">
    <node begin="0" cat="top" end="6" id="0" rel="top">
      <node begin="0" cat="sv1" end="5" id="1" rel="--">
        <node begin="0" end="1" frame="verb(hebben,sg1,ld_pp)" id="2" infl="sg1" lcat="sv1" lemma="kijken" pos="verb" postag="WW(pv,tgw,ev)" pt="ww" pvagr="ev" pvtijd="tgw" rel="hd" root="kijk" sc="ld_pp" sense="kijk" stype="imparative" tense="present" word="kijk" wvorm="pv"/>
        <node begin="1" end="2" frame="tmp_adverb" id="3" lcat="advp" lemma="eens" pos="adv" postag="BW()" pt="bw" rel="mod" root="eens" sense="eens" special="tmp" word="eens"/>
        <node begin="2" cat="pp" end="5" id="4" rel="ld">
          <node begin="2" end="3" frame="preposition(in,[])" id="5" lcat="pp" lemma="in" pos="prep" postag="VZ(init)" pt="vz" rel="hd" root="in" sense="in" vztype="init" word="in"/>
          <node begin="3" cat="np" end="5" id="6" rel="obj1">
            <node begin="3" end="4" frame="determiner(de)" id="7" infl="de" lcat="detp" lemma="de" lwtype="bep" naamval="stan" npagr="rest" pos="det" postag="LID(bep,stan,rest)" pt="lid" rel="det" root="de" sense="de" word="de"/>
            <node begin="4" end="5" frame="noun(de,count,sg)" gen="de" genus="zijd" getal="ev" graad="basis" id="8" lcat="np" lemma="kamer" naamval="stan" ntype="soort" num="sg" pos="noun" postag="N(soort,ev,basis,zijd,stan)" pt="n" rel="hd" rnum="sg" root="kamer" sense="kamer" word="kamer"/>
          </node>
        </node>
      </node>
      <node begin="5" end="6" frame="punct(uitroep)" id="9" lcat="punct" lemma="!" pos="punct" postag="LET()" pt="let" rel="--" root="!" sense="!" special="uitroep" word="!"/>
    </node>
    <sentence sentid="151">kijk eens in de kamer !</sentence>
    <metadata/>
  </alpino_ds>

'''


testtreestr[4] = '''

  <alpino_ds version="1.3" id="TARSP_Examples_from_Schlichting-195.xml">
    <node begin="0" cat="top" end="4" id="0" rel="top">
      <node begin="0" cat="sv1" end="4" id="1" rel="--">
        <node begin="0" end="1" frame="verb(hebben,sg1,aci)" id="2" infl="sg1" lcat="sv1" lemma="doen" pos="verb" postag="WW(pv,tgw,ev)" pt="ww" pvagr="ev" pvtijd="tgw" rel="hd" root="doe" sc="aci" sense="doe" stype="imparative" tense="present" word="doe" wvorm="pv"/>
        <node begin="1" buiging="met-e" end="2" frame="determiner(de,nwh,nmod,pro,nparg)" getal-n="zonder-n" id="3" index="1" infl="de" lcat="np" lemma="deze" naamval="stan" pdtype="det" pos="det" positie="nom" postag="VNW(aanw,det,stan,nom,met-e,zonder-n)" pt="vnw" rel="obj1" rnum="sg" root="deze" sense="deze" vwtype="aanw" wh="nwh" word="deze"/>
        <node begin="1" cat="inf" end="4" id="4" rel="vc">
          <node begin="1" end="2" id="5" index="1" rel="su"/>
          <node begin="2" end="3" frame="noun(het,count,sg)" gen="het" genus="onz" getal="ev" graad="dim" id="6" lcat="np" lemma="pop" naamval="stan" ntype="soort" num="sg" pos="noun" postag="N(soort,ev,dim,onz,stan)" pt="n" rel="obj1" rnum="sg" root="pop_DIM" sense="pop_DIM" word="poppetje"/>
          <node begin="3" buiging="zonder" end="4" frame="verb(hebben,inf(no_e),ninv(transitive,part_transitive(in)))" id="7" infl="inf(no_e)" lcat="inf" lemma="in_doen" pos="verb" positie="vrij" postag="WW(inf,vrij,zonder)" pt="ww" rel="hd" root="doe_in" sc="part_transitive(in)" sense="doe_in" word="indoen" wvorm="inf"/>
        </node>
      </node>
    </node>
    <sentence sentid="195">doe deze poppetje indoen</sentence>
    <metadata/>
  </alpino_ds>

'''


testtreestr[5] = '''
  <alpino_ds version="1.3" id="TARSP_Examples_from_Schlichting-149.xml">
    <node begin="0" cat="top" end="3" id="0" rel="top">
      <node begin="0" cat="sv1" end="2" id="1" rel="--">
        <node begin="0" end="1" frame="verb(hebben,sg1,intransitive)" id="2" infl="sg1" lcat="sv1" lemma="zien" pos="verb" postag="WW(pv,tgw,ev)" pt="ww" pvagr="ev" pvtijd="tgw" rel="hd" root="zie" sc="intransitive" sense="zie" stype="topic_drop" tense="present" word="zie" wvorm="pv"/>
        <node begin="1" end="2" frame="adverb" id="3" lcat="advp" lemma="maar" pos="adv" postag="BW()" pt="bw" rel="mod" root="maar" sense="maar" word="maar"/>
      </node>
      <node begin="2" end="3" frame="punct(uitroep)" id="4" lcat="punct" lemma="!" pos="punct" postag="LET()" pt="let" rel="--" root="!" sense="!" special="uitroep" word="!"/>
    </node>
    <sentence sentid="149">zie maar !</sentence>
    <metadata/>
  </alpino_ds>
'''


testtreestr[6] = '''
<alpino_ds version="1.6">
  <parser cats="1" skips="0" />
  <node begin="0" cat="top" end="7" id="0" rel="top">
    <node begin="0" cat="sv1" end="6" id="1" rel="--">
      <node begin="0" end="1" frame="verb(hebben,sg1,part_transitive(open))" his="normal" his_1="normal" id="2" infl="sg1" lcat="sv1" lemma="open_doen" pos="verb" postag="WW(pv,tgw,ev)" pt="ww" pvagr="ev" pvtijd="tgw" rel="hd" root="doe_open" sc="part_transitive(open)" sense="doe_open" stype="topic_drop" tense="present" word="doe" wvorm="pv"/>
      <node begin="1" end="2" frame="adverb" his="normal" his_1="normal" id="3" lcat="advp" lemma="maar" pos="adv" postag="BW()" pt="bw" rel="mod" root="maar" sense="maar" word="maar"/>
      <node begin="2" cat="np" end="4" id="4" rel="obj1">
        <node begin="2" end="3" frame="determiner(de)" his="normal" his_1="normal" id="5" infl="de" lcat="detp" lemma="de" lwtype="bep" naamval="stan" npagr="rest" pos="det" postag="LID(bep,stan,rest)" pt="lid" rel="det" root="de" sense="de" word="de"/>
        <node begin="3" end="4" frame="noun(both,both,both)" gen="both" genus="zijd" getal="ev" graad="basis" his="noun" id="6" lcat="np" lemma="hek" naamval="stan" ntype="soort" num="both" pos="noun" postag="N(soort,ev,basis,zijd,stan)" pt="n" rel="hd" rnum="sg" root="hek" sense="hek" word="hek"/>
      </node>
      <node begin="4" end="5" frame="adverb" his="normal" his_1="normal" id="7" lcat="advp" lemma="weer" pos="adv" postag="BW()" pt="bw" rel="mod" root="weer" sense="weer" word="weer"/>
      <node begin="5" buiging="zonder" end="6" frame="particle(open)" graad="basis" his="normal" his_1="normal" id="8" lcat="part" lemma="open" pos="part" positie="vrij" postag="ADJ(vrij,basis,zonder)" pt="adj" rel="svp" root="open" sense="open" word="open"/>
    </node>
    <node begin="6" end="7" frame="punct(punt)" his="normal" his_1="normal" id="9" lcat="punct" lemma="." pos="punct" postag="LET()" pt="let" rel="--" root="." sense="." special="punt" word="."/>
  </node>
  <sentence sentid="24">doe maar de hek weer open .</sentence>
<metadata>
<meta type="text" name="charencoding" value="UTF8" />
<meta type="text" name="childage" value="4;9" />
<meta type="int" name="childmonths" value="57" />
<meta type="text" name="comment" value="##META text title = TARSP_06" />
<meta type="text" name="session" value="TARSP_06" />
<meta type="text" name="origutt" value="doe maaw [: maar] de hek weew [: weer] open . " />
<meta type="text" name="parsefile" value="Unknown_corpus_TARSP_06_u00000000024.xml" />
<meta type="text" name="speaker" value="CHI" />
<meta type="int" name="uttendlineno" value="54" />
<meta type="int" name="uttid" value="24" />
<meta type="int" name="uttstartlineno" value="54" />
<meta type="text" name="name" value="chi" />
<meta type="text" name="SES" value="" />
<meta type="text" name="age" value="4;9" />
<meta type="text" name="custom" value="" />
<meta type="text" name="education" value="" />
<meta type="text" name="group" value="" />
<meta type="text" name="language" value="nld" />
<meta type="int" name="months" value="57" />
<meta type="text" name="role" value="Target_Child" />
<meta type="text" name="sex" value="female" />
<meta type="text" name="xsid" value="24" />
<meta type="int" name="uttno" value="24" />
</metadata>
</alpino_ds>
'''

testtreestr[7] = '''
  <alpino_ds version="1.3" id="TARSP_Examples_from_Schlichting-127.xml">
    <node begin="0" cat="top" end="5" id="0" rel="top">
      <node begin="0" cat="sv1" end="4" id="1" rel="--">
        <node begin="0" end="1" frame="verb(unacc,sg_heeft,intransitive)" id="2" infl="sg_heeft" lcat="sv1" lemma="zijn" pos="verb" postag="WW(pv,tgw,ev)" pt="ww" pvagr="ev" pvtijd="tgw" rel="hd" root="ben" sc="intransitive" sense="ben" stype="ynquestion" tense="present" word="is" wvorm="pv"/>
        <node begin="1" end="2" frame="determiner(de,nwh,nmod,pro,nparg)" getal="getal" id="3" infl="de" lcat="np" lemma="die" naamval="stan" pdtype="pron" persoon="3" pos="det" postag="VNW(aanw,pron,stan,vol,3,getal)" pt="vnw" rel="su" rnum="sg" root="die" sense="die" status="vol" vwtype="aanw" wh="nwh" word="die"/>
        <node begin="2" cat="pp" end="4" id="4" rel="mod">
          <node begin="2" end="3" frame="preposition(voor,[aan,door,uit,[in,de,plaats]])" id="5" lcat="pp" lemma="voor" pos="prep" postag="VZ(init)" pt="vz" rel="hd" root="voor" sense="voor" vztype="init" word="voor"/>
          <node begin="3" end="4" frame="proper_name(sg,'PER')" genus="zijd" getal="ev" graad="basis" id="6" lcat="np" lemma="Richard" naamval="stan" neclass="PER" ntype="eigen" num="sg" pos="name" postag="N(eigen,ev,basis,zijd,stan)" pt="n" rel="obj1" rnum="sg" root="Richard" sense="Richard" word="Richard"/>
        </node>
      </node>
      <node begin="4" end="5" frame="punct(vraag)" id="7" lcat="punct" lemma="?" pos="punct" postag="LET()" pt="let" rel="--" root="?" sense="?" special="vraag" word="?"/>
    </node>
    <sentence sentid="127">is die voor Richard ?</sentence>
    <metadata/>
  </alpino_ds>
'''

testtreestr[8] = '''
  <alpino_ds version="1.3" id="TARSP_Examples_from_Schlichting-133.xml">
    <node begin="0" cat="top" end="5" id="0" rel="top">
      <node begin="0" cat="sv1" end="4" id="1" rel="--">
        <node begin="0" end="1" frame="verb(hebben,sg,transitive_ndev_ndev)" id="2" infl="sg" lcat="sv1" lemma="mogen" pos="verb" postag="WW(pv,tgw,ev)" pt="ww" pvagr="ev" pvtijd="tgw" rel="hd" root="mag" sc="transitive_ndev_ndev" sense="mag" stype="ynquestion" tense="present" word="mag" wvorm="pv"/>
        <node begin="1" case="nom" def="def" end="2" frame="pronoun(nwh,fir,sg,de,nom,def)" gen="de" getal="ev" id="3" lcat="np" lemma="ik" naamval="nomin" num="sg" pdtype="pron" per="fir" persoon="1" pos="pron" postag="VNW(pers,pron,nomin,vol,1,ev)" pt="vnw" rel="su" rnum="sg" root="ik" sense="ik" status="vol" vwtype="pers" wh="nwh" word="ik"/>
        <node begin="2" end="3" frame="determiner(het,nwh,nmod,pro,nparg,wkpro)" genus="onz" getal="ev" id="4" infl="het" lcat="np" lemma="het" naamval="stan" pdtype="pron" persoon="3" pos="det" postag="VNW(pers,pron,stan,red,3,ev,onz)" pt="vnw" rel="obj1" rnum="sg" root="het" sense="het" status="red" vwtype="pers" wh="nwh" word="het"/>
        <node begin="3" end="4" frame="sentence_adverb" id="5" lcat="advp" lemma="ook" pos="adv" postag="BW()" pt="bw" rel="mod" root="ook" sense="ook" special="sentence" word="ook"/>
      </node>
      <node begin="4" end="5" frame="punct(vraag)" id="6" lcat="punct" lemma="?" pos="punct" postag="LET()" pt="let" rel="--" root="?" sense="?" special="vraag" word="?"/>
    </node>
    <sentence sentid="133">mag ik het ook ?</sentence>
    <metadata/>
  </alpino_ds>
'''

testtreestr[9] = '''
  <alpino_ds version="1.3" id="TARSP_Examples_from_Schlichting-134.xml">
    <node begin="0" cat="top" end="6" id="0" rel="top">
      <node begin="0" cat="sv1" end="5" id="1" rel="--">
        <node begin="0" end="1" frame="verb(hebben,modal_not_u,aux(inf))" id="2" infl="modal_not_u" lcat="sv1" lemma="zullen" pos="verb" postag="WW(pv,tgw,ev)" pt="ww" pvagr="ev" pvtijd="tgw" rel="hd" root="zal" sc="aux(inf)" sense="zal" stype="ynquestion" tense="present" word="zal" wvorm="pv"/>
        <node begin="1" case="nom" def="def" end="2" frame="pronoun(nwh,fir,sg,de,nom,def)" gen="de" getal="ev" id="3" index="1" lcat="np" lemma="ik" naamval="nomin" num="sg" pdtype="pron" per="fir" persoon="1" pos="pron" postag="VNW(pers,pron,nomin,vol,1,ev)" pt="vnw" rel="su" rnum="sg" root="ik" sense="ik" status="vol" vwtype="pers" wh="nwh" word="ik"/>
        <node begin="1" cat="inf" end="5" id="4" rel="vc">
          <node begin="1" end="2" id="5" index="1" rel="su"/>
          <node begin="2" end="3" frame="tmp_adverb" id="6" lcat="advp" lemma="eens" pos="adv" postag="BW()" pt="bw" rel="mod" root="eens" sense="eens" special="tmp" word="eens"/>
          <node aform="base" begin="3" end="4" frame="adjective(pred(nonadv))" id="7" infl="pred" lcat="ap" lemma="zo" pos="adj" postag="BW()" pt="bw" rel="predc" root="zo" sense="zo" vform="adj" word="zo"/>
          <node begin="4" buiging="zonder" end="5" frame="verb(hebben,inf(no_e),nonp_copula)" id="8" infl="inf(no_e)" lcat="inf" lemma="doen" pos="verb" positie="vrij" postag="WW(inf,vrij,zonder)" pt="ww" rel="hd" root="doe" sc="nonp_copula" sense="doe" word="doen" wvorm="inf"/>
        </node>
      </node>
      <node begin="5" end="6" frame="punct(vraag)" id="9" lcat="punct" lemma="?" pos="punct" postag="LET()" pt="let" rel="--" root="?" sense="?" special="vraag" word="?"/>
    </node>
    <sentence sentid="134">zal ik eens zo doen ?</sentence>
    <metadata/>
  </alpino_ds>
'''

testtreestr[10] = '''
  <alpino_ds version="1.3" id="TARSP_Examples_from_Schlichting-141.xml">
    <node begin="0" cat="top" end="7" id="0" rel="top">
      <node begin="0" cat="sv1" end="6" id="1" rel="--">
        <node begin="0" end="1" frame="verb(hebben,sg,transitive_ndev_ndev)" id="2" infl="sg" lcat="sv1" lemma="mogen" pos="verb" postag="WW(pv,tgw,ev)" pt="ww" pvagr="ev" pvtijd="tgw" rel="hd" root="mag" sc="transitive_ndev_ndev" sense="mag" stype="ynquestion" tense="present" word="mag" wvorm="pv"/>
        <node begin="1" case="nom" def="def" end="2" frame="pronoun(nwh,fir,sg,de,nom,def)" gen="de" getal="ev" id="3" lcat="np" lemma="ik" naamval="nomin" num="sg" pdtype="pron" per="fir" persoon="1" pos="pron" postag="VNW(pers,pron,nomin,vol,1,ev)" pt="vnw" rel="su" rnum="sg" root="ik" sense="ik" status="vol" vwtype="pers" wh="nwh" word="ik"/>
        <node begin="2" end="3" frame="er_vp_adverb" getal="getal" id="4" lcat="advp" lemma="er" naamval="stan" pdtype="adv-pron" persoon="3" pos="adv" postag="VNW(aanw,adv-pron,stan,red,3,getal)" pt="vnw" rel="mod" root="er" sense="er" special="er" status="red" vwtype="aanw" word="er"/>
        <node begin="3" end="4" frame="sentence_adverb" id="5" lcat="advp" lemma="ook" pos="adv" postag="BW()" pt="bw" rel="mod" root="ook" sense="ook" special="sentence" word="ook"/>
        <node begin="4" cat="np" end="6" id="6" rel="obj1">
          <node begin="4" end="5" frame="determiner(een)" id="7" infl="een" lcat="detp" lemma="een" lwtype="onbep" naamval="stan" npagr="agr" pos="det" postag="LID(onbep,stan,agr)" pt="lid" rel="det" root="een" sense="een" word="een"/>
          <node begin="5" end="6" frame="meas_mod_noun(het,count,meas)" gen="het" genus="onz" getal="ev" graad="basis" id="8" lcat="np" lemma="paar" naamval="stan" ntype="soort" num="meas" pos="noun" postag="N(soort,ev,basis,onz,stan)" pt="n" rel="hd" rnum="sg" root="paar" sense="paar" special="meas_mod" word="paar"/>
        </node>
      </node>
      <node begin="6" end="7" frame="punct(vraag)" id="9" lcat="punct" lemma="?" pos="punct" postag="LET()" pt="let" rel="--" root="?" sense="?" special="vraag" word="?"/>
    </node>
    <sentence sentid="141">mag ik er ook een paar ?</sentence>
    <metadata/>
  </alpino_ds>
'''

testtreestr[11] = '''
  <alpino_ds version="1.3" id="TARSP_Examples_from_Schlichting-142.xml">
    <node begin="0" cat="top" end="9" id="0" rel="top">
      <node begin="0" cat="sv1" end="8" id="1" rel="--">
        <node begin="0" end="1" frame="verb(hebben,modal_not_u,aux(inf))" id="2" infl="modal_not_u" lcat="sv1" lemma="zullen" pos="verb" postag="WW(pv,tgw,ev)" pt="ww" pvagr="ev" pvtijd="tgw" rel="hd" root="zal" sc="aux(inf)" sense="zal" stype="ynquestion" tense="present" word="zal" wvorm="pv"/>
        <node begin="1" case="nom" def="def" end="2" frame="pronoun(nwh,fir,sg,de,nom,def)" gen="de" getal="ev" id="3" index="1" lcat="np" lemma="ik" naamval="nomin" num="sg" pdtype="pron" per="fir" persoon="1" pos="pron" postag="VNW(pers,pron,nomin,vol,1,ev)" pt="vnw" rel="su" rnum="sg" root="ik" sense="ik" status="vol" vwtype="pers" wh="nwh" word="ik"/>
        <node begin="1" cat="inf" end="8" id="4" rel="vc">
          <node begin="1" end="2" id="5" index="1" rel="su"/>
          <node begin="2" end="3" frame="tmp_adverb" id="6" lcat="advp" lemma="eens" pos="adv" postag="BW()" pt="bw" rel="mod" root="eens" sense="eens" special="tmp" word="eens"/>
          <node begin="4" cat="np" end="6" id="7" rel="obj1">
            <node begin="4" end="5" frame="determiner(een)" id="8" infl="een" lcat="detp" lemma="een" lwtype="onbep" naamval="stan" npagr="agr" pos="det" postag="LID(onbep,stan,agr)" pt="lid" rel="det" root="een" sense="een" word="een"/>
            <node begin="5" end="6" frame="noun(de,count,sg)" gen="de" genus="zijd" getal="ev" graad="basis" id="9" lcat="np" lemma="helikopter" naamval="stan" ntype="soort" num="sg" pos="noun" postag="N(soort,ev,basis,zijd,stan)" pt="n" rel="hd" rnum="sg" root="helikopter" sense="helikopter" word="helikopter"/>
          </node>
          <node begin="3" cat="pp" end="7" id="10" rel="pc">
            <node begin="3" end="4" frame="er_loc_adverb" getal="getal" id="11" lcat="advp" lemma="hier" naamval="obl" pdtype="adv-pron" persoon="3o" pos="adv" postag="VNW(aanw,adv-pron,obl,vol,3o,getal)" pt="vnw" rel="obj1" root="hier" sense="hier" special="er_loc" status="vol" vwtype="aanw" word="hier"/>
            <node begin="6" end="7" frame="preposition(van,[af,uit,vandaan,[af,aan]])" id="12" lcat="pp" lemma="van" pos="prep" postag="VZ(fin)" pt="vz" rel="hd" root="van" sense="van" vztype="fin" word="van"/>
          </node>
          <node begin="7" buiging="zonder" end="8" frame="verb(hebben,inf,np_pc_pp(van))" id="13" infl="inf" lcat="inf" lemma="maken" pos="verb" positie="vrij" postag="WW(inf,vrij,zonder)" pt="ww" rel="hd" root="maak" sc="np_pc_pp(van)" sense="maak-van" word="maken" wvorm="inf"/>
        </node>
      </node>
      <node begin="8" end="9" frame="punct(vraag)" id="14" lcat="punct" lemma="?" pos="punct" postag="LET()" pt="let" rel="--" root="?" sense="?" special="vraag" word="?"/>
    </node>
    <sentence sentid="142">zal ik eens hier een helikopter van maken ?</sentence>
    <metadata/>
  </alpino_ds>
'''

testtreestr[12] = '''
  <alpino_ds version="1.3" id="TARSP_Examples_from_Schlichting-126.xml">
    <node begin="0" cat="top" end="4" id="0" rel="top">
      <node begin="0" cat="sv1" end="3" id="1" rel="--">
        <node begin="0" end="1" frame="verb(hebben,sg,intransitive)" id="2" infl="sg" lcat="sv1" lemma="mogen" pos="verb" postag="WW(pv,tgw,ev)" pt="ww" pvagr="ev" pvtijd="tgw" rel="hd" root="mag" sc="intransitive" sense="mag" stype="ynquestion" tense="present" word="mag" wvorm="pv"/>
        <node begin="1" case="nom" def="def" end="2" frame="pronoun(nwh,fir,sg,de,nom,def)" gen="de" getal="ev" id="3" lcat="np" lemma="ik" naamval="nomin" num="sg" pdtype="pron" per="fir" persoon="1" pos="pron" postag="VNW(pers,pron,nomin,vol,1,ev)" pt="vnw" rel="su" rnum="sg" root="ik" sense="ik" status="vol" vwtype="pers" wh="nwh" word="ik"/>
        <node begin="2" end="3" frame="adverb" id="4" lcat="advp" lemma="nog" pos="adv" postag="BW()" pt="bw" rel="mod" root="nog" sense="nog" word="nog"/>
      </node>
      <node begin="3" end="4" frame="punct(vraag)" id="5" lcat="punct" lemma="?" pos="punct" postag="LET()" pt="let" rel="--" root="?" sense="?" special="vraag" word="?"/>
    </node>
    <sentence sentid="126">mag ik nog ?</sentence>
    <metadata/>
  </alpino_ds>
'''

testtreestr[13] = '''
<alpino_ds version="1.6">
  <parser cats="1" skips="0" />
  <node begin="0" cat="top" end="6" id="0" rel="top">
    <node begin="0" cat="sv1" end="5" id="1" rel="--">
      <node begin="0" end="1" frame="verb(zijn,sg3,aux(inf))" his="normal" his_1="normal" id="2" infl="sg3" lcat="sv1" lemma="gaan" pos="verb" postag="WW(pv,tgw,met-t)" pt="ww" pvagr="met-t" pvtijd="tgw" rel="hd" root="ga" sc="aux(inf)" sense="ga" stype="ynquestion" tense="present" word="gaat" wvorm="pv"/>
      <node begin="1" cat="np" end="3" id="3" index="1" rel="su">
        <node begin="1" end="2" frame="determiner(de)" his="normal" his_1="normal" id="4" infl="de" lcat="detp" lemma="de" lwtype="bep" naamval="stan" npagr="rest" pos="det" postag="LID(bep,stan,rest)" pt="lid" rel="det" root="de" sense="de" word="de"/>
        <node begin="2" end="3" frame="noun(de,count,sg)" gen="de" genus="zijd" getal="ev" graad="basis" his="normal" his_1="normal" id="5" lcat="np" lemma="juf" naamval="stan" ntype="soort" num="sg" pos="noun" postag="N(soort,ev,basis,zijd,stan)" pt="n" rel="hd" rnum="sg" root="juf" sense="juf" word="juf"/>
      </node>
      <node begin="1" cat="inf" end="5" id="6" rel="vc">
        <node begin="1" end="3" id="7" index="1" rel="su"/>
        <node begin="3" end="4" frame="sentence_adverb" his="normal" his_1="normal" id="8" lcat="advp" lemma="ook" pos="adv" postag="BW()" pt="bw" rel="mod" root="ook" sense="ook" special="sentence" word="ook"/>
        <node begin="4" buiging="zonder" end="5" frame="verb('hebben/zijn',inf,intransitive)" his="normal" his_1="normal" id="9" infl="inf" lcat="inf" lemma="verhuizen" pos="verb" positie="vrij" postag="WW(inf,vrij,zonder)" pt="ww" rel="hd" root="verhuis" sc="intransitive" sense="verhuis" word="verhuizen" wvorm="inf"/>
      </node>
    </node>
    <node begin="5" end="6" frame="punct(vraag)" his="normal" his_1="normal" id="10" lcat="punct" lemma="?" pos="punct" postag="LET()" pt="let" rel="--" root="?" sense="?" special="vraag" word="?"/>
  </node>
  <sentence sentid="25">gaat de juf ook verhuizen ?</sentence>
<metadata>
<meta type="text" name="charencoding" value="UTF8" />
<meta type="text" name="childage" value="6;6" />
<meta type="int" name="childmonths" value="78" />
<meta type="text" name="comment" value="##META text title = TARSP_09" />
<meta type="text" name="session" value="TARSP_09" />
<meta type="text" name="origutt" value="gaat de juf ook verhuizen?  " />
<meta type="text" name="parsefile" value="Unknown_corpus_TARSP_09_u00000000025.xml" />
<meta type="text" name="speaker" value="CHI" />
<meta type="int" name="uttendlineno" value="56" />
<meta type="int" name="uttid" value="25" />
<meta type="int" name="uttstartlineno" value="56" />
<meta type="text" name="name" value="chi" />
<meta type="text" name="SES" value="" />
<meta type="text" name="age" value="6;6" />
<meta type="text" name="custom" value="" />
<meta type="text" name="education" value="" />
<meta type="text" name="group" value="" />
<meta type="text" name="language" value="nld" />
<meta type="int" name="months" value="78" />
<meta type="text" name="role" value="Target_Child" />
<meta type="text" name="sex" value="female" />
<meta type="text" name="xsid" value="25" />
<meta type="int" name="uttno" value="25" />
</metadata>
</alpino_ds>
'''


testtrees = []
for ctr in testtreestr:
    # print(ctr)
    testtrees.append((ctr, etree.fromstring(testtreestr[ctr])))

# testtrees = [(ctr, etree.fromstring(testtreestr[ctr])) for ctr in testtreestr ]
labeledfs = [('wx', wx), ('wxy', wxy), ('wxyz', wxyz), ('wxyz5', wxyz5), ('wondx', wondx), ('wond4', wond4), ('wond5plus', wond5plus)]


def test_imperatives():
    for (treename, testtree) in testtrees:
        print(treename)
        for label, thef in labeledfs:
            # print('starting', label)
            results = thef(testtree)
            print(label, len(results))
