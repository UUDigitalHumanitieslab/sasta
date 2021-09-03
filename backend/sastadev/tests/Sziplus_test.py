from lxml import etree

from sastadev.Sziplus import empty, notempty, sziplus6

testtree1str = '''  <alpino_ds version="1.3" id="Treebank_Schlichting_CHAT-115.xml">
    <node begin="0" cat="top" end="8" id="0" rel="top">
      <node begin="0" cat="smain" end="8" id="1" rel="--">
        <node begin="0" end="1" frame="tmp_adverb" id="2" lcat="advp" lemma="dan" pos="adv" postag="BW()" pt="bw" rel="mod" root="dan" sense="dan" special="tmp" word="dan"/>
        <node begin="1" end="2" frame="verb(hebben,sg3,np_ld_pp)" id="3" infl="sg3" lcat="smain" lemma="leggen" pos="verb" postag="WW(pv,tgw,met-t)" pt="ww" pvagr="met-t" pvtijd="tgw" rel="hd" root="leg" sc="np_ld_pp" sense="leg" stype="declarative" tense="present" word="legt" wvorm="pv"/>
        <node begin="2" case="nom" def="def" end="3" frame="pronoun(nwh,thi,sg,de,nom,def)" gen="de" genus="masc" getal="ev" id="4" lcat="np" lemma="hij" naamval="nomin" num="sg" pdtype="pron" per="thi" persoon="3" pos="pron" postag="VNW(pers,pron,nomin,vol,3,ev,masc)" pt="vnw" rel="su" rnum="sg" root="hij" sense="hij" status="vol" vwtype="pers" wh="nwh" word="hij"/>
        <node begin="3" end="4" frame="determiner(de,nwh,nmod,pro,nparg)" getal="getal" id="5" infl="de" lcat="np" lemma="die" naamval="stan" pdtype="pron" persoon="3" pos="det" postag="VNW(aanw,pron,stan,vol,3,getal)" pt="vnw" rel="obj1" rnum="sg" root="die" sense="die" status="vol" vwtype="aanw" wh="nwh" word="die"/>
        <node begin="4" end="5" frame="adverb" id="6" lcat="advp" lemma="zo" pos="adv" postag="BW()" pt="bw" rel="mod" root="zo" sense="zo" word="zo"/>
        <node begin="5" cat="pp" end="8" id="7" rel="ld">
          <node begin="5" end="6" frame="preposition(op,[af,na])" id="8" lcat="pp" lemma="op" pos="prep" postag="VZ(init)" pt="vz" rel="hd" root="op" sense="op" vztype="init" word="op"/>
          <node begin="6" cat="np" end="8" id="9" rel="obj1">
            <node begin="6" end="7" frame="determiner(de)" id="10" infl="de" lcat="detp" lemma="de" lwtype="bep" naamval="stan" npagr="rest" pos="det" postag="LID(bep,stan,rest)" pt="lid" rel="det" root="de" sense="de" word="de"/>
            <node begin="7" end="8" frame="noun(both,both,both)" gen="both" genus="zijd" getal="ev" graad="basis" id="11" lcat="np" lemma="rug " naamval="stan" ntype="soort" num="both" pos="noun" postag="N(soort,ev,basis,zijd,stan)" pt="n" rel="hd" rnum="sg" root="rug " sense="rug " word="rug "/>
          </node>
        </node>
      </node>
    </node>
    <sentence sentid="115">dan legt hij die zo op de rug</sentence>
    <metadata>
      <meta type="text" name="sourcefile" value="treebank_TARSP_samengevoegd_CHAT.xlsx"/>
      <meta type="text" name="auteur" value="Liesbeth Schlichting"/>
      <meta type="text" name="jaar" value="3"/>
      <meta type="text" name="titel" value="Taal Analyse Remediëring en Screening Procedure: TARSP"/>
      <meta type="text" name="subtitel" value="Taalontwikkelingsschaal van Nederlandse kinderen van 1-4 jaar"/>
      <meta type="text" name="plaats" value="Amsterdam"/>
      <meta type="text" name="uitgever" value="Pearson"/>
      <meta type="text" name="Druk" value="7e"/>
      <meta type="text" name="ID" value="M003"/>
      <meta type="text" name="Category" value="Zinsconstructies"/>
      <meta type="text" name="Subcat" value="Mededelende Zin"/>
      <meta type="text" name="Level" value="Zc"/>
      <meta type="text" name="Item" value="6+"/>
      <meta type="text" name="pagina" value="56"/>
      <meta type="text" name="fase" value="6"/>
      <meta type="int" name="months" value="46"/>
      <meta type="text" name="age" value="3;10"/>
      <meta type="text" name="kind" value="Davey"/>
      <meta type="text" name="origutt" value="dan legt hij die zo op de rug"/>
      <meta type="text" name="opmerkingen" value="ben"/>
      <meta type="text" name="opmerkingen2" value="buiten gieg [:vliegtuig]"/>
      <meta type="text" name="maand" value="10"/>
    </metadata>
  </alpino_ds>
'''

testtree1 = etree.fromstring(testtree1str)

testtree2str = '''
  <alpino_ds version="1.3" id="Treebank_Schlichting_CHAT-1.xml">
    <node begin="0" cat="top" end="2" id="0" rel="top">
      <node begin="0" cat="np" end="2" id="1" rel="--">
        <node begin="0" buiging="zonder" end="1" frame="determiner(de,nwh,nmod,pro,nparg)" id="2" infl="de" lcat="detp" lemma="die" naamval="stan" npagr="rest" pdtype="det" pos="det" positie="prenom" postag="VNW(aanw,det,stan,prenom,zonder,rest)" pt="vnw" rel="det" root="die" sense="die" vwtype="aanw" wh="nwh" word="die"/>
        <node begin="1" end="2" frame="noun(both,both,both)" gen="both" genus="zijd" getal="ev" graad="basis" id="3" lcat="np" lemma="hier " naamval="stan" ntype="soort" num="both" pos="noun" postag="N(soort,ev,basis,zijd,stan)" pt="n" rel="hd" rnum="sg" root="hier " sense="hier " word="hier "/>
      </node>
    </node>
    <sentence sentid="1">die hier</sentence>
    <metadata>
      <meta type="text" name="sourcefile" value="treebank_TARSP_samengevoegd_CHAT.xlsx"/>
      <meta type="text" name="auteur" value="Liesbeth Schlichting"/>
      <meta type="text" name="jaar" value="1"/>
      <meta type="text" name="titel" value="Taal Analyse Remediëring en Screening Procedure: TARSP"/>
      <meta type="text" name="subtitel" value="Taalontwikkelingsschaal van Nederlandse kinderen van 1-4 jaar"/>
      <meta type="text" name="plaats" value="Amsterdam"/>
      <meta type="text" name="uitgever" value="Pearson"/>
      <meta type="text" name="Druk" value="7e"/>
      <meta type="text" name="ID" value="M064"/>
      <meta type="text" name="Category" value="Zinsconstructies"/>
      <meta type="text" name="Subcat" value="Mededelende Zin"/>
      <meta type="text" name="Level" value="Zc"/>
      <meta type="text" name="Item" value="OndB"/>
      <meta type="text" name="pagina" value="45"/>
      <meta type="text" name="fase" value="2"/>
      <meta type="text" name="maand" value="11"/>
      <meta type="int" name="months" value="23"/>
      <meta type="text" name="age" value="1;11"/>
      <meta type="text" name="kind" value="Pieter"/>
      <meta type="text" name="origutt" value="die hier"/>
    </metadata>
  </alpino_ds>
'''
testtree2 = etree.fromstring(testtree2str)

testtree3str = '''
  <alpino_ds version="1.3" id="Treebank_Schlichting_CHAT-124.xml">
    <node begin="0" cat="top" end="9" id="0" rel="top">
      <node begin="5" end="6" frame="complementizer(als)" id="1" lcat="--" lemma="als" pos="comp" postag="VZ(init)" pt="vz" rel="--" root="als" sc="als" sense="als" vztype="init" word="als"/>
      <node begin="6" end="7" frame="reflexive(je,both)" getal="ev" id="2" lcat="--" lemma="je" naamval="nomin" num="both" pdtype="pron" per="je" persoon="2v" pos="pron" postag="VNW(pers,pron,nomin,red,2v,ev)" pt="vnw" refl="refl" rel="--" root="je" sense="je" status="red" vwtype="pers" word="je"/>
      <node begin="0" cat="du" end="9" id="3" rel="--">
        <node begin="0" cat="smain" end="5" id="4" rel="dp">
          <node begin="1" end="2" frame="verb(zijn,sg1,aux(inf))" id="5" infl="sg1" lcat="smain" lemma="gaan" pos="verb" postag="WW(pv,tgw,ev)" pt="ww" pvagr="ev" pvtijd="tgw" rel="hd" root="ga" sc="aux(inf)" sense="ga" stype="declarative" tense="present" word="ga" wvorm="pv"/>
          <node begin="2" case="nom" def="def" end="3" frame="pronoun(nwh,fir,sg,de,nom,def)" gen="de" getal="ev" id="6" index="1" lcat="np" lemma="ik" naamval="nomin" num="sg" pdtype="pron" per="fir" persoon="1" pos="pron" postag="VNW(pers,pron,nomin,vol,1,ev)" pt="vnw" rel="su" rnum="sg" root="ik" sense="ik" status="vol" vwtype="pers" wh="nwh" word="ik"/>
          <node begin="0" cat="inf" end="5" id="7" rel="vc">
            <node begin="0" end="1" frame="determiner(de,nwh,nmod,pro,nparg)" getal="getal" id="8" infl="de" lcat="np" lemma="die" naamval="stan" pdtype="pron" persoon="3" pos="det" postag="VNW(aanw,pron,stan,vol,3,getal)" pt="vnw" rel="obj1" rnum="sg" root="die" sense="die" status="vol" vwtype="aanw" wh="nwh" word="die"/>
            <node begin="2" end="3" id="9" index="1" rel="su"/>
            <node begin="3" end="4" frame="sentence_adverb" id="10" lcat="advp" lemma="altijd" pos="adv" postag="BW()" pt="bw" rel="mod" root="altijd" sense="altijd" special="sentence" word="altijd"/>
            <node begin="4" buiging="zonder" end="5" frame="verb(hebben,inf,ninv(transitive,part_transitive(op)))" id="11" infl="inf" lcat="inf" lemma="op_eten" pos="verb" positie="vrij" postag="WW(inf,vrij,zonder)" pt="ww" rel="hd" root="eet_op" sc="part_transitive(op)" sense="eet_op" word="opeten" wvorm="inf"/>
          </node>
        </node>
        <node begin="7" cat="np" end="9" id="12" rel="dp">
          <node begin="7" end="8" frame="determiner(het,nwh,nmod,pro,nparg,wkpro)" id="13" infl="het" lcat="detp" lemma="het" lwtype="bep" naamval="stan" npagr="evon" pos="det" postag="LID(bep,stan,evon)" pt="lid" rel="det" root="het" sense="het" wh="nwh" word="het"/>
          <node begin="8" end="9" frame="noun(both,both,both)" gen="both" genus="onz" getal="ev" graad="basis" id="14" lcat="np" lemma="bakt " naamval="stan" ntype="soort" num="both" pos="noun" postag="N(soort,ev,basis,onz,stan)" pt="n" rel="hd" rnum="sg" root="bakt " sense="bakt " word="bakt "/>
        </node>
      </node>
    </node>
    <sentence sentid="124">die ga ik altijd opeten als je het bakt</sentence>
    <metadata>
      <meta type="text" name="sourcefile" value="treebank_TARSP_samengevoegd_CHAT.xlsx"/>
      <meta type="text" name="auteur" value="Liesbeth Schlichting"/>
      <meta type="text" name="jaar" value="3"/>
      <meta type="text" name="titel" value="Taal Analyse Remediëring en Screening Procedure: TARSP"/>
      <meta type="text" name="subtitel" value="Taalontwikkelingsschaal van Nederlandse kinderen van 1-4 jaar"/>
      <meta type="text" name="plaats" value="Amsterdam"/>
      <meta type="text" name="uitgever" value="Pearson"/>
      <meta type="text" name="Druk" value="7e"/>
      <meta type="text" name="ID" value="M011"/>
      <meta type="text" name="Category" value="Zinsconstructies"/>
      <meta type="text" name="Subcat" value="Mededelende Zin"/>
      <meta type="text" name="Level" value="Zc"/>
      <meta type="text" name="Item" value="Bbijzin"/>
      <meta type="text" name="pagina" value="57"/>
      <meta type="text" name="fase" value="6"/>
      <meta type="int" name="months" value="46"/>
      <meta type="text" name="age" value="3;10"/>
      <meta type="text" name="kind" value="Timo"/>
      <meta type="text" name="origutt" value="die ga ik altijd opeten als je het bakt"/>
      <meta type="text" name="opmerkingen" value="Wat doet…"/>
      <meta type="text" name="opmerkingen2" value="buiten gieg [:vliegtuig]"/>
      <meta type="text" name="maand" value="10"/>
    </metadata>
  </alpino_ds>
'''
testtree3 = etree.fromstring(testtree3str)


testtree4str = '''
  <alpino_ds version="1.3" id="Treebank_Schlichting_CHAT-171.xml">
    <node begin="0" cat="top" end="7" id="0" rel="top">
      <node begin="0" cat="whq" end="7" id="1" rel="--">
        <node begin="0" end="1" frame="waar_adverb(om)" id="2" index="1" lcat="pp" lemma="waarom" pos="pp" postag="BW()" pt="bw" rel="whd" root="waarom" sense="waarom" special="waar" word="waarom"/>
        <node begin="0" cat="sv1" end="7" id="3" rel="body">
          <node begin="0" end="1" id="4" index="1" rel="mod"/>
          <node begin="1" end="2" frame="verb(hebben,sg1,pred_np)" id="5" infl="sg1" lcat="sv1" lemma="vinden" pos="verb" postag="WW(pv,tgw,ev)" pt="ww" pvagr="ev" pvtijd="tgw" rel="hd" root="vind" sc="pred_np" sense="vind" stype="whquestion" tense="present" word="vind" wvorm="pv"/>
          <node begin="2" case="both" def="def" end="3" frame="pronoun(nwh,je,sg,de,both,def,wkpro)" gen="de" getal="ev" id="6" lcat="np" lemma="je" naamval="nomin" num="sg" pdtype="pron" per="je" persoon="2v" pos="pron" postag="VNW(pers,pron,nomin,red,2v,ev)" pt="vnw" rel="su" rnum="sg" root="je" sense="je" special="wkpro" status="red" vwtype="pers" wh="nwh" word="je"/>
          <node begin="3" end="4" frame="determiner(het,nwh,nmod,pro,nparg)" getal="ev" id="7" infl="het" lcat="np" lemma="dat" naamval="stan" pdtype="pron" persoon="3o" pos="det" postag="VNW(aanw,pron,stan,vol,3o,ev)" pt="vnw" rel="obj1" rnum="sg" root="dat" sense="dat" status="vol" vwtype="aanw" wh="nwh" word="dat"/>
          <node begin="4" end="5" frame="adverb" id="8" lcat="advp" lemma="niet" pos="adv" postag="BW()" pt="bw" rel="mod" root="niet" sense="niet" word="niet"/>
          <node aform="base" begin="5" buiging="zonder" end="6" frame="adjective(no_e(adv))" graad="basis" id="9" infl="no_e" lcat="ap" lemma="leuk" pos="adj" positie="vrij" postag="ADJ(vrij,basis,zonder)" pt="adj" rel="mod" root="leuk" sense="leuk" vform="adj" word="leuk"/>
          <node begin="6" end="7" frame="number(hoofd(both))" id="10" infl="both" lcat="np" lemma="? " numtype="hoofd" pos="num" positie="vrij" postag="TW(hoofd,vrij)" pt="tw" rel="predc" rnum="sg" root="? " sense="? " special="hoofd" word="? "/>
        </node>
      </node>
    </node>
    <sentence sentid="171">waarom vind je dat niet leuk ?</sentence>
    <metadata>
      <meta type="text" name="sourcefile" value="treebank_TARSP_samengevoegd_CHAT.xlsx"/>
      <meta type="text" name="auteur" value="Liesbeth Schlichting"/>
      <meta type="text" name="jaar" value="3"/>
      <meta type="text" name="titel" value="Taal Analyse Remediëring en Screening Procedure: TARSP"/>
      <meta type="text" name="subtitel" value="Taalontwikkelingsschaal van Nederlandse kinderen van 1-4 jaar"/>
      <meta type="text" name="plaats" value="Amsterdam"/>
      <meta type="text" name="uitgever" value="Pearson"/>
      <meta type="text" name="Druk" value="7e"/>
      <meta type="text" name="ID" value="M113"/>
      <meta type="text" name="Category" value="Zinsconstructies"/>
      <meta type="text" name="Subcat" value="Vragen"/>
      <meta type="text" name="Level" value="Zc"/>
      <meta type="text" name="Item" value="Vr5+"/>
      <meta type="text" name="pagina" value="62"/>
      <meta type="text" name="fase" value="6"/>
      <meta type="int" name="months" value="47"/>
      <meta type="text" name="age" value="3;11"/>
      <meta type="text" name="kind" value="Sander"/>
      <meta type="text" name="origutt" value="waarom vind je dat niet leuk?"/>
      <meta type="text" name="opmerkingen" value="wat is dit?"/>
      <meta type="text" name="opmerkingen2" value="helicopter -&gt; helikopter"/>
      <meta type="text" name="maand" value="11"/>
    </metadata>
  </alpino_ds>
'''

testtree4 = etree.fromstring(testtree4str)

testtree5str = '''
  <alpino_ds version="1.3" id="Tarvb2-1.xml">
    <node begin="0" cat="top" end="1" id="0" rel="top">
      <node begin="0" end="1" frame="noun(both,both,both)" gen="both" genus="zijd" getal="ev" graad="basis" id="1" lcat="np" lemma="poppie" naamval="stan" ntype="soort" num="both" pos="noun" postag="N(soort,ev,basis,zijd,stan)" pt="n" rel="--" rnum="sg" root="poppie" sense="poppie" word="poppie"/>
    </node>
    <sentence sentid="01 ">poppie</sentence>
    <metadata>
      <meta type="int" name="uttid" value="1"/>
    </metadata>
  </alpino_ds>
'''

testtree5 = etree.fromstring(testtree5str)


def report(nodelist, f):
    if f(nodelist):
        print('OK')
        return True
    else:
        print('NOT OK')
        return False


def test_sziplus():
    test1 = sziplus6(testtree1)
    assert report(test1, notempty)
    test2 = sziplus6(testtree2)
    assert report(test2, empty)
    test3 = sziplus6(testtree3)
    assert report(test3, empty)
    test4 = sziplus6(testtree4)
    assert report(test4, notempty)
    test5 = sziplus6(testtree5)
    assert report(test5, empty)
